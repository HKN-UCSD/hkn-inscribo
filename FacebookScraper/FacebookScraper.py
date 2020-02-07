from selenium import webdriver
from bs4 import BeautifulSoup

class FacebookScraper:
    """A Facebook Scraper for HKN public events.
    This is meant to be used as a temporary solution before the database is setup as
    source of truth for events. For now, Facebook will be used as the source of truth.
    (Admittedly this does have the added benefit of not having to develop a UI for
    the user to input event information...)

    Note: This scraper was first conceived on November 25th 2019. Let's see how long
    it lives before Zuckerberg changes stuff up and breaks everything :)

    **Dependencies**
    Selenium
    - Used as webdriver to get rendered HTML from FB.
    Firefox
    - Used as browser.
    BeautifulSoup
    - Used as HTML parser.
    """
    def __init__(self):
        """Initializes scraper with headless driver running on Firefox.

        Attributes:
        driver - webdriver
        """
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.set_headless(headless=True)
        self.driver = webdriver.Firefox(
            options = options
        )

    def __del__(self):
        """Ensures driver is closed on destruction of FacebookScraper."""
        self.driver.close()

    def get_event(self, fb_url):
        """Given link to facebook event, returns dictionary containing event details.
        Note: Method will probably refactored soon to return an Event object instead of this stupid dictionary stuff.

        Arguments:
            fb_url: str
                url to PUBLIC Facebook event.

        Returns:
            event_dict: dict {str:str}
                title: str
                time: str
                date: str
                    This was included so that we can use date to determine which week
                    an event is occurring instead of having to wrangle the date out
                    of the date time string.
                location: str
                description: str
                urls: {str:str}
                    fb: str
                        This is equal to fb_url, and is just duplicated for convenience.
                    rsvp: str
                        RSVP link for the event is taken from the get tickets link on event.
                    banner: str
                        Link to event banner image.
        """
        html_src = self._get_html(fb_url)
        soup = BeautifulSoup(html_src, 'html.parser')
        event_dict = {}
        event_dict['title'] = self._get_event_title(soup)
        event_dict['time'] = self._get_event_time(soup)
        event_dict['location'] = self._get_event_location(soup)
        event_dict['date'] = self._get_event_date(soup)
        event_dict['description'] = self._get_event_description(soup)
        event_dict['urls'] = {}
        event_dict['urls']['rsvp'] = self._get_event_rsvp_url(soup)
        event_dict['urls']['banner'] = self._get_event_banner_url(soup)
        event_dict['urls']['fb'] = fb_url
        return event_dict

    def _get_event_title(self, soup):
        return soup.select('h1[data-testid="event-permalink-event-name"]')[0].contents

    def _get_event_time(self, soup):
        return soup.find_all('div', class_='_xkh', limit=1)[0].find('div').contents[0]

    def _get_event_location(self, soup):
        """Sometimes the location is in a span and sometimes it's in a div... """
        td_tag = soup.select('div[id="event_summary"]')[0].ul.select('li')[1].select('td')[-1]
        location_tag_list = td_tag.select('span') + td_tag.select('a')
        return location_tag_list[0].contents

    def _get_event_date(self, soup):
        return soup.select('div[id="title_subtitle"]')[0].span.get('title')

    def _get_event_description(self, soup):
        return soup.select('div[data-testid="event-permalink-details"]')[0].find('span').contents[0]

    def _get_event_rsvp_url(self, soup):
        """Facebook tags on a tracker to links originating from page, so need to delegate to _get_actual_url."""
        tags= soup.select('a[href*="forms.gle"]') + soup.select('a[href*="docs.google"]')
        if not tags:
            return ''
        rsvp_url_with_tracker = tags[0].a.get('href')
        return self._get_actual_url(rsvp_url_with_tracker)

    def _get_event_banner_url(self, soup):
        return soup.select('div[class*="uiScaledImageContainer"]')[0].img.get('data-src')

    def _get_html(self, url):
        self.driver.get(url)
        html = str(self.driver.page_source)
        return html

    def _get_actual_url(self, url):
        self.driver.get(url)
        actual_url = self.driver.current_url
        return actual_url

    def _log_errors(self):
        pass
