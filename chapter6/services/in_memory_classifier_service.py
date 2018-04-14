class InMemoryClassifierService(object):

    def __init__(self, *args, **kwargs):
        super(InMemoryClassifierService, self).__init__()
        print("Using InMemoryStorage")
        # Counts of feature/category combinations
        self.fc = {}
        # Counts of documents in each category
        self.cc = {}

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

