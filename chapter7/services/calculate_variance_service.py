class CalculateVarianceService:
    def __init__(self, rows):
        self.rows = rows

    def call(self):
        """
        Calculate the variance of numbers in the result column
        """
        if not len(self.rows):
            return 0

        data = [float(row[-1]) for row in self.rows]
        mean = sum(data) / len(data)
        variance = sum([(d - mean) ** 2 for d in data]) / len(data)
        return variance
