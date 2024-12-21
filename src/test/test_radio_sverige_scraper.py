from src.main.api.radio_sverige_scraper import RadioSverigeScraper

if __name__ == '__main__':
    rsc = RadioSverigeScraper()
    list = rsc.start_scraper()
