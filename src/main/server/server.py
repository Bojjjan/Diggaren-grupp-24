import sys
import os
import signal
import time
import base64
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from flask import Flask, jsonify, Response, request, session
from flask_cors import CORS
from flask import render_template

from dotenv import load_dotenv

from main.api.sveriges_radio_api import SvergiesRadioApi
from main.api.SpotifyAPI import SpotifyAPI
from main.server.history_updater import HistoryUpdater
from main.api.SpotifyPlaylistManager import SpotifyPlaylistManager
from main.api.DatabaseManager import DatabaseManager
from main.api.SpotifyAuth import SpotifyAuth


app = Flask(__name__)
CORS(app)
srAPI = SvergiesRadioApi()
spotifyAPI = SpotifyAPI()
history_updater = HistoryUpdater()
temp_code = None
load_dotenv()


@app.route("/channels", methods=["GET"])
def get_channels():
    """
    Returns information about all channels that are currently playing music in a JSON format.
    """

    channels = srAPI.get_all_channels()

    if channels is None:
        return "500 : Internal Server Error", 500

    for track in channels:
        track = spotifyAPI.add_spotify_data_to_track(track)
        track = spotifyAPI.get_album_image_for_track(track)

    return jsonify(channels), 200

@app.route("/channels/<int:channel_id>", methods=["GET"])
def get_channel_history(channel_id):

    """
    Returns the song history in JSON format of the channel that was given as input parameter.
    """

    dbm = DatabaseManager()
    tracks = dbm.get_play_history_one_day_back(channel_id)

    return jsonify(tracks), 200

@app.route("/user_playlists", methods=["GET"])
def get_user_spotify_playlists():

    """
    Returns a list of all the playlists on the users spotify account in a JSON format.

    Requires a spotify authentication code.
    """

    access_token = request.args.get("access_token")

    if not access_token:
        return "400: Access token is required.", 400

    spm = SpotifyPlaylistManager(access_token)
    playlists = spm.get_playlists()

    return jsonify(playlists), 200

@app.route("/add_song_to_playlist", methods=["POST"])
def add_song_to_playlist():

    """
    Adds a song to the selected playlist on the users spotify account.

    Requires a spotify authentication code.
    """

    access_token = request.args.get("access_token")
    track_uris = request.args.get("track_uris")
    playlist_id = request.args.get("playlist_id")

    track_list = []
    track_list.append(track_uris)

    print("ACCESS TOKEN: ",access_token)
    print("TRACK: ",track_uris)
    print("PLAYLIST: ",playlist_id)

    if not access_token:
        return "400: Access token is required.", 400

    spm = SpotifyPlaylistManager(access_token)
    spm.add_to_playlist(playlist_id, track_list)

    return "Track successfully added.", 201

@app.route("/get_code",  methods=["GET"])
def get_code():
    """
    This method is only used when a user is logging into their Spotify account. 
    It's called directly after /callback to send back the user token.
    """

    global temp_code
    counter = 0
    while temp_code is None and counter < 10:
        time.sleep(1)
        print("Waiting for the variable to be declared...")
        counter += 1


    return {"code": temp_code}

@app.route("/callback",  methods=["GET"])
def callback():
    """
    This API call is only used when a user is logging into their Spotify account. It's used by the spotify login API
    as a callback to when the user has logged in. It saves the users token in the variable temp_code which is then
    fetched by the website via /get_code.
    """

    global temp_code
    temp_code = None
    code = request.args.get('code')
    if not code:
        return 'Authorization code not found', 400

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{os.getenv("SPOTIFY_CLIENT_ID")}:{os.getenv("SPOTIFY_CLIENT_SECRET")}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "http://localhost:5000/callback"
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        return f'Error fetching access token: {response.text}', 400

    token_data = response.json()
    access_token = token_data.get('access_token')
    if not access_token:
        return 'Access token not found in response =(', 400

    temp_code = access_token
    return render_template("access_granted.html"), 200

@app.route("/spotify_url", methods=["GET"])
def get_spotify_url():
    """
    This function is used to get a spotify login url.
    """


    client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "https://diggaren.tech/callback")

    spotify_auth = SpotifyAuth(client_id, client_secret, redirect_uri)

    scopes = [
        "playlist-modify-public",
        "playlist-modify-private",
        "playlist-read-private",
    ]

    auth_url = spotify_auth.get_authorization_url(scopes)

    return jsonify(auth_url), 200

@app.route("/client_id", methods=["GET"])
def get_client_id():
    """
    This function is used to get the Spotify clientID.
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID", "")

    return {"client_id": client_id}, 200


@app.route("/")
def hello_world():
    return "<p>Diggaren API!</p>", 200

def handle_shutdown(signum, frame):
    """
    Handles the shutdown of the server by stopping the history_updater thread so the server stops correctly.
    """
    history_updater.stop()
    sys.exit(0)


    """
    This code handles the startup of the server. It also starts the history_updater thread. 
    """
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    debug_status = False

    if len(sys.argv) > 1:
        debug_status = True
    
    history_updater.start()

    app.run(debug=debug_status, port=5000)