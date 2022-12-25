import datetime
import json
import logging
import secrets
import threading
from urllib.parse import urlencode

import requests
from flask import Flask, request
from werkzeug.serving import make_server


# This class is a thread that will listen for incoming connections and create a new thread for each
# connection
class ServerThread(threading.Thread):
    # https://stackoverflow.com/a/45017691
    def __init__(self, app, host, port):
        threading.Thread.__init__(self)
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


# > This class is a subclass of ServerThread, and it's used to authenticate users
class Auth(ServerThread):
    def __init__(
        self,
        client_id,
        client_secret=None,
        host: str = None,
        port: int = None,
        callback_url: str = None,
        store_token=True,
        token_path="token.pickle",
    )-> dict:
        """
        This function initializes the class with the client_id, client_secret, host, port, callback_url,
        store_token, and token_path
        
        Args:
          client_id: Your client ID.
          client_secret: The client secret for your app.
          host (str): The hostname of the server that will be running the OAuth2 callback.
          port (int): The port number that the server will run on.
          callback_url (str): The URL that the user will be redirected to after they authorize your
        application.
          store_token: If True, the token will be stored in a file called token.pickle. Defaults to True
          token_path: The path to the file where the token will be stored. Defaults to token.pickle
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = "https://myanimelist.net/v1/oauth2/authorize"
        self.host = host
        self.port = port
        self.store_token = store_token
        self.token_path = token_path
        self.code_verifier = self._get_new_code_verifier()
        self.callback_url = callback_url

    def auth(self):
        """
        If the host, port, and callback_url are all set, then we'll use the web-based authentication
        flow. Otherwise, we'll use the user-input authentication flow.
        
        Returns:
          The token is being returned.
        """
        if [self.host, self.port, self.callback_url].count(None) != 0:
            return self.get_token_user_input()
        else:
            return self.get_token_web()

    def _get_new_code_verifier(self) -> str:
        """
        It generates a random string of 128 characters
        
        Returns:
          A string of 128 characters.
        """
        token = secrets.token_urlsafe(100)
        return token[:128]

    def get_auth_url(self):
        """
        It takes the client_id, code_verifier, client_secret, and callback_url and returns a URL that
        can be used to get an authorization code
        
        Returns:
          The URL for the authorization endpoint.
        """
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "code_challenge": self.code_verifier,
        }
        if self.client_secret is not None:
            params["client_secret"] = self.client_secret
        if self.callback_url is not None:
            params["redirect_uri"] = self.callback_url
        return f"{self.auth_url}?{urlencode(params)}"

    def generate_token(self, authorization_code: str, code_verifier: str) -> dict:
        """
        It takes an authorization code and a code verifier and returns a token
        
        Args:
          authorization_code (str): The authorization code you received from the user.
          code_verifier (str): A random string of 43-128 characters.
        
        Returns:
          A dictionary containing the access token, refresh token, and expiration time.
        """
        url = "https://myanimelist.net/v1/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": authorization_code,
            "code_verifier": code_verifier,
            "redirect_uri": self.callback_url,
            "grant_type": "authorization_code",
        }

        response = requests.post(url, data)
        token = response.json()
        response.close()

        if self.store_token:
            with open(self.token_path, "w") as f:
                json.dump(token, f)
                
        return token

    def get_token_user_input(self) -> str:
        """
        It prints out the auth url, asks the user to visit it, and then asks the user to enter the code
        that is returned to the callback url
        
        Returns:
          The token is being returned.
        """
        print(f"Please visit {self.get_auth_url()}")
        code = input("Please enter the code (callback?code=): ").strip()
        token = self.generate_token(code, self.code_verifier)
        print("Token generated successfully!")
        return token

    def get_token_web(self) -> str:
        """
        It starts a Flask server on a new thread, then opens a browser window to the auth url, and waits
        for the user to authenticate. Once the user authenticates, the server receives the auth code,
        and the function returns the token
        
        Returns:
          The token is being returned.
        """
        global server
        global code
        code = None
        app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.disabled = True
        path = self.callback_url.split("/")[-1]
        print(path)

        @app.route(f"/{path}")
        def auth_code():
            global server
            global code
            code = request.args.get("code")
            return "You can close this window now."

        server = ServerThread(app, self.host, self.port)
        server.start()
        print(f"Please visit {self.get_auth_url()}")
        time = datetime.datetime.now()
        while code is None:
            if (datetime.datetime.now() - time).seconds > 60:
                print("Timeout")
                server.shutdown()
                return
            pass
        server.shutdown()
        return self.generate_token(code, self.code_verifier)