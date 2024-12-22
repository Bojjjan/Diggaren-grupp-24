import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SpotifyPlaylistManager:
    """
    Manages Spotify playlists and track operations.
    """

    def __init__(self, access_token: str):
        self.api_base_url = "https://api.spotify.com/v1"
        self.access_token = access_token

    def add_to_playlist(self, playlist_id: str, track_uris: list):
        """
        Add tracks to a playlist.

        Args:
            playlist_id (str): The Spotify playlist ID.
            track_uris (list): A list of Spotify track URIs to add.
        """
        if not self.access_token:
            raise Exception("Access token is not available. Please authorize first.")

        endpoint = f"{self.api_base_url}/playlists/{playlist_id}/tracks"
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        data = {"uris": track_uris}

        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code == 201:
            logging.info("Tracks successfully added to playlist.")
        else:
            logging.error(f"Failed to add tracks to playlist: {response.text}")
            raise Exception(f"Add to Playlist Error: {response.status_code}")

    @staticmethod
    def generate_link(spotify_id: str, type_: str = "track") -> str:
        """
        Generate a Spotify link for a track or artist.

        Args:
            spotify_id (str): The Spotify ID of the track or artist.
            type_ (str): The type of Spotify entity ("track" or "artist").

        Returns:
            str: A Spotify link for the given entity.
        """
        if not spotify_id.strip():
            raise ValueError("Spotify ID must not be empty.")
        if type_ not in ["track", "artist"]:
            raise ValueError("Type must be 'track' or 'artist'.")
        return f"https://open.spotify.com/{type_}/{spotify_id}"
