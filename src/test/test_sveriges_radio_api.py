from src.main.api.sveriges_radio_api import sveriges_radio_api

if __name__ == '__main__':
    sveriges_radio = sveriges_radio_api()
    sveriges_radio.get_all_channels()
    #sveriges_radio.get_channel_music_history(163)
