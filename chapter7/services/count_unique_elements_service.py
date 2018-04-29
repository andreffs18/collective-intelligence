from collections import Counter


class CountUniqueElementsService:

    def __init__(self, rows):
        self.rows = rows

    def call(self):
        """
        Create counts of possible results (we assume that th last column of each row is the result)
        """
        last_elements = map(lambda r: r[-1], self.rows)
        return Counter(last_elements)
