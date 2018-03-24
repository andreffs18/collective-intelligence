class IsIndexedService(object):

    def __init__(self, crawler, url):
        self.crawler = crawler
        self.url = url

    def call(self):
        cur = self.crawler.con.execute("SELECT rowid FROM urllist WHERE url='{}'".format(self.url))
        res = cur.fetchone()
        if res is None:
            return False

        # check if has been actually been crawled
        cur = self.crawler.con.execute("SELECT * FROM wordlocation WHERE urlid={}".format(res[0]))
        res = cur.fetchone()
        if res is None:
            return False

        return True
