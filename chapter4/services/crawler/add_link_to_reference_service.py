class AddLinkReferenceService(object):

    def __init__(self, crawler, url_from, url_to, link_text):
        self.crawler = crawler
        self.url_from = url_from
        self.url_to = url_to
        self.link_text = link_text

    def call(self):
        url_from_id = self.crawler.get_entry_id('urllist', 'url', self.url_from)
        url_to_id = self.crawler.get_entry_id('urllist', 'url', self.url_to)

        query = "INSERT INTO link (fromid, toid) VALUES ({}, {})".format(url_from_id, url_to_id)
        return self.crawler.con.execute(query)
