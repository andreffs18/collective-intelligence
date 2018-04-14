class BaseClassifierService(object):

    def __init__(self, get_features, filename=None):
        # Counts of feature/category combinations
        self.fc = {}
        # Counts of documents in each category
        self.cc = {}
        self.get_features = get_features
        self.filename = filename

    def incf(self, f, cat):
        """
        Increment amount of times pair "feature/category" is used
        """
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    def incc(self, cat):
        """
        Increment the amount of times category "cat" is used
        """
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def fcount(self, f, cat):
        """
        Return count for given feature/category pair
        """
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return .0

    def ccount(self, cat):
        """
        Return count for given category
        """
        if cat in self.cc:
            return float(self.cc[cat])
        return .0

    def total_count(self):
        """
        Return total amount of categories
        """
        return sum(self.cc.values())

    def categories(self):
        """
        Return all categories
        """
        return self.cc.keys()

    def train(self, item, category):
        """
        For given item (string/sentence) and category ("bad", "good", etc) update scores on classifier set
        """
        features = self.get_features(item)
        for feature in features:
            self.incf(feature, category)
        self.incc(category)

    def fprob(self, f, cat):
        """
        For given feature & category, calculate the probability that a word (feature) is in an particular
        category. To do that, just divide the amount of times the word appears in a document by the total
        amount of documents. (Basically, we're just doing conditional probability)
        """
        try:
            return self.fcount(f, cat) / self.ccount(cat)
        except ZeroDivisionError:
            return 0

    def wprob(self, f, cat, prob_func=None, weight=1.0, assumed_probability=0.5):
        """
        Calculate weighted probability
        """
        # Calculate current probability
        if not prob_func:
            prob_func = self.fprob
        basic_prob = prob_func(f, cat)

        # Count the number of times this feature has appeared in all categories
        count = sum([self.fcount(f, c) for c in self.categories()])

        # Calculate the weighted average
        print(weight, assumed_probability, count, basic_prob, weight, count)
        return ((weight * assumed_probability) + (count * basic_prob)) / (weight + count)

#
#def incf(self, f, cat):
#    count = self.fcount(f, cat)
#    if count == 0:
#        self.con.execute("insert into fc values ('%s','%s',1)" % (f, cat))
#    else:
#        self.con.execute("update fc set count=%d where feature='%s' and category='%s'" % (count + 1, f, cat))
#
#def incc(self, cat):
#    count = self.catcount(cat)
#    if count == 0:
#        self.con.execute("insert into cc values ('%s',1)" % (cat))
#    else:
#        self.con.execute("update cc set count=%d where category='%s'" % (count + 1, cat))
#
#
#def fcount(self, f, cat):
#    res = self.con.execute('select count from fc where feature="%s" and category="%s"' % (f, cat)).fetchone()
#    if res == None:
#        return 0
#    else:
#        return float(res[0])
#
#
#def catcount(self, cat):
#    res = self.con.execute('select count from cc where category="%s"' % (cat)).fetchone()
#    if res == None:
#        return 0
#    else:
#        return float(res[0])
#
#def categories(self):
#    cur = self.con.execute('select category from cc');
#    return [d[0] for d in cur]
#
#def totalcount(self):
#    res = self.con.execute('select sum(count) from cc').fetchone();
#    if res == None: return 0
#    return res[0]
#
#

#def setdb(self, dbfile):
#    self.con = sqlite.connect(dbfile)
#    self.con.execute('create table if not exists fc(feature,category,count)')
#    self.con.execute('create table if not exists cc(category,count)')
#