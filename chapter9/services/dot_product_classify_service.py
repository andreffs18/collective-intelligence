class DotProductClassifyService:

    def __init__(self, point, averages):
        self.point = point
        self.avgs = averages

    def _dot_product(self, v1, v2):
        return sum([v1[i] * v2[i] for i in range(len(v1))])

    def call(self):
        """
        class = (X.M0 - X.M1 + (M0.M0 - M1.M1) / 2)
        class = (     y      +           b)
        """
        b = (self._dot_product(self.avgs[1], self.avgs[1]) - self._dot_product(self.avgs[0], self.avgs[0])) / 2
        y = (self._dot_product(self.point, self.avgs[0]) - self._dot_product(self.point, self.avgs[1]))
        return 0 if (y + b) > 0 else 1
