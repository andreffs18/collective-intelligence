class GetTextOnlyService(object):

    def __init__(self, crawler, soup):
        self.crawler = crawler
        self.soup = soup

    def call(self):
        v = self.soup.string
        if v is None:
            return v.strip()

        contents = self.soup.contents
        result_text = ''
        for text in contents:
            sub_text = GetTextOnlyService(self.crawler, text).call()
            result_text += sub_text + "\n"
        return result_text
