import os
import base64
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional
import logging

from main.models.track import Track

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()


def _extract_images_from_items(items: List[Dict], key: str = "album") -> Optional[str]:
    """
    Extract images from a list of items (album or artist).

    Args:
        items (List[Dict]): A list of Spotify API response items.
        key (str): The key to extract images from (default is "album").

    Returns:
        Optional[str]: The URL of the largest image, or None if not found.
    """
    if not items:
        return None

    images = items[0].get(key, {}).get("images", [])
    return images[0]["url"] if images else None


def _extract_album_image_url(track_response: Dict) -> Optional[str]:
    """
    Extract the album image URL from a Spotify track response.

    Args:
        track_response (Dict): JSON response from the Spotify API.

    Returns:
        Optional[str]: URL of the album image if available, else None.
    """
    return _extract_images_from_items(track_response.get("tracks", {}).get("items", []))


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
        self.SPOTIFY_ARTIST_URL = "https://api.spotify.com/v1/artists"
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
            return response.json()
        else:
            logging.error(
                f"Spotify API request failed: {response.status_code} - {response.text}"
            )
            return None

    def _extract_genres(self, response: Dict) -> Optional[List[str]]:
        """
        Extract genres from a Spotify API response.

        Args:
            response (Dict): JSON response from the Spotify API.

        Returns:
            Optional[List[str]]: A list of genres or None if not found.
        """
        tracks = response.get("tracks", {}).get("items", [])
        if tracks:
            artist_id = tracks[0].get("artists", [{}])[0].get("id")
            if artist_id:
                artist_response = self._make_spotify_request(f"{self.SPOTIFY_ARTIST_URL}/{artist_id}", {})
                if artist_response:
                    return artist_response.get("genres", [])
        return None

    def get_album_image_for_song(self, song_title: str, artist_name: str) -> Optional[str]:
        """
        Retrieve the album image URL for a song and artist.
        If no album image is found, fallback to an artist image.

        Args:
            song_title (str): The song title.
            artist_name (str): The artist's name.

        Returns:
            Optional[str]: URL of the album or artist image, or None if not found.
        """
        search_params = {
            "q": f"track:{song_title} artist:{artist_name}",
            "type": "track",
            "limit": 1,
        }
        response = self._make_spotify_request(self.SPOTIFY_SEARCH_URL, search_params)
        if response:
            tracks = response.get("tracks", {}).get("items", [])
            if tracks:
                album_images = tracks[0].get("album", {}).get("images", [])
                if album_images:
                    return album_images[0]["url"]

                artist_id = tracks[0].get("artists", [{}])[0].get("id")
                if artist_id:
                    if not artist_id.strip():
                        logging.warning("Artist ID is empty or invalid. Skipping fallback to artist image.")
                        return None
                    return self.get_artist_image(artist_id)

            return None

    def get_album_image_for_track(self, track: Track) -> Track:
        """
        Retrieve the album image for a given Track object and update it.
        If no album image is found, fallback to an artist image.

        Args:
            track (Track): A Track object containing song title and artist name.

        Returns:
            Track: The updated Track object with the album_image attribute set.
        """
        album_image = self.get_album_image_for_song(track.song_title, track.artist_name)
        if not album_image:
            logging.warning(
                f"No album image found for '{track.song_title}' by '{track.artist_name}', using fallback."
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

    def get_genre_for_track(self, track: Track) -> Optional[List[str]]:
        """
        Retrieve the genre for a given Track object.

        Args:
            track (Track): A Track object containing song title and artist name.

        Returns:
            Optional[List[str]]: A list of genres or None if not found.
        """
        search_params = {
            "q": f"track:{track.song_title} artist:{track.artist_name}",
            "type": "track",
            "limit": 1,
        }
        response = self._make_spotify_request(self.SPOTIFY_SEARCH_URL, search_params)
        genres = self._extract_genres(response)
        if genres:
            return genres
        logging.warning(f"No genres found for '{track.song_title}' by '{track.artist_name}'.")
        return None

    def get_artist_image(self, artist_id: str) -> Optional[str]:
        """
        Retrieve the image for a given artist from Spotify.

        Args:
            artist_id (str): The Spotify artist ID.

        Returns:
            Optional[str]: URL of the artist's image, or None if not found.
        """
        endpoint = f"{self.SPOTIFY_ARTIST_URL}/{artist_id}"
        response = self._make_spotify_request(endpoint, {})
        return _extract_images_from_items([response], key="images") if response else None

    def get_genre_for_song(self, song_title: str, artist_name: str) -> Optional[List[str]]:
        """
        Retrieve the genre for a song and artist.

        Args:
            song_title (str): The song title.
            artist_name (str): The artist's name.

        Returns:
            Optional[List[str]]: A list of genres or None if not found.
        """
        search_params = {
            "q": f"track:{song_title} artist:{artist_name}",
            "type": "track",
            "limit": 1,
        }
        response = self._make_spotify_request(self.SPOTIFY_SEARCH_URL, search_params)
        genres = self._extract_genres(response)
        if genres:
            return genres
        logging.warning(f"No genres found for '{song_title}' by '{song_title}'.")
        return None

    def add_spotify_data_to_track(self, track: Track) -> Track:
        """
        Add the Spotify ID to a Track object.

        Args:
            track (Track): A Track object containing song title and artist name.

        Returns:
            Track: The updated Track object with the Spotify ID attribute set.
        """
        spotify_data = self.fetch_spotify_data_for_track(track)
        if not spotify_data:
            track.spotify_id = track.song_title + track.artist_name
            return track

        track.spotify_id = spotify_data.get("id")
        if track.spotify_id:
            logging.info(f"Spotify ID added for '{track.song_title}' by '{track.artist_name}': {track.spotify_id}")
        else:
            logging.warning(f"No Spotify ID found for '{track.song_title}' by '{track.artist_name}'.")

        return track

    def fetch_spotify_data_for_track(self, track: Track) -> Optional[Dict]:
        """
        Fetch Spotify data for a given track.

        Args:
            track (Track): A Track object containing song title and artist name.

        Returns:
            Optional[Dict]: The Spotify track data dictionary or None if not found.
        """
        search_params = {
            "q": f'track:"{track.song_title}" artist:"{track.artist_name}"',
            "type": "track",
            "limit": 1,
        }
        response = self._make_spotify_request(self.SPOTIFY_SEARCH_URL, search_params)

        if not response:
            logging.error(f"Failed to retrieve data for '{track.song_title}' by '{track.artist_name}'.")
            return None

        tracks = response.get("tracks", {}).get("items", [])
        if not tracks:
            logging.warning(f"No tracks found for '{track.song_title}' by '{track.artist_name}'.")
            return None

        logging.debug(f"Spotify API response for '{track.song_title}': {tracks[0]}")
        return tracks[0]