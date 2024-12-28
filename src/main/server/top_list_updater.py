import os
import threading
import time
from dotenv import load_dotenv, find_dotenv
from main.api.sveriges_radio_api import SvergiesRadioApi
from main.api.DatabaseManager import DatabaseManager
from main.api.SpotifyAPI import SpotifyAPI
from main.models.track import Track

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TopListUpdater:
    def __init__(self):
        self.sveriges_radio_api = SvergiesRadioApi()
        self.stop_event = threading.Event()
        self.thread = None

        load_dotenv(find_dotenv())

        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_pass = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")

    
    def update_top_list(self):
        while not self.stop_event.is_set():
            db = None
            try:
                db = DatabaseManager(self.db_host, self.db_user, self.db_pass, self.db_name)
                spotify_api = SpotifyAPI()

                logger.info("TopListUpdater: Fetching channels from Sveriges Radio...")
                sr_channels = self.sveriges_radio_api.get_all_channels()

                for track in sr_channels:

                    spotify_api.add_spotify_data_to_track(track)

                    channel = db.get_channel_by_id(track.channel_id)
                    if not channel:
                        logger.info(f"TopListUpdater: Adding channel with ID '{track.channel_id}'.")
                        db.add_channel_with_id(track.channel_id, track.channel_name)

                    existing_track = db.get_track_by_id(track.spotify_id)
                    if not existing_track:
                        logger.info(f"TopListUpdater: Adding new track '{track.song_title}' "
                                    f"by '{track.artist_name}' to 'Tracks'.")
                        db.add_track(
                            spotify_id=track.spotify_id,
                            title=track.song_title,
                            artist=track.artist_name
                        )

                    latest_in_channel = db.get_latest_track_from_channel(track.channel_id)

                    if not latest_in_channel or latest_in_channel.get("SpotifyID") != track.spotify_id:
                        logger.info(f"TopListUpdater: Adding to 'PlayHistory' => track '{track.song_title}' "
                                    f"by '{track.artist_name}'.")
                        db.add_play_history(track.spotify_id, track.channel_id)

            except Exception as e:
                logger.error(f"TopListUpdater: An error occurred: {e}", exc_info=True)
            finally:
                if db is not None:
                    db.close_connection()

            time.sleep(60)

    def start(self):
        self.thread = threading.Thread(target=self.update_top_list, name="TopListUpdaterThread")
        self.thread.start()
        logger.info("TopListUpdater: Thread started.")

    def stop(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()
        logger.info("TopListUpdater: Thread stopped.")