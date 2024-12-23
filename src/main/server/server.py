import sys
import os
import signal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from flask import Flask, jsonify, Response

from main.api.sveriges_radio_api import SvergiesRadioApi
from main.api.SpotifyAPI import SpotifyAPI
from main.server.top_list_updater import TopListUpdater

app = Flask(__name__)
srAPI = SvergiesRadioApi()
spotifyAPI = SpotifyAPI()
top_list_updater = TopListUpdater()

@app.route("/channels", methods=["GET"])
def get_channels():
    channels = srAPI.get_all_channels()

    if channels is None:
        return "500 : Internal Server Error", 500

    for track in channels:
        track = spotifyAPI.get_album_image_for_track(track)

    return jsonify(channels), 200


@app.route("/")
def hello_world():
    return "<p>Diggaren API!</p>"

def handle_shutdown(signum, frame):
    top_list_updater.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    debug_status = False

    if len(sys.argv) > 1:
        debug_status = True
    
    #top_list_updater.start()

    app.run(debug=debug_status)