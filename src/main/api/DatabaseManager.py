import os

import dotenv
import pymysql
import logging
from pymysql.cursors import DictCursor
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from main.models.track import Track

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


def clean_string(input_str: str) -> str:
    """
    Encodes the string in UTF-8, replacing invalid characters with '?'.
    Then decodes it back to a Python string so that it is valid UTF-8.
    """
    return input_str.encode("utf-8", errors="replace").decode("utf-8")


class DatabaseManager:
    """
    Handles database interactions for Tracks, Channels, and PlayHistory.
    """

    def __init__(self):
        """
        Initialize the database connection.
        """
        dotenv.load_dotenv()
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_DATABASE")

        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10,
        )

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")

    def _execute_query(
            self,
            query: str,
            params: tuple = (),
            fetchone: bool = False,
            commit: bool = False
    ) -> Optional[object]:
        """
        Private helper method that handles:
          1. Checking (pinging) the connection to keep it alive/reconnect if needed.
          2. Executing the query with the given parameters.
          3. Fetching results if it's a SELECT query (controlled by fetchone).
          4. Committing if it's an INSERT/UPDATE/DELETE (controlled by commit).

        Returns either a single row (dict), a list of rows (list of dicts), or None.
        """
        try:
            self.connection.ping(reconnect=True)

            with self.connection.cursor() as cursor:
                cursor.execute(query, params)

                if commit:
                    self.connection.commit()

                if query.strip().lower().startswith("select"):
                    return cursor.fetchone() if fetchone else cursor.fetchall()

        except pymysql.err.OperationalError as e:
            logger.error(f"OperationalError: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while executing query: {e}")
        return None

    # --- Tracks Table Methods ---

    def add_track(self, spotify_id: str, title: str, artist: str):
        """
        Adds a track to the Tracks table.
        Replaces problematic characters in the title and artist names before inserting.
        """
        title = clean_string(title)
        artist = clean_string(artist)

        query = """
        INSERT INTO Tracks (TrackID, Title, Artist)
        VALUES (%s, %s, %s)
        """
        self._execute_query(query, (spotify_id, title, artist), commit=True)
        logger.info(f"Track '{title}' by '{artist}' added (or attempted) successfully.")

    def get_track_by_id(self, track_id: int) -> Optional[Dict]:
        """
        Retrieves a track by its ID.
        """
        query = "SELECT * FROM Tracks WHERE TrackID = %s"
        return self._execute_query(query, (track_id,), fetchone=True)

    def search_tracks(self, title: Optional[str] = None, artist: Optional[str] = None) -> List[Dict]:
        """
        Searches for tracks by title and/or artist.
        """
        query = "SELECT * FROM Tracks"
        params = []
        if title:
            query += " AND Title LIKE %s"
            params.append(f"%{title}%")
        if artist:
            query += " AND Artist LIKE %s"
            params.append(f"%{artist}%")
        result = self._execute_query(query, tuple(params))
        return result if result else []

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
        self._execute_query(query, (channel_id, name), commit=True)
        logger.info(f"Channel '{name}' with ID '{channel_id}' added successfully.")

    def get_channel_by_id(self, channel_id: int) -> Optional[Dict]:
        """
        Retrieves a channel by its ID.
        """
        query = "SELECT * FROM Channels WHERE ChannelID = %s"
        return self._execute_query(query, (channel_id,), fetchone=True)

    # --- PlayHistory Table Methods ---

    def add_play_history(self, spotify_id: int, channel_id: int):
        """
        Adds an entry to the PlayHistory table.
        """
        query = """
        INSERT INTO PlayHistory (SpotifyID, ChannelID)
        VALUES (%s, %s)
        """
        self._execute_query(query, (spotify_id, channel_id), commit=True)
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
        result = self._execute_query(query, (channel_id,))
        return result if result else []

    def get_latest_track_from_channel(self, channel_id: int) -> Optional[Dict]:
        """
        Retrieves the latest played track for a specific channel.
        """
        query = """
        SELECT SpotifyID FROM PlayHistory
        WHERE ChannelID = %s
        ORDER BY Timestamp DESC
        """
        return self._execute_query(query, (channel_id,), fetchone=True)

    def get_play_history_by_date(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Retrieves play history for a date range.
        """
        query = """
        SELECT * FROM PlayHistory
        WHERE Timestamp BETWEEN %s AND %s
        ORDER BY Timestamp DESC
        """
        result = self._execute_query(query, (start_date, end_date))
        return result if result else []

    def get_channel_id_by_name(self, channel_name: str) -> Optional[int]:
        """
        Retrieves the ChannelID for a given channel name.
        """
        query = "SELECT ChannelID FROM Channels WHERE Name = %s"
        result = self._execute_query(query, (channel_name,), fetchone=True)
        return result["ChannelID"] if result else None

    def get_play_history_one_day_back(self, channel_identifier: str) -> List[Track]:
        """
        Retrieves play history one day back as Track objects for a specific channel.
        Args:
            channel_identifier (str): ChannelID or channel name.
        Returns:
            List[Track]: List of Track objects.
        """
        channel_id = self.get_channel_id_by_name(channel_identifier)
        if not channel_id:
            logger.error(f"Channel '{channel_identifier}' not found.")
            return []

        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        query = """
        SELECT t.TrackID, t.Title, t.Artist
        FROM PlayHistory ph
        JOIN Tracks t ON ph.SpotifyID = t.TrackID
        WHERE ph.ChannelID = %s AND ph.Timestamp BETWEEN %s AND %s
        ORDER BY ph.Timestamp DESC
        """
        results = self._execute_query(query, (channel_id, start_date, end_date))

        tracks = [Track(
            spotify_id=row["TrackID"],
            song_title=row["Title"],
            artist_name=row["Artist"],
        ) for row in results] if results else []

        return tracks