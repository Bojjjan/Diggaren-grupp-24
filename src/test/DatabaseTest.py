import logging

from src.main.api.DatabaseManager import DatabaseManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def main():

    db_manager = DatabaseManager()

    channel_name = "P3"
    tracks = db_manager.get_play_history_one_day_back(channel_name)

    if tracks:
        for track in tracks:
            print(f"Track ID: {track.spotify_id}, Title: {track.song_title}, Artist: {track.artist_name}, Duration: {track.duration_ms}, Channel ID: {track.channel_id}")
    else:
        logger.info("No tracks found for the specified channel.")

if __name__ == '__main__':
    main()