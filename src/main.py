from dotenv import load_dotenv
from src.spotify.SpotifyClient import SpotifyClient
from ytmusicapi import YTMusic
import os


def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


SRC_PATH = os.path.dirname(__file__)
DOTENV_PATH = os.path.join(os.path.join(SRC_PATH, ".."), ".env")
YTMUSIC_BROWSER_FILE = os.path.join(os.path.join(SRC_PATH, ".."), "browser.json")
PLAYLIST_ID = "4tPyVse0VPEs2NwHTsJNPH"
PLAYLIST_NAME = "..."

load_dotenv(DOTENV_PATH)

spotify = SpotifyClient(
    os.getenv("SPOTIFY_BASE_URL"),
    os.getenv("SPOTIFY_CLIENT_ID"),
    os.getenv("SPOTIFY_CLIENT_SECRET")
)

print("Retrieving musics from Spotify...")
musics = spotify.get_playlist_musics(PLAYLIST_ID)

ytmusic = YTMusic(YTMUSIC_BROWSER_FILE)

print("Creating YTMusic playlist...")
playlist_id = ytmusic.create_playlist(PLAYLIST_NAME, PLAYLIST_NAME)

print("Searching musics...")
video_ids = []
for music in musics:
    try:
        video_ids.append(ytmusic.search(music)[0]["videoId"])
    except Exception as e:
        print(f"Music {music} not found: {e}")

chunk_size = 10
for chunk in chunk_list(video_ids, chunk_size):
    try:
        print(f"Adding {len(chunk)} songs to the playlist...")
        ytmusic.add_playlist_items(playlist_id, chunk)
    except Exception as e:
        print(f"Error adding songs to the playlist: {e}")

print("Musics added to the new playlist!")
