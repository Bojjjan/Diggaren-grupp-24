class Track:
    def __init__(self):
        self._song_name = None
        self._song_img = None
        self._artist_name = None
        self._song_stop = None
        self._song_start = None
        self._channel_name = None
        self._channel_color = None
        self._channel_img = None
        self._channel_id = None

    # song_name
    @property
    def song_name(self):
        return self._song_name

    @song_name.setter
    def song_name(self, value):
        self._song_name = value

    # song_img
    @property
    def song_img(self):
        return self._song_img

    @song_img.setter
    def song_img(self, img):
        self._song_img = img

    # artist_name
    @property
    def artist_name(self):
        return self._artist_name

    @artist_name.setter
    def artist_name(self, value):
        self._artist_name = value

    # song_stop
    @property
    def song_stop(self):
        return self._song_stop

    @song_stop.setter
    def song_stop(self, value):
        self._song_stop = value

    # song_start
    @property
    def song_start(self):
        return self._song_start

    @song_start.setter
    def song_start(self, value):
        self._song_start = value

    # channel_name
    @property
    def channel_name(self):
        return self._channel_name

    @channel_name.setter
    def channel_name(self, value):
        self._channel_name = value

    # channel_color
    @property
    def channel_color(self):
        return self._channel_color

    @channel_color.setter
    def channel_color(self, value):
        self._channel_color = value

    # channel_img
    @property
    def channel_img(self):
        return self._channel_img

    @channel_img.setter
    def channel_img(self, value):
        self._channel_img = value

    # channel_id
    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value):
        self._channel_id = value