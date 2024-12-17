from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Track:
  song_title: str
  artist_name: str
  album_image: Optional[str] = field(default=None)

  def to_dict(self) -> dict:
    return {
      "song": self.song_title,
      "artist": self.artist_name,
      "album_image": self.album_image,
    }

  @classmethod
  def from_dict(cls, track_dict: dict) -> "Track":
    return cls(
        song_title=track_dict["song"],
        artist_name=track_dict["artist"],
        album_image=track_dict.get("album_image"),
    )
