import base64
import requests
import logging
from typing import Optional
from urllib.parse import urlencode

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SpotifyAuth:
    """
    Handles Spotify authentication and token management.
    """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        self.token_url = "https://accounts.spotify.com/api/token"
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

    def get_authorization_url(self, scopes: Optional[list] = None) -> str:
        """
        Generate the Spotify authorization URL.

        Args:
            scopes (Optional[list]): List of scopes for the access request.

        Returns:
            str: The authorization URL.
        """
        scope = " ".join(scopes) if scopes else ""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope,
        }
        return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

    def exchange_authorization_code(self, authorization_code: str):
        """
        Exchange the authorization code for an access and refresh token.

        Args:
            authorization_code (str): The authorization code received from Spotify.
        """
        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(self.token_url, headers=headers, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            print("***ACCESS TOKEN***")
            print(self.access_token)
            print("***ACCESS TOKEN***")
            self.refresh_token = tokens["refresh_token"]
            logging.info("Access and refresh tokens successfully retrieved.")
        else:
            logging.error(f"Failed to exchange authorization code: {response.text}")
            raise Exception(f"Authorization Code Exchange Error: {response.status_code}")

    def refresh_access_token(self):
        """
        Refresh the access token using the refresh token.
        """
        if not self.refresh_token:
            raise Exception("No refresh token available. Please authorize again.")

        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}

        response = requests.post(self.token_url, headers=headers, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            logging.info("Access token successfully refreshed.")
        else:
            logging.error(f"Failed to refresh access token: {response.text}")
            raise Exception(f"Token Refresh Error: {response.status_code}")
