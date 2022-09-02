import unittest
from mal.client import Client
from mal.auth import Auth
import os

MAL_CLIENT_ID = os.environ["MAL_CLIENT_ID"]
MAL_CLIENT_SECRET = os.environ["MAL_CLIENT_SECRET"]
MAL_HOST = "0.0.0.0"
MAL_PORT = 5000
MAL_CALLBACK_URL = "http://localhost:5000/callback"
MAL_TOKEN_PATH = "TEST.json"

TEST_ANIME_ID = 50709
TEST_ANIME_TITLE = "Lycoris Recoil"

class TestClient(unittest.TestCase):
    def test_get_token_web(self):
        auth = Auth(
            client_id=MAL_CLIENT_ID,
            client_secret=MAL_CLIENT_SECRET,
            host=MAL_HOST,
            port=MAL_PORT,
            callback_url=MAL_CALLBACK_URL,
            store_token=False,
        )
        token = auth.get_token_web()
        self.assertTrue(token)
    
    def test_get_token_user_input(self):
        auth = Auth(
            client_id=MAL_CLIENT_ID,
            client_secret=MAL_CLIENT_SECRET,
            host=MAL_HOST,
            port=MAL_PORT,
            callback_url=MAL_CALLBACK_URL,
            store_token=False,
        )
        token = auth.get_token_user_input()
        self.assertTrue(token)
    
    def test_get_user(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        user = client.get_user()
        self.assertEqual(type(user), dict)

    def test_search_anime(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        anime = client.search_anime(TEST_ANIME_TITLE)
        self.assertEqual(type(anime), list)
        
    def test_get_anime_details(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        anime = client.get_anime_details(TEST_ANIME_ID)
        self.assertEqual(type(anime), dict)
    
    def test_get_anime_ranking(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        anime = client.get_anime_ranking()
        self.assertEqual(type(anime), list)
    
    def test_get_seasonal_anime(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        anime = client.get_seasonal_anime()
        self.assertEqual(type(anime), list)
    
    def test_get_suggested_anime(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        anime = client.get_suggested_anime()
        self.assertEqual(type(anime), list)
    
    def test_get_user_anime_list(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        anime = client.get_user_anime_list()
        self.assertEqual(type(anime), list)
    
    def test_update_user_anime_list(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        anime = client.update_user_anime_list(17619, status="completed")
        self.assertEqual(type(anime), dict)
    
    def test_delete_user_anime_list(self):
        client = Client(MAL_CLIENT_ID, MAL_CLIENT_SECRET, token_path=MAL_TOKEN_PATH)
        anime = client.delete_user_anime_list(17619)
        print(type(anime))
        self.assertEqual(type(anime), list)

if __name__ == "__main__":
    unittest.main()