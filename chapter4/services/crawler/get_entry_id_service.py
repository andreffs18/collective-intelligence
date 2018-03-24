class GetEntryIdService(object):

    def __init__(self, crawler, table, field, value, create_new):
        self.crawler = crawler
        self.table = table
        self.field = field
        self.value = value
        self.create_new = create_new

    def call(self):
        cur = self.crawler.con.execute("SELECT rowid FROM {} WHERE {}='{}'".format(self.table, self.field, self.value))
        res = cur.fetchone()
        if res is not None:
            return res[0]

        cur = self.crawler.con.execute("INSERT INTO {} ({}) VALUES ('{}')".format(self.table, self.field, self.value))
        return cur.lastrowid
