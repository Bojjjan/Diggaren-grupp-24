import sys
import os
import signal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from flask import Flask, jsonify, Response, request
from flask_cors import CORS

from main.api.sveriges_radio_api import SvergiesRadioApi
from main.api.SpotifyAPI import SpotifyAPI
from main.server.history_updater import HistoryUpdater
from main.api.SpotifyPlaylistManager import SpotifyPlaylistManager
from main.api.DatabaseManager import DatabaseManager

app = Flask(__name__)
CORS(app)
srAPI = SvergiesRadioApi()
spotifyAPI = SpotifyAPI()
history_updater = HistoryUpdater()



@app.route("/channels", methods=["GET"])
def get_channels():
    """
    Returns information about all channels that are currently playing music in a JSON format.
    """

    channels = srAPI.get_all_channels()

    if channels is None:
        return "500 : Internal Server Error", 500

    for track in channels:
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

    data = request.json
    auth_code = data.get("auth_code")

    spm = SpotifyPlaylistManager(auth_code)
    playlists = spm.get_playlists()

    if not auth_code:
        return "400: Authorization code is required.", 400

    return jsonify(playlists), 200

@app.route("/add_song_to_playlist", methods=["POST"])
def add_song_to_playlist():

    """
    Adds a song to the selected playlist on the users spotify account.

    Requires a spotify authentication code.
    """

    data = request.json
    auth_code = data.get("auth_code")
    track_uris = data.get("track_uris")
    playlist_id = data.get("playlist_idd")

    if not auth_code:
        return "400: Authorization code is required.", 400

    spm = SpotifyPlaylistManager(auth_code)
    spm.add_to_playlist(playlist_id, track_uris)

    return 200

@app.route("/")
def hello_world():
    return "<p>Diggaren API!</p>", 200

def handle_shutdown(signum, frame):
    history_updater.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    debug_status = False

    if len(sys.argv) > 1:
        debug_status = True
    
    history_updater.start()

    app.run(debug=debug_status, port=5001)