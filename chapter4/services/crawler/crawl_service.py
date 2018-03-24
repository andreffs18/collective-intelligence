import urllib2
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin


class CrawlService(object):

    def __init__(self, crawler, pages, depth=2):
        self.crawler = crawler
        self.pages = pages
        self.depth = depth

    def call(self):
        for i in range(self.depth):
            new_pages = set()

            for page in self.pages:
                # soup = self._get_soup(page)
                soup = self._get_better_soup(page)
                if not soup:
                    continue

                self.crawler.add_to_index(page, soup)
                links = soup('a')
                for link in links:

                    url = self._get_url(page, link)
                    if not url:
                        continue

                    new_pages.add(url)
                    link_text = self.crawler.get_text_only(url)
                    self.crawler.add_link_ref(page, url, link_text)

                self.crawler.db_commit()

            self.pages = new_pages

    def _get_soup(self, page):
        try:
            c = urllib2.urlopen(page)
        except:
            print("Could not open page \"{}\"".format(page))
            return None
        soup = BeautifulSoup(c.read(), "html5lib")
        return soup

    def _get_better_soup(self, page, fake_headers=False, verify=False):
        """Validates all calls from requests.get"""
        headers = {}
        if fake_headers:
            headers = {
                "user-agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko)"
                               " Chrome/55.0.2883.95 Safari/537.36"),
                "accept-language": "en"
            }

        res = requests.get(page, verify=verify, headers=headers, cookies={'detectedCountry': 'EN'})
        if res.status_code != 200:
            if fake_headers and verify:
                print("Could not open page \"{}\"".format(page))
                return BeautifulSoup("", "html5lib")
            return self._get_better_soup(page, fake_headers=True, verify=True)
        return BeautifulSoup(res.text, "html5lib")

    def _get_url(self, page, link):
        if 'href' not in dict(link.attrs):
            return None

        url = urljoin(page, link['href'])

        if url.find("'") != -1:
            return None

        url = url.split("#")[0]

        try:
            url = url.encode('utf8')
        except:
            try:
                url = url.decode('utf8')
            except:
                import pdb; pdb.set_trace()

        if url[0:4] == 'http' and not self.crawler.is_indexed(url):
            return url

        return None
