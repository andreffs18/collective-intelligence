from bs4 import BeautifulSoup


class GetTextOnlyService(object):

    def __init__(self, crawler, soup):
        self.crawler = crawler

        if isinstance(soup, basestring):
            soup = BeautifulSoup(soup, "html5lib")

        self.soup = soup

    def call(self):
        v = self.soup.get_text()
        if v is not None:
            return v.strip()

        contents = self.soup.contents
        result_text = ''
        for text in contents:
            sub_text = GetTextOnlyService(self.crawler, text).call()
            result_text += sub_text + "\n"
        return result_text
