

class CreateIndexTablesService(object):

    def __init__(self, crawler):
        self.crawler = crawler

    def call(self):
        print("Start with creation of table...")
        self.crawler.con.execute('CREATE TABLE urllist(url)')
        self.crawler.con.execute('CREATE TABLE wordlist(word)')
        self.crawler.con.execute('CREATE TABLE wordlocation(urllid, wordid, location)')
        self.crawler.con.execute('CREATE TABLE link(fromid INTEGER, toid INTEGER)')
        self.crawler.con.execute('CREATE TABLE linkwords(wordid, linkid)')

        self.crawler.con.execute('CREATE INDEX wordidx ON wordlist(word)')
        self.crawler.con.execute('CREATE INDEX urlidx ON urllist(url)')
        self.crawler.con.execute('CREATE INDEX wordurlidx ON wordlocation(wordid)')
        self.crawler.con.execute('CREATE INDEX urltoidx ON link(toid)')
        self.crawler.con.execute('CREATE INDEX urlfromidx ON link(fromid)')

        self.crawler.db_commit()
        print("Tables created with success!")
