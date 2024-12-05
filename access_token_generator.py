from spotipy.oauth2 import SpotifyOAuth
import os

# Spotify API configuration
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "playlist-modify-public playlist-modify-private"

auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

token_info = auth_manager.get_access_token(as_dict=True)
print("Refresh Token:", token_info['refresh_token'])
