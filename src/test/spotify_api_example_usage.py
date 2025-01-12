from main.models.track import Track
from src.main.api.SpotifyAPI import SpotifyAPI

if __name__ == "__main__":
    spotify_api = SpotifyAPI()

    # Example 1: Retrieve album image using song title and artist name
    song_title = "Genesis"
    artist_name = "Justice"
    image_url = spotify_api.get_album_image_for_song(song_title, artist_name)
    print(f"Album image URL for '{song_title}' by '{artist_name}': {image_url}")

    # Example 2: Retrieve album image for a single Track object
    track = Track(song_title="Imagine", artist_name="John Lennon")
    updated_track = spotify_api.get_album_image_for_track(track)
    print(f"Updated Track: {updated_track}")

    # Example 3: Retrieve album images for multiple Track objects
    track_objects = [
        Track(song_title="Last Christmas", artist_name="Wham!"),
        Track(song_title="Money", artist_name="Pink Floyd"),
        Track(song_title="Sunshine of Your Love", artist_name="Cream"),
    ]
    updated_tracks = spotify_api.get_album_images_for_tracks(track_objects)
    for track in updated_tracks:
        print(f"{track.song_title} by {track.artist_name}: {track.album_image}")