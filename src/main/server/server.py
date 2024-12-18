import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from flask import Flask, jsonify, Response

from main.api.sveriges_radio_api import SvergiesRadioApi
from main.api.SpotifyAPI import SpotifyAPI

app = Flask(__name__)
srAPI = SvergiesRadioApi()
spotifyAPI = SpotifyAPI()

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

if __name__ == '__main__':
    app.run(debug=True)