# PyMAL

PyMAL is a Python library for interacting with the MyAnimeList API.

This project is still in development.
## Usage

To use this library, you will need to obtain an API Client ID from [https://myanimelist.net/apiconfig](https://myanimelist.net/apiconfig)

Once you have your Client ID, you can create a PyMAL instance like so:

```python
from PyMAL.mal import Client

client = Client(
    client_id="",
    client_secret="",
    host="localhost",
    port=5000,
    callback_url="http://localhost:5000/callback",
    store_token=True,
    user_login=True,
)
```

This will start a temporary server at the specified host and port to receive a callback

You can emit host, port and callback_url to paste the code manually through the console

if you don't need user authentication, you can also set user_login to false

With your PyMAL instance created, you can now start making API calls.

```python
from PyMAL.mal import Client

client = Client(
    client_id="",
    client_secret="",
    host="localhost",
    port=5000,
    callback_url="http://localhost:5000/callback",
    store_token=True,
    user_login=True,
)

user_name = client.get_user()["name"]
print(f"hello {user_name}!")
print(client.search_anime("Lycoris Recoil"))
```

## Todo

- [x]  Authentication
    - [x]  user-input flow
    - [x]  web-callback flow
- [x]  Endpoint Coverage
    - [x]  User
    - [x]  Anime
        - [x]  Get anime list
        - [x]  Get anime details
        - [x]  Get anime ranking
        - [x]  Get seasonal anime
        - [x]  Get suggested anime
    - [x]  User Anime List
        - [x]  Update my anime list status
        - [x]  Delete my anime list item
        - [x]  Get user anime list
    - [ ]  Manga
        - [ ]  Get manga list
        - [ ]  Get manga details
        - [ ]  Get manga ranking
    - [ ]  User Manga List
        - [ ]  Update my manga list status
        - [ ]  Delete my manga list item
        - [ ]  Get user manga list
    - [ ]  Forum
        - [ ]  Get forum boards
        - [ ]  Get forum topics
        - [ ]  Get forum topic detail