from FacebookScraper import FacebookScraper
import pprint
scraper = FacebookScraper()
fb_urls = [
    'https://www.facebook.com/events/572493850165742/',
    'https://www.facebook.com/events/2173701746067049/',
    'https://www.facebook.com/events/1341938379320787/',
    'https://www.facebook.com/events/2654179024633236/',
]

# fb_urls = ['https://www.facebook.com/events/526480761508199/']

pp = pprint.PrettyPrinter(indent = 2)
for url in fb_urls:
    pp.pprint(scraper.get_event(url))