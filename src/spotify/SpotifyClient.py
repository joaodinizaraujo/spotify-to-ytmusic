import requests
import base64
from datetime import datetime


def generate_token(client_id: str, client_secret: str) -> str:
    url = "https://accounts.spotify.com/api/token"
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = "grant_type=client_credentials"

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"Error during Spotify token generation: {response.status_code}, {response.text}")

    data = response.json()
    return data["access_token"]


class SpotifyClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url
        self.token = generate_token(client_id, client_secret)

    def get_playlist_musics(self, playlist_id: str) -> list[str]:
        offset = 0
        limit = 100
        track_names = []

        url = f"{self.base_url}/playlists/{playlist_id}/tracks"
        params = {
            "fields": "items(track(name, album(name, release_date, artists(name)))),next",
            "limit": limit,
            "offset": offset
        }
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Spotify request error taking musics: {response.status_code}, {response.text}")
                break

            data = response.json()
            for item in data["items"]:
                artist_name = item["track"]["album"]["artists"][0]["name"] if len(item["track"]["album"]["artists"]) > 0 else ""
                music_name = item["track"]["name"]
                album_name = item["track"]["album"]["name"]
                try:
                    release_year = datetime.strptime(item["track"]["album"]["release_date"], "%Y-%m-%d").year
                except (ValueError, TypeError):
                    release_year = item["track"]["album"]["release_date"] if item["track"]["album"]["release_date"] is not None else ""

                track_name = f"{artist_name} - {music_name} - {album_name} {release_year}"
                track_names.append(track_name)

            if not data.get("next"):
                break

            url = data["next"]
            offset += limit

        return track_names
