from flask import Flask, request
import os
from dotenv import load_dotenv
from main.api.SpotifyAuth import SpotifyAuth
from main.api.SpotifyPlaylistManager import SpotifyPlaylistManager
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
    Runs the example Flask server in a separate thread to handle Spotify's callback, to prevent blocking main thread.
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


if __name__ == "__main__":
    # --- Spotify Authentication Setup ---
    # Initialize SpotifyAuth to handle authentication and tokens
    client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:5000/callback")
    spotify_auth = SpotifyAuth(client_id, client_secret, redirect_uri)

    # Generate the URL for user authorization
    scopes = ["playlist-modify-public", "playlist-modify-private"]
    auth_url = spotify_auth.get_authorization_url(scopes)
    logger.info(f"Visit this URL to authorize: {auth_url}")

    # --- Start Flask Server ---
    # Start a separate thread to run the Flask server for the authorization callback
    server_thread = FlaskServerThread(app)
    server_thread.start()

    try:
        # --- Wait for Authorization Code ---
        # Wait for the user to complete the authorization process
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
        # Exchange the captured code for an access and refresh token
        spotify_auth.exchange_authorization_code(authorization_code)
        logger.info("Authorization successful.")
    except Exception as e:
        logger.error(f"Error during authorization: {e}")
        sys.exit(1)

    # --- Spotify Playlist Operations ---
    # Initialize SpotifyPlaylistManager with the access token
    spotify_playlist_manager = SpotifyPlaylistManager(spotify_auth.access_token)

    # Example: Add tracks to a Spotify playlist
    playlist_id = "your_playlist_id_here"  # Replace with your Spotify playlist ID
    track_uris = ["spotify:track:track_id_1", "spotify:track:track_id_2"]  # Replace with Spotify track URIs

    try:
        # Add tracks to the playlist
        spotify_playlist_manager.add_to_playlist(playlist_id, track_uris)
        logger.info("Tracks successfully added to playlist.")
    except Exception as e:
        logger.error(f"Error adding tracks to playlist: {e}")
        sys.exit(1)

    logger.info("Process complete. Exiting...")
    sys.exit(0)
