class CalculateInverseScoreService:

    def __init__(self, num=1.0, den=0, const=0.1):
        self.numerator = num
        self.denominator = den
        self.constant = const

    def call(self):
        return self.numerator / (self.denominator + self.constant)
