import logging
import os
from dotenv import load_dotenv
from src.main.api.DatabaseManager import DatabaseManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def main():
    load_dotenv()

    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_manager = DatabaseManager(host=db_host, user=db_user, password=db_pass, database=db_name)

    channel_name = "P3"
    tracks = db_manager.get_play_history_one_day_back(channel_name)

    if tracks:
        for track in tracks:
            print(f"Track ID: {track.spotify_id}, Title: {track.song_title}, Artist: {track.artist_name}, Duration: {track.duration_ms}, Channel ID: {track.channel_id}")
    else:
        logger.info("No tracks found for the specified channel.")

if __name__ == '__main__':
    main()