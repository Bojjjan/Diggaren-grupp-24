import pymysql
import logging
from pymysql.cursors import DictCursor
from typing import Optional, List, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

class DatabaseManager:
    """
    Handles database interactions for Tracks, Channels, and PlayHistory.
    """

    def __init__(self, host: str, user: str, password: str, database: str):
        """
        Initialize the database connection.
        """
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor
        )

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")


    # --- Tracks Table Methods ---
    def add_track(self, spotify_id: str, title: str, artist: str):
        """
        Adds a track to the Tracks table.
        """
        query = """
        INSERT INTO Tracks (TrackID, Title, Artist)
        VALUES (%s, %s, %s)
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (spotify_id, title, artist))
            self.connection.commit()
            logger.info(f"Track '{title}' by '{artist}' added successfully.")

    def get_track_by_id(self, track_id: int) -> Optional[Dict]:
        """
        Retrieves a track by its ID.
        """
        query = "SELECT * FROM Tracks WHERE TrackID = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (track_id,))
            return cursor.fetchone()

    def search_tracks(self, title: Optional[str] = None, artist: Optional[str] = None) -> List[Dict]:
        """
        Searches for tracks by title and/or artist.
        """
        query = "SELECT * FROM Tracks WHERE 1=1"
        params = []
        if title:
            query += " AND Title LIKE %s"
            params.append(f"%{title}%")
        if artist:
            query += " AND Artist LIKE %s"
            params.append(f"%{artist}%")
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


    # --- Channels Table Methods ---
    def add_channel(self, name: str):
        """
        Adds a channel to the Channels table.
        """
        query = """
        INSERT INTO Channels (Name)
        VALUES (%s)
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (name,))
            self.connection.commit()
            logger.info(f"Channel '{name}' added successfully.")

    def add_channel_with_id(self, channel_id: int, name: str):
        """
        Adds a channel to the Channels table with a specific ID.
        """
        query = """
        INSERT INTO Channels (ChannelID, Name)
        VALUES (%s, %s)
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (channel_id, name))
            self.connection.commit()
            logger.info(f"Channel '{name}' with ID '{channel_id}' added successfully.")

    def get_channel_by_id(self, channel_id: int) -> Optional[Dict]:
        """
        Retrieves a channel by its ID.
        """
        query = "SELECT * FROM Channels WHERE ChannelID = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (channel_id,))
            return cursor.fetchone()


    # --- PlayHistory Table Methods ---
    def add_play_history(self, spotify_id: int, channel_id: int):
        """
        Adds an entry to the PlayHistory table.
        """
        query = """
        INSERT INTO PlayHistory (SpotifyID, ChannelID)
        VALUES (%s, %s)
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (spotify_id, channel_id))
            self.connection.commit()
            logger.info(f"Play history added for SpotifyID '{spotify_id}' on channel '{channel_id}'")

    def get_play_history_by_channel(self, channel_id: int) -> List[Dict]:
        """
        Retrieves play history for a specific channel.
        """
        query = """
        SELECT * FROM PlayHistory
        WHERE ChannelID = %s
        ORDER BY Timestamp DESC
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (channel_id,))
            return cursor.fetchall()

    def get_latest_track_from_channel(self, channel_id: int) -> List[Dict]:
        """
        Retrieves play history for a specific channel.
        """
        query = """
        SELECT SpotifyID FROM PlayHistory
        WHERE ChannelID = %s
        ORDER BY Timestamp DESC
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (channel_id,))
            return cursor.fetchone()

    def get_play_history_by_date(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Retrieves play history for a date range.
        """
        query = """
        SELECT * FROM PlayHistory
        WHERE Timestamp BETWEEN %s AND %s
        ORDER BY Timestamp DESC
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()
