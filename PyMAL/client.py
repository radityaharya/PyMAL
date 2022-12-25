import json
import os
from .rest_adapter import API
from .auth import Auth
from .modules.user import User
from .modules.anime import Anime

class Client(API, User, Anime):
    def __init__(
        self,
        client_id: str,
        client_secret=None,
        user_login:bool = True,
        host: str = None,
        port: int = None,
        callback_url: str = None,
        store_token=True,
        token_path="token.json",
        
    ):
        """
        > This function initializes the class with the client ID, client secret, and token path
        
        if user_login is set to False, the client will not attempt to login the user instead it will use client_id in the  X-MAL-CLIENT-ID request header to authenticate the request with a limited scope.
        
        client_secret can be set to None if you did not set "web" as the "App Type" in the MAL API config.
        
        if host and or port are not specified, the client will use console input to retrieve authoirzation code
        
        else, the client will use the the host and port to retrieve authoirzation code via callback url

        Args:
          client_id (str): The client ID of the API.
          client_secret (str): The client secret of the API.
          host (str): The host to use for the callback url.
          port (int): The port to use for the callback url.
          callback_url (str): The callback url set in the MAL apiconfig.
          token_path (str): The path to the token file.
          store_token (bool): Whether or not to store the token in the token file.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host
        self.port = port
        self.callback_url = callback_url
        self.token_path = token_path
        self.store_token = store_token
        
        if user_login:
            self.headers = {"Authorization": f"Bearer {self.get_token()['access_token']}"}
        else:
            self.headers = {"X-MAL-CLIENT-ID": self.client_id}
        
        self.api_call = API(base_url="https://api.myanimelist.net", version="v2", headers=self.headers)
        self.anime_fields = [
            "id",
            "title",
            "main_picture",
            "alternative_titles",
            "start_date",
            "end_date",
            "synopsis",
            "mean",
            "rank",
            "popularity",
            "num_list_users",
            "num_scoring_users",
            "nsfw",
            "created_at",
            "updated_at",
            "media_type",
            "status",
            "genres",
            "my_list_status",
            "num_episodes",
            "start_season",
            "broadcast",
            "source",
            "average_episode_duration",
            "rating",
            "pictures",
            "background",
            "related_anime",
            "related_manga",
            "recommendations",
            "studios",
            "statistic",
        ]
    
    def get_token(self):
        """
        If the token path exists, open the file and return the token. If it doesn't exist, return the
        auth function
        
        Returns:
          The token is being returned.
        """
        if self.token_path is not None:
          if os.path.exists(self.token_path):
              with open(self.token_path, "r") as file:
                  token = json.load(file)
                  return token
        return Auth(self.client_id, self.client_secret, self.host, self.port, self.callback_url, self.store_token, self.token_path).auth()
