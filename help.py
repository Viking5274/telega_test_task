import re
from bs4 import BeautifulSoup
import html2text
import requests


class TeleScraper:
    def __init__(self, post_urls):
        self.post_urls = post_urls
        self.urlSplit = self.post_urls.split(',')
        self.urlList = [entry + '?embed=1&mode=tme' for entry in self.urlSplit]
        self.author = ""
        self.content = ""
        self.dateTime = ""
        self.media_data = ""

    def html_to_text(self, html):
        h = html2text.HTML2Text()

        text = h.handle(html)
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'^[ \t]*[\\`]', '', text, flags=re.MULTILINE)
        return text

    def parse_date(self, html_str):
        self.content = self.html_to_text(
            str(html_str.find('div', {'class': 'tgme_widget_message_text js-message_text', 'dir': 'auto'})))
        self.author = self.html_to_text(
            str(html_str.find('div', {'class': 'tgme_widget_message_author accent_color'}).find('a', {
                'class': 'tgme_widget_message_owner_name'}).find('span', {'dir': 'auto'})))
        self.dateTime = self.html_to_text(
            str(html_str.find('span', {'class': 'tgme_widget_message_meta'}).find('time',
                                                                                  {'class': 'datetime'})))

    def get_media_data(self, html_str):
        imgs = html_str.findAll('a', {'class': 'tgme_widget_message_photo_wrap'})
        videos = html_str.findAll('div', {'class': 'tgme_widget_message_video_wrap'})
        if len(imgs) > 0 or len(videos) > 0:
            self.media_data = f'[TG Scraper] Found {len(imgs)} image(s) and {len(videos)} video(s).'
        else:
            self.media_data = 'No Media Found.'

    async def run(self):

        try:
            for link in self.urlList:

                link_req = requests.get(url=link)
                link_req.raise_for_status()
                html_str = BeautifulSoup(link_req.text, 'html.parser')

                self.parse_date(html_str)
                self.get_media_data(html_str)

        except requests.exceptions.RequestException as err:
            print(err)
