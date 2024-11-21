from dotenv import load_dotenv
from src.spotify.SpotifyClient import SpotifyClient
import os

SRC_PATH = os.path.dirname(__file__)
DOTENV_PATH = os.path.join(os.path.join(SRC_PATH, ".."), ".env")
YTMUSIC_OAUTH_PATH = os.path.join(os.path.join(SRC_PATH, ".."), "oauth.json")
PLAYLIST_ID = "4tPyVse0VPEs2NwHTsJNPH"
PLAYLIST_NAME = "..."

load_dotenv(DOTENV_PATH)

# spotify = SpotifyClient(
#     os.getenv("SPOTIFY_BASE_URL"),
#     os.getenv("SPOTIFY_CLIENT_ID"),
#     os.getenv("SPOTIFY_CLIENT_SECRET")
# )
#
# musics = spotify.get_playlist_musics(PLAYLIST_ID)
# print("Musics retrieved from Spotify.")