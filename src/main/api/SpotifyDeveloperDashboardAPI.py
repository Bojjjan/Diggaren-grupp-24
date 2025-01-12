import os
import dotenv
import requests
import logging

logging.basicConfig(level=logging.INFO)


class SpotifyDeveloperDashboardAPI:
    """
    Interacts with the Spotify Developer Dashboard API to manage users.
    """

    def __init__(self):
        dotenv.load_dotenv()

        self.app_id = os.getenv("SPOTIFY_APP_ID")
        self.sp_dc = os.getenv("SP_DC")
        self.sp_key = os.getenv("SP_KEY")
        self.sp_t = os.getenv("SP_T")
        self.csrf_token = os.getenv("CSRF_TOKEN")

        self.base_url = "https://developer.spotify.com"

    def add_user_to_allowlist(self, user_email: str, user_name: str):
        endpoint = f"{self.base_url}/dashboard/{self.app_id}/users"

        cookie_header_value = f"sp_dc={self.sp_dc}; sp_key={self.sp_key}; sp_t={self.sp_t}"

        headers = {
            "Content-Type": "application/json",
            "Cookie": cookie_header_value,
        }

        if self.csrf_token:
            headers["x-csrf-token"] = self.csrf_token

        payload = {"email": user_email, "name": user_name}

        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"User {user_email} added.")
        else:
            print(f"Failed to add user. Status: {response.status_code}")
            print("Response:", response.text)

    def get_cookie_header_value(self):
        return f"sp_dc={self.sp_dc}; sp_key={self.sp_key}; sp_t={self.sp_t}"
