from dotenv import load_dotenv
from src.spotify.SpotifyClient import SpotifyClient
from ytmusicapi import YTMusic
from typing import Any
import os
import re


def chunk_list(arr: list[Any], chunk_size: int):
    for i in range(0, len(arr), chunk_size):
        yield arr[i:i + chunk_size]


def preprocess_text(text: str) -> set[str]:
    text = re.sub(r"[^\w\s]", "", text)
    return set(text.lower().split())


def get_text_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0
    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union) * 100


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
i = 0
for music in musics:
    try:
        items = ytmusic.search(music)
        chosen_item = None

        for item in items:
            if item["resultType"] == "song" and "album" in item and item["album"] is not None:
                album_name = item["album"].get("name", "")
                if get_text_similarity(album_name, music) > 60:
                    chosen_item = item
                    break

        if chosen_item is None:
            for item in items:
                if item["resultType"] == "song":
                    chosen_item = item
                    break

        if chosen_item is None and items:
            chosen_item = items[0]

        if chosen_item:
            video_ids.append(chosen_item["videoId"])
        else:
            print(f"No suitable item found for {music}")
    except Exception as e:
        print(f"Music {music} not found: {e}")

    i += 1
    print(f"{i}/{len(musics)}")

chunk_size = 50
for chunk in chunk_list(video_ids, chunk_size):
    try:
        print(f"Adding {len(chunk)} songs to the playlist...")
        ytmusic.add_playlist_items(playlist_id, chunk)
    except Exception as e:
        print(f"Error adding songs to the playlist: {e}")

print("Musics added to the new playlist!")
