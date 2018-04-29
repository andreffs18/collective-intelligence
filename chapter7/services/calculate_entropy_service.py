from math import log
from services import CountUniqueElementsService


class CalculateEntropyService:

    def __init__(self, rows):
        self.rows = rows

    def call(self):
        """
        Calculate the sum of p(x)*log(p(x)) across all dfferent possible results
        """
        log2 = lambda x: log(x) / log(2)
        counts = CountUniqueElementsService(self.rows).call()
        # Now calculate the entropy
        ent = .0
        for element in counts:
            p = float(counts[element]) / len(self.rows)
            ent -= p * log2(p)

        return ent
