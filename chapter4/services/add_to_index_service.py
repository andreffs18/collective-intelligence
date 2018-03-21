from services.get_text_only_service import GetTextOnlyService
from services.separate_words_service import SeparateWordsService

class AddToIndexService(object):

    def __init__(self, crawler, url, soup):
        self.crawler = crawler
        self.url = url
        self.soup = soup

    def call(self):
        if self.crawler.is_indexed(self.url):
            return
        print("Indexing {}".format(self.url))

        # get individual words
        text = GetTextOnlyService(self.crawler, self.soup).call()
        words = SeparateWordsService(text).call()

        # get the url id
        url_id = self.crawler.get_entry_id('urllist', 'url', self.url)

        # link each word to this url
        for i, word in enumerate(words):
            if word in IGNORE_WORDS:
                continue

            word_id = self.crawler.get_entry_id('wordlist', 'word', word)
            self.crawler.con.execute("insert into wordlocation(urlid, wordid, location) "
                                     "values ({}, {}, {})".format(url_id, word_id, i))



