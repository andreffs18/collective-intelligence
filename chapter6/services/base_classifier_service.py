from .in_memory_classifier_service import InMemoryClassifierService
from .persistent_classifier_service import PersistentClassifierService


class BaseClassifierService(object):

    def __init__(self, get_features, persistent_storage=True, *args, **kwargs):
        self.get_features = get_features
        self.persistent_storage = persistent_storage

        if self.persistent_storage:
            self.s = PersistentClassifierService(*args, **kwargs)
        else:
            self.s = InMemoryClassifierService(*args, **kwargs)

        # inherit given methods
        for func in dir(self.s):
            if not func.startswith("__"):
                setattr(self, func, getattr(self.s, func))

    def train(self, item, category):
        """
        For given item (string/sentence) and category ("bad", "good", etc) update scores on classifier set
        """
        features = self.get_features(item)
        for feature in features:
            self.incf(feature, category)
        self.incc(category)

        if self.persistent_storage:
            self.con.commit()

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
        return ((weight * assumed_probability) + (count * basic_prob)) / (weight + count)
