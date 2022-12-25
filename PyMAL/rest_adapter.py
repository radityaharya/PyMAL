import requests


# It takes in a base URL, version, and bearer token, and returns a JSON response from the API
class API(object):
    def __init__(self, base_url:str, version:str, headers:str):
        """
        > This function initializes the class with the base URL, version, and bearer token
        
        Args:
          base_url (str): The base URL of the API.
          version (str): The version of the API you want to use.
          bearer_token (str): This is the token that you get from the API provider.
        """
        self.base_url = base_url
        self.version = version
        self.headers = headers
    
    def request(self, method, endpoint, params = None, data = None)->dict:
        """
        > This function takes in a method, endpoint, params, and data, and returns the JSON response from
        the API
        
        Args:
          method: The HTTP method to use (GET, POST, PUT, DELETE, PATCH)
          endpoint: The endpoint you want to hit.
          params: a dictionary of parameters to be passed to the API
          data: The data to be sent in the request body.
        
        Returns:
          A dictionary of the JSON response from the API.
        """
        url = f'{self.base_url}/{self.version}/{endpoint}'
        
        method = method.upper()
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        if method not in methods:
            raise ValueError(f'{method} is not a valid method')

        r = requests.request(method, url, headers = self.headers, params = params, data = data)

        if r.status_code == 200:
            return r.json()
        else:
            if r.status_code == 401:
                if "The access token expired" in r.headers['WWW-Authenticate']:
                    raise Exception('The access token expired')
                else:
                    raise Exception(f'{r.status_code} - {r.json()}')
            else:
                raise Exception(f'{r.status_code} - {r.json()}')

