from main.models.track import Track
from src.main.api.spotify_api import (
  get_album_image_for_song,
  get_album_image_for_track,
  get_album_images_for_tracks,
)
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
  try:
    # Example 1: Retrieve album image using song title and artist name
    song_title = "Genesis"
    artist_name = "Justice"
    image_url = get_album_image_for_song(song_title, artist_name)
    if image_url:
      print(
        f"Album image URL for '{song_title}' by '{artist_name}': {image_url}")
    else:
      print(f"No album image found for '{song_title}' by '{artist_name}'.")

    print("\n" + "-" * 50 + "\n")

    # Example 2: Retrieve album image for a single Track object
    track = Track(song_title="Let It Happen", artist_name="Tame Impala")
    try:
      updated_track = get_album_image_for_track(track)
      print(
          f"Album image for '{updated_track.song_title}' by '{updated_track.artist_name}': {updated_track.album_image}"
      )
    except Exception as e:
      print(f"Error retrieving album image for single track: {e}")

    print("\n" + "-" * 50 + "\n")

    # Example 3: Retrieve album images for multiple Track objects
    track_objects = [
      Track(song_title="21st Century Schizoid Man", artist_name="King Crimson"),
      Track(song_title="Money", artist_name="Pink Floyd"),
      Track(song_title="Sunshine of Your Love", artist_name="Cream"),
    ]
    try:
      updated_tracks = get_album_images_for_tracks(track_objects)
      print("Album images for multiple tracks:")
      for track in updated_tracks:
        print(
            f"{track.song_title} by {track.artist_name}: {track.album_image}"
        )
    except Exception as e:
      print(f"Error retrieving album images for multiple tracks: {e}")

  except Exception as main_error:
    logging.error(f"An unexpected error occurred: {main_error}")
