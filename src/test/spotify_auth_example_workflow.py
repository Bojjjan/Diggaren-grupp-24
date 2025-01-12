import requests
from flask import Flask, request
import os
from dotenv import load_dotenv
from main.api import SpotifyAuth
from main.api import SpotifyPlaylistManager
from main.api import SpotifyDeveloperDashboardAPI
import threading
import time
import logging
import sys

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

app = Flask(__name__)

authorization_code_storage = {"authorization_code": ""}


@app.route("/callback")
def callback():
    """
    Flask route to handle the authorization callback.
    Captures the authorization code sent by Spotify and stores it.
    """
    code = request.args.get("code")
    if code:
        authorization_code_storage["authorization_code"] = code
        logger.info("Authorization code received.")
    return "Authorization successful. You can close this page."


class FlaskServerThread(threading.Thread):
    """
    Runs the example Flask server in a separate thread to handle Spotify's callback,
    to prevent blocking the main thread.
    """

    def __init__(self, flask_app, port=5000):
        super().__init__(daemon=True)
        self.flask_app = flask_app
        self.port = port

    def run(self):
        """
        Starts the example Flask server.
        """
        self.flask_app.run(port=self.port, use_reloader=False)


def wait_for_authorization_code(storage, timeout=300):
    """
    Waits for the authorization code to be stored, with a timeout.

    Args:
        storage (dict): The storage dictionary for the authorization code.
        timeout (int): Maximum wait time in seconds.

    Raises:
        TimeoutError: If the authorization code is not received within the timeout period.
    """
    start_time = time.time()
    while not storage.get("authorization_code"):
        if time.time() - start_time > timeout:
            raise TimeoutError("Authorization code was not received within the timeout period.")
        time.sleep(1)

def whitelist_user(cookie_header_value: str, email: str, display_name: str):
    """
    Add a user to the Spotify Developer Dashboard allowlist.

    Args:
        cookie_header_value (str): The combined cookie header value.
        email (str): The email address of the user.
        display_name (str): The display name of the user.
    """
    headers = {
        "Content-Type": "application/json",
        "Cookie": cookie_header_value,
    }

    endpoint = "https://developer.spotify.com/dashboard/your_app_id/users"
    payload = {
        "email": email,
        "name": display_name,
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        logger.info(f"User {email} successfully added to the allowlist.")
    else:
        logger.error(f"Failed to add user to allowlist: {response.text}")
        raise Exception(f"Add User to Allowlist Error: {response.status_code}")

if __name__ == "__main__":
    # --- Spotify Authentication Setup ---
    client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:5000/callback")

    spotify_auth = SpotifyAuth(client_id, client_secret, redirect_uri)

    # List of scopes needed; consider adding "user-read-email" if you want to fetch user emails automatically
    scopes = [
        "playlist-modify-public",
        "playlist-modify-private",
        "playlist-read-private",
        # "user-read-email"  <-- If you want to call /me to fetch the user's email
    ]

    # 2) Generate the URL for user authorization
    auth_url = spotify_auth.get_authorization_url(scopes)
    logger.info(f"Visit this URL to authorize: {auth_url}")

    # --- Start Flask Server ---
    server_thread = FlaskServerThread(app)
    server_thread.start()

    try:
        # --- Wait for Authorization Code ---
        wait_for_authorization_code(authorization_code_storage, timeout=300)
        authorization_code = authorization_code_storage.get("authorization_code")
        if not authorization_code:
            logger.error("Authorization code is missing. Exiting.")
            sys.exit(1)
        logger.info("Authorization code successfully captured.")
    except TimeoutError as e:
        logger.error(e)
        sys.exit(1)

    try:
        # --- Exchange Authorization Code for Tokens ---
        spotify_auth.exchange_authorization_code(authorization_code)
        logger.info("Authorization successful.")
    except Exception as e:
        logger.error(f"Error during authorization: {e}")
        sys.exit(1)

    # --- Spotify Playlist Operations ---
    spotify_playlist_manager = SpotifyPlaylistManager(spotify_auth.access_token)

    try:
        playlists = spotify_playlist_manager.get_playlists()
        if playlists:
            logger.info("User Playlists:")
            for playlist in playlists:
                logger.info(f"Playlist Name: {playlist['name']} (ID: {playlist['id']})")
        else:
            logger.info("No playlists found. Please ensure the account has playlists.")
    except Exception as e:
        logger.error(f"Error retrieving playlists: {e}")

    # --- Add User to Developer Dashboard Allowlist ---
    dashboard_api = SpotifyDeveloperDashboardAPI()

    cookie_header_value = dashboard_api.get_cookie_header_value()

    # Example request headers:
    headers = {
        "Content-Type": "application/json",
        "Cookie": cookie_header_value,
    }

    dashboard_api.add_user_to_allowlist("newuser@example.com", "New User")
