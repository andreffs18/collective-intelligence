import re
import math
from sqlite3 import dbapi2 as sqlite


def get_words(document, min_words=2, max_words=20):
    """
    From given document (string) return list of words between min_words and max_words
    """
    splitter = re.compile('\\W*')
    # Split the words by non-alpha characters and lower splitted words
    words = splitter.split(document)
    words = map(lambda w: w.lower(), words)
    # Only words that are between "min_words" and "max_words" characters
    words = filter(lambda w: min_words < len(w) < max_words, words)
    # Return the unique set of words only
    words = list(set(words))
    return dict(map(lambda w: (w, 1), words))

#
# class NaiveBayes(Classifier):
#     def __init__(self, getfeatures):
#         classifier.__init__(self, getfeatures)
#         self.thresholds = {}
#
#     def docprob(self, item, cat):
#         features = self.getfeatures(item)
#
#         # Multiply the probabilities of all the features together
#         p = 1
#         for f in features: p *= self.weightedprob(f, cat, self.fprob)
#         return p
#
#     def prob(self, item, cat):
#         catprob = self.catcount(cat) / self.totalcount()
#         docprob = self.docprob(item, cat)
#         return docprob * catprob
#
#     def setthreshold(self, cat, t):
#         self.thresholds[cat] = t
#
#     def getthreshold(self, cat):
#         if cat not in self.thresholds: return 1.0
#         return self.thresholds[cat]
#
#     def classify(self, item, default=None):
#         probs = {}
#         # Find the category with the highest probability
#         max = 0.0
#         for cat in self.categories():
#             probs[cat] = self.prob(item, cat)
#             if probs[cat] > max:
#                 max = probs[cat]
#                 best = cat
#
#         # Make sure the probability exceeds threshold*next best
#         for cat in probs:
#             if cat == best: continue
#             if probs[cat] * self.getthreshold(best) > probs[best]: return default
#         return best
#
#
# class FisherClassifier(Classifier):
#     def cprob(self, f, cat):
#         # The frequency of this feature in this category
#         clf = self.fprob(f, cat)
#         if clf == 0: return 0
#
#         # The frequency of this feature in all the categories
#         freqsum = sum([self.fprob(f, c) for c in self.categories()])
#
#         # The probability is the frequency in this category divided by
#         # the overall frequency
#         p = clf / (freqsum)
#
#         return p
#
#     def fisherprob(self, item, cat):
#         # Multiply all the probabilities together
#         p = 1
#         features = self.getfeatures(item)
#         for f in features:
#             p *= (self.weightedprob(f, cat, self.cprob))
#
#         # Take the natural log and multiply by -2
#         fscore = -2 * math.log(p)
#
#         # Use the inverse chi2 function to get a probability
#         return self.invchi2(fscore, len(features) * 2)
#
#     def invchi2(self, chi, df):
#         m = chi / 2.0
#         sum = term = math.exp(-m)
#         for i in range(1, df // 2):
#             term *= m / i
#             sum += term
#         return min(sum, 1.0)
#
#     def __init__(self, getfeatures):
#         classifier.__init__(self, getfeatures)
#         self.minimums = {}
#
#     def setminimum(self, cat, min):
#         self.minimums[cat] = min
#
#     def getminimum(self, cat):
#         if cat not in self.minimums: return 0
#         return self.minimums[cat]
#
#     def classify(self, item, default=None):
#         # Loop through looking for the best result
#         best = default
#         max = 0.0
#         for c in self.categories():
#             p = self.fisherprob(item, c)
#             # Make sure it exceeds its minimum
#             if p > self.getminimum(c) and p > max:
#                 best = c
#                 max = p
#         return best
#
#
