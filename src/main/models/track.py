from dataclasses import dataclass, field, asdict
from typing import Optional, Dict

@dataclass
class Track:
    spotify_id: Optional[str] = None
    duration_ms: Optional[int] = None
    song_title: Optional[str] = None
    album_image: Optional[str] = None
    artist_name: Optional[str] = None
    song_stop: Optional[int] = None
    song_start: Optional[int] = None
    channel_name: Optional[str] = None
    channel_color: Optional[str] = None
    channel_img: Optional[str] = None
    channel_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        """
        Convert the Track object to a dictionary.

        Returns:
            Dict[str, Optional[str]]: A dictionary representation of the Track object.
        """
        return {
            "song": self.song_title,
            "artist": self.artist_name,
            "album_image": self.album_image,
        }

    @classmethod
    def from_dict(cls, track_dict: Dict[str, str]) -> "Track":
        """
        Create a Track object from a dictionary.

        Args:
            track_dict (Dict[str, str]): A dictionary containing track information.

        Returns:
            Track: A new Track object created from the dictionary.
        """
        return cls(
            song_title=track_dict.get("song"),
            artist_name=track_dict.get("artist"),
            album_image=track_dict.get("album_image"),
        )
