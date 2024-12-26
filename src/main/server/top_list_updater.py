import os
import threading
import time
from dotenv import load_dotenv
from main.api.sveriges_radio_api import SvergiesRadioApi
from main.api.DatabaseManager import DatabaseManager
from main.api.SpotifyAPI import SpotifyAPI
from main.models.track import Track


class TopListUpdater:
    def __init__(self):
        self.sveriges_radio_api = SvergiesRadioApi()
        self.stop_event = threading.Event()
        self.thread = None

        load_dotenv()

        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_pass = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")

    
    def update_top_list(self):
        while not self.stop_event.is_set():
            db = DatabaseManager(self.db_host, self.db_user, self.db_pass, self.db_name)
            spotify_api = SpotifyAPI()

            print("TopListUpdater: Fetching Channels")
            sr_channels = self.sveriges_radio_api.get_all_channels()
            for track in sr_channels:

                spotify_api.add_spotify_data_to_track(track)

                if not db.get_channel_by_id(track.channel_id):
                    print("TopListUpdater: Adding channel ", track.channel_id, " added to DB.")

                    db.add_channel_with_id(track.channel_id, track.channel_name)

                if not db.get_track_by_id(track.spotify_id):
                    print(f"TopListUpdater: Adding track '{track.song_title}' by '{track.artist_name}'to "
                          f"'Tracks' table.")

                    db.add_track(spotify_id=track.spotify_id, title=track.song_title, artist=track.artist_name)

                if db.get_latest_track_from_channel(track.channel_id) != track.spotify_id:
                    print(f"TopListUpdater: Adding track '{track.song_title}' by '{track.artist_name}'to "
                          f"'PlayHistory' table.")

                    db.add_play_history(spotify_id=track.spotify_id, channel_id=track.channel_id)

            db.close_connection()
            time.sleep(60)
            
    def start(self):
        self.thread = threading.Thread(target=self.update_top_list)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()