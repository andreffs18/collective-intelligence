import math


class CalculateGaussianScoreService:

    def __init__(self, value=0, sigma=10.0):
        self.value = value
        self.sigma = sigma

    def call(self):
        return math.e ** (-self.value ** 2 / (2 * self.sigma ** 2))
