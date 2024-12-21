from playwright.sync_api import sync_playwright
import random
import time



class RadioSverigeScraper:
    """
    A class to scrape radio information from the Radio Sveriges website.

    This class uses Playwright to interact with the Radio Sveriges website
    and retrieve information about various radio channels.
    """

    def __init__(self):
        """
        Initialize the RadioSverigeScraper class.
        """
        self._HEADLESS_BROWSER = False
        self._URL = "https://www.radio-sveriges.se"
        self._SOURCES_LIST = ['a[href="/rix-fm"]',
                              'a[href="/mix-megapol"]' ,
                              'a[href="/guldkanalen"]',
                              'a[href="/star-fm"]',
                              'a[href="/nrj"]',
                              'a[href="/dansbandskanalen"]',
                              'a[href="/retro-fm"]' ]


    def start_scraper(self):
        """
        Start the web scraper.

        This method launches a Playwright browser, navigates to the Radio Sveriges
        website, and retrieves information about various radio channels.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self._HEADLESS_BROWSER)
            page = browser.new_page()
            page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Accept-Encoding": "gzip, deflate, br",
            })

            response = page.goto(self._URL)

            if 200 <= response.status < 300:
                page.wait_for_selector(".qc-cmp2-summary-buttons") # Cookie banner
                page.click(".qc-cmp2-summary-buttons .css-47sehv") # Cookie btn


                copy_list = self._SOURCES_LIST
                while copy_list:
                    page.wait_for_selector('body')
                    random_item = random.choice(copy_list)
                    channel_name  = (random_item[9:-2])
                    self._mouseMovent(page)
                    self.newpage(page, random_item, channel_name)
                    copy_list.remove(random_item)



            elif response.status == 429:
                print("Rate limit reached!")

            else:
                print(response.status)

            time.sleep(random.uniform(5, 9))
            browser.close()



    def newpage (self, page, source, channel_name):
        """
        Open a new page and retrieve information about a specific radio channel.

        Args:
            page: The Playwright page object.
            source (str): The CSS selector for the radio channel link.
            channel_name (str): The name of the radio channel.
        """
        #time.sleep(random.uniform(1, 3))
        page.click(source)

        self._Check_for_ad(page, source)
        page.wait_for_load_state("load")

        try:
            page.wait_for_selector("#player_box_container", timeout=30000) # 30 seconds timeout

            self._mouseMovent(page)
            time.sleep(random.uniform(1, 2))
            artist_name_element = page.query_selector(".latest-song .history-song .artist-name")
            artist_name = artist_name_element.text_content() if artist_name_element else None

            song_name_element = page.query_selector(".latest-song .history-song .song-name p")
            song_name = song_name_element.text_content() if song_name_element else None

            image = page.query_selector(".latest-song .history-song img.lazy")
            image_song = image.get_attribute("src") if image else None

            image = page.query_selector("#player_image_container img")
            image_Channel = image.get_attribute("src") if image else None

            print("")
            print(f"Channel_name: {channel_name}")
            print(f"Channel_IMG: {image_Channel}")
            print(f"Song Name: {song_name}")
            print(f"Artist Name: {artist_name}")
            print(f"Song IMG: {image_song}")

            #self._mouseMovent(page)
            #time.sleep(random.uniform(2, 4))
        except TimeoutError:
            print(f"Page took too long to load: {channel_name}. Skipping...")

        page.go_back()



    @staticmethod
    def _mouseMovent(page):
        """
        Simulate random mouse movements.

        Args:
            page: The Playwright page object.
        """
        page.mouse.move(random.randint(0, 1000), random.randint(0, 1000))
        page.mouse.wheel(0, random.randint(500, 1500))



    def _Check_for_ad(self, page, source):
        """
        Check for and handle popup advertisements.

        Args:
            page: The Playwright page object.
            source (str): The CSS selector for the radio channel link.
        """
        time.sleep(random.uniform(1, 2))
        ins_element = page.query_selector('#gpt_unit_62660943\\/APPGEN_radiose\\/web_interstitial_0')

        if(ins_element):
            print("\n### ad detected! ###")
            page.reload()
            page.wait_for_selector('body')
            page.click(source)








