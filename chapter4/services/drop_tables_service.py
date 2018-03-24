

class DropTablesService(object):

    def __init__(self, crawler):
        self.crawler = crawler

    def call(self):
        print("Start drop tables...")
        self.crawler.con.execute('DROP TABLE urllist')
        self.crawler.con.execute('DROP TABLE wordlist')
        self.crawler.con.execute('DROP TABLE wordlocation')
        self.crawler.con.execute('DROP TABLE link')
        self.crawler.con.execute('DROP TABLE linkwords')

        self.crawler.db_commit()
        print("Tables dropped with success!")
