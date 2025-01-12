import logging

from main.models.track import Track
from typing import List
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

class SvergiesRadioApi:
    """
    A class to interact with the Sveriges Radio API.

    This class provides methods to retrieve live music and channel information
    from the Sveriges Radio API.
    """

    def __init__(self):
        """
        Initialize the SvergiesRadioApi class.
        """
        self._track_list: List[Track] = []
        self._URL =  "https://api.sr.se/api/v2"
        self._PARAMS = {
            "pagination": "false",
            "format": "JSON"
        }

    def get_all_channels(self):
        """
        Retrieve all channels and their live music information.

        This method clears the current track list, retrieves live music and
        channel information, and returns the updated track list.

        Returns:
            list: A list of Track objects containing channel and live music information.
        """

        try:
            self._track_list.clear()
            self._get_all_live_music()
            self._get_all_channel_information()
        except Exception as e:
            logger.error(f"Error in get_all_channels: {e}", exc_info=True)
        return self._track_list



    def _get_all_channel_information(self):
        """
        Retrieve and update channel information for all tracks.

        This method retrieves channel information from the Sveriges Radio API
        and updates the track list with the retrieved information.
        """
        try:
            response = requests.get((self._URL + "/channels"), params=self._PARAMS)
            response.raise_for_status()
            data = response.json()

            for channel in data["channels"]:
                for track in self._track_list:
                    if track.channel_id == channel["id"]:
                        track.channel_img = channel["image"]
                        track.channel_color = channel["color"]

        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException in _get_all_channel_information: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Error in _get_all_channel_information: {e}", exc_info=True)



    def _get_all_live_music(self):
        """
        Retrieve and update live music information for all channels.

        This method retrieves live music information from the Sveriges Radio API
        and updates the track list with the retrieved information.
        """
        try:
            response = requests.get((self._URL + "/playlists/rightnow"), params=self._PARAMS)
            response.raise_for_status()
            data = response.json()

            try:
                for channel in data["channels"]:
                    skip = False
                    song = channel["playlists"]["playlist"].get("song")
                    if not song: continue

                    if len(self._track_list) > 0:
                        for track in self._track_list:
                            if track.channel_id == channel["id"]: # Look for duplicate id
                                skip = True

                    if not skip:
                        newtrack = Track()

                        newtrack.song_title = song["title"]
                        newtrack.artist_name = song["artist"]
                        newtrack.channel_id = channel["id"]
                        newtrack.channel_name = channel["name"]

                        self._track_list.append(newtrack)
            except Exception as e:
                logger.error(f"Error processing live music data: {e}", exc_info=True)

        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException in _get_all_live_music: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Error in _get_all_live_music: {e}", exc_info=True)







