from main.models import track
from main.models.track import Track
from datetime import datetime, timedelta
from typing import List
import requests


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

        self._track_list.clear()
        self._get_all_live_music()
        self._get_all_channel_information()
        return self._track_list


    def get_channel_music_history(self, channel_id):
        """
        Retrieve the music history for a specific channel.

        This method retrieves the music history for the specified channel
        within the current day.

        Args:
            channel_id (int): The ID of the channel.

        Returns:
            list: A list of Track objects containing the music history for the channel.
        """
        music_history_list = []
        start_date = (datetime.now().strftime('%Y-%m-%d'))
        end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        start_date = (start_date+"T00:00:00Z")
        end_date = (end_date+"T00:00:00Z")
        params = {
            "pagination":"false",
            "format":"JSON",
            "id":channel_id,
            "startdatetime":start_date,
            "endDateTime":end_date
        }

        try:
            response = requests.get((self._URL + "/playlists/getplaylistbychannelid"), params=params)
            response.raise_for_status()
            data = response.json()

            for song in data["song"]:
                newtrack = Track()
                newtrack.channel_id = channel_id
                newtrack.song_title = song["title"]
                newtrack.artist_name = song["artist"]

                newtrack.song_start = self._microsoft_date_converter(song["starttimeutc"])
                newtrack.song_stop = self._microsoft_date_converter(song["stoptimeutc"])
                music_history_list.append(newtrack)

            return music_history_list

        except requests.exceptions.RequestException as e:
            print(e)
            return None



    def _microsoft_date_converter(self, time_text):
        """
        Convert a Microsoft date string to a formatted date string.

        Args:
            time_text (str): The Microsoft date string.

        Returns:
            str: The formatted date string.
        """
        time_ms = time_text[6:-2]
        time_s = (int(time_ms) / 1000)
        dt = datetime.fromtimestamp(time_s)
        return dt.strftime('%Y-%m-%d %H:%M:%S')



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
            print(e)



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
                print(e)

        except requests.exceptions.RequestException as e:
            print(e)




    def debugg_print(self, list):
        """
        Print the details of each track in the provided list.

        Args:
            list (list): A list of Track objects to be printed.
        """
        for t in list:
            print("#")
            print("| ID:     ", t.channel_id)
            print("| Name:   ", t.channel_name)
            print("|")
            print("| Song:   ", t.song_title)
            print("| Artist:  ", t.artist_name)
            print("| Start:   ", t.song_start)
            print("| Stop:   ", t.song_stop)
            print("|")
            print("| Color:  ", t.channel_color)
            print("| IMG:    ", t.channel_img)
            print("# ")
            print("\n\n")



