from src.main.api.sveriges_radio_api import SvergiesRadioApi

if __name__ == '__main__':
    sveriges_radio = SvergiesRadioApi()
    list = sveriges_radio.get_all_channels()
    #list = sveriges_radio.get_channel_music_history(2562)
    sveriges_radio.debugg_print(list)
