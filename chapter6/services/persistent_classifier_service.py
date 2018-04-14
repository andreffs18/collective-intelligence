from sqlite3 import dbapi2 as sqlite


class PersistentClassifierService(object):

    def __init__(self, dbname='classifier.db'):
        super(PersistentClassifierService, self).__init__()
        print("Using PersistentStorage: {}".format(dbname))
        self.dbname = dbname
        self.setdb()

    def setdb(self):
        """
        Initialize database with default tables
        """
        self.con = sqlite.connect(self.dbname)
        self.con.execute('CREATE TABLE IF NOT EXISTS fc(feature, category, count)')
        self.con.execute('CREATE TABLE IF NOT EXISTS cc(category, count)')

    def incf(self, f, cat):
        """
        Increment amount of times pair "feature/category" is used
        """
        count = self.fcount(f, cat)
        if not count:
            self.con.execute("INSERT INTO fc "
                             "VALUES ('{}', '{}', 1)".format(f, cat))
        else:
            self.con.execute("UPDATE fc "
                             "SET count={} "
                             "WHERE feature='{}' AND category='{}'".format(count + 1, f, cat))

    def incc(self, cat):
        """
        Increment the amount of times category "cat" is used
        """
        count = self.ccount(cat)
        if not count:
            self.con.execute("INSERT INTO cc VALUES ('{}', 1)".format(cat))
        else:
            self.con.execute("UPDATE cc "
                             "SET count={} "
                             "WHERE category='{}'".format(count + 1, cat))

    def fcount(self, f, cat):
        """
        Return count for given feature/category pair
        """
        res = self.con.execute('SELECT count '
                               'FROM fc '
                               'WHERE feature="{}" AND category="{}"'
                               ''.format(f, cat)).fetchone()
        if not res:
            return 0
        return float(res[0])

    def ccount(self, cat):
        """
        Return count for given category
        """
        res = self.con.execute('SELECT count '
                               'FROM cc '
                               'WHERE category="{}"'.format(cat)).fetchone()
        if not res:
            return 0
        return float(res[0])

    def total_count(self):
        """
        Return total amount of categories
        """
        res = self.con.execute('SELECT SUM(count) '
                               'FROM cc').fetchone();
        if not res:
            return 0
        return res[0]

    def categories(self):
        """
        Return all categories
        """
        cur = self.con.execute('SELECT category '
                               'FROM cc');
        return [d[0] for d in cur]
