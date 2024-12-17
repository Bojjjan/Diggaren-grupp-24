import os
import base64
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional
import logging

from main.models.track import Track

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

class SpotifyAPI:
    """
    A class to interact with the Spotify API for retrieving track and album information.
    """

    def __init__(self):
        """
        Initialize the SpotifyAPI instance with API credentials and endpoints.
        """
        self.SPOTIFY_TOKEN_URL = os.getenv("SPOTIFY_TOKEN_URL", "https://accounts.spotify.com/api/token")
        self.SPOTIFY_SEARCH_URL = os.getenv("SPOTIFY_SEARCH_URL", "https://api.spotify.com/v1/search")
        self.CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
        self._cached_token: Optional[str] = None

    def _get_spotify_token(self) -> str:
        """
        Retrieve a Spotify access token using client credentials.

        Returns:
            str: A valid Spotify access token.
        """
        if self._cached_token:
            return self._cached_token

        client_credentials = f"{self.CLIENT_ID}:{self.CLIENT_SECRET}"
        auth_header = base64.b64encode(client_credentials.encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(self.SPOTIFY_TOKEN_URL, headers=headers, data=data)

        if response.status_code == 200:
            self._cached_token = response.json().get("access_token")
            logging.info("Spotify token successfully retrieved.")
            return self._cached_token
        else:
            logging.error(
                f"Failed to retrieve Spotify token: {response.status_code} - {response.text}"
            )
            raise Exception(
                f"Failed to retrieve Spotify token: {response.status_code} - {response.text}"
            )

    def _make_spotify_request(self, endpoint: str, params: Dict[str, str]) -> Optional[Dict]:
        """
        Make an authenticated GET request to the Spotify API.

        Args:
            endpoint (str): The Spotify API endpoint.
            params (Dict[str, str]): Query parameters.

        Returns:
            Optional[Dict]: JSON response data or None if request fails.
        """
        token = self._get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            logging.info(f"Spotify API request successful for params: {params}")
            return response.json()
        else:
            logging.error(
                f"Spotify API request failed: {response.status_code} - {response.text}"
            )
            return None

    def _extract_album_image_url(self, track_response: Dict) -> Optional[str]:
        """
        Extract the album image URL from a Spotify track response.

        Args:
            track_response (Dict): JSON response from the Spotify API.

        Returns:
            Optional[str]: URL of the album image if available, else None.
        """
        tracks = track_response.get("tracks", {}).get("items", [])
        if tracks:
            album_images = tracks[0].get("album", {}).get("images", [])
            if album_images:
                return album_images[0]["url"]
        return None

    def get_album_image_for_song(self, song_title: str, artist_name: str) -> Optional[str]:
        """
        Retrieve the album image URL for a song and artist.

        Args:
            song_title (str): The song title.
            artist_name (str): The artist's name.

        Returns:
            Optional[str]: URL of the album image, or None if not found.
        """
        search_params = {
            "q": f"track:{song_title} artist:{artist_name}",
            "type": "track",
            "limit": 1,
        }
        response = self._make_spotify_request(self.SPOTIFY_SEARCH_URL, search_params)
        if response:
            return self._extract_album_image_url(response)
        return None

    def get_album_image_for_track(self, track: Track) -> Track:
        """
        Retrieve the album image for a given Track object and update it.

        Args:
            track (Track): A Track object containing song title and artist name.

        Returns:
            Track: The updated Track object with the album_image attribute set.
        """
        album_image = self.get_album_image_for_song(track.song_title, track.artist_name)
        if album_image:
            logging.info(
                f"Album image found for '{track.song_title}' by '{track.artist_name}'."
            )
        else:
            logging.warning(
                f"No album image found for '{track.song_title}' by '{track.artist_name}'."
            )
        track.album_image = album_image
        return track

    def get_album_images_for_tracks(self, track_objects: List[Track]) -> List[Track]:
        """
        Retrieve album image URLs for a list of Track objects and update them.

        Args:
            track_objects (List[Track]): A list of Track objects.

        Returns:
            List[Track]: The list of Track objects with updated album_image attributes.
        """
        for track in track_objects:
            self.get_album_image_for_track(track)
        return track_objects
