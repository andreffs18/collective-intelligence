from .base_classifier_service import BaseClassifierService


class NaiveClassifierService(BaseClassifierService):

    def __init__(self, *args, **kwargs):
        super(NaiveClassifierService, self).__init__(self, *args, **kwargs)
        self.thresholds = {}

    def set_threshold(self, cat, t):
        self.thresholds[cat] = t

    def get_threshold(self, cat):
        return self.thresholds[cat] if cat in self.thresholds else 1.0

    def dprob(self, item, cat):
        """
        Document probability: extract all words from item and multiplies all probabilities together
        """
        p = 1
        for f in self.get_features(item):
            p *= self.wprob(f, cat)
        return p

    def prob(self, item, cat):
        """
        calculate the probability of the category, and returns the product of PR(Document | Category)
        and PR(Category)
        """
        category_prob = self.ccount(cat) / self.total_count()
        document_prob = self.dprob(item, cat)
        return document_prob * category_prob

    def classify(self, item, default=None):
        probs = {}
        # Find the category with the highest probability
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat

        # Make sure the probability exceeds threshold * next best
        for cat in probs:
            if cat == best:
                continue
            if probs[cat] * self.get_threshold(best) > probs[best]:
                return default
        return best
