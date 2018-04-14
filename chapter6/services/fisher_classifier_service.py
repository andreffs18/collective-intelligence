import math
from .base_classifier_service import BaseClassifierService


class FisherClassifierService(BaseClassifierService):

    def __init__(self, *args, **kwargs):
        super(FisherClassifierService, self).__init__(self, *args, **kwargs)
        self.minimums = {}

    def set_minimum(self, cat, min):
        self.minimums[cat] = min

    def get_minimum(self, cat):
        return self.minimums[cat] if cat in self.minimums else .0

    def cprob(self, f, cat):
        """
        Calculate the probability that given feature belong to given category, assuming that there
        will be an equal number of items in each category
        """
        # The frequency of this feature in this category
        clf = self.fprob(f, cat)
        if not clf:
            return 0

        # The frequency of this feature in all the categories
        freqsum = sum([self.fprob(f, c) for c in self.categories()])

        # The probability is the frequency in this category divided by the overall frequency
        return clf / (freqsum)

    def fisherprob(self, item, cat):
        # Multiply all the probabilities together
        p = 1
        for f in self.get_features(item):
            p *= (self.wprob(f, cat, prob_func=self.cprob))

        # Take the natural log and multiply by -2
        fscore = -2 * math.log(p)

        # Use the inverse chi2 function to get a probability
        return self.invchi2(fscore, len(self.get_features(item)) * 2)

    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df // 2):
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def classify(self, item, default=None):
        # Loop through looking for the best result
        best = default
        max = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            # Make sure it exceeds its minimum
            if p > self.get_minimum(c) and p > max:
                best = c
                max = p
        return best