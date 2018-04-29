from services import CountUniqueElementsService

class CalculateGiniImpurityService:
    def __init__(self, rows):
        self.rows = rows

    def call(self):
        """
        Calculate the probability that a randomly placed item will be in the wrong category
        """
        total = len(self.rows)
        counts = CountUniqueElementsService(self.rows).call()

        impurity = 0
        for element1 in counts:
            for element2 in counts:
                if element1 == element2:
                    continue

                p1 = float(counts[element1]) / total
                p2 = float(counts[element2]) / total
                impurity += p1 * p2
        return impurity
