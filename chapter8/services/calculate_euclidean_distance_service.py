from math import sqrt


class CalculateEuclideanDistanceService:

    def __init__(self, v1, v2):
        self.value1 = v1
        self.value2 = v2

    def call(self):
        d = 0.0
        for i in range(len(self.value1)):
            d += (self.value1[i] - self.value2[i]) ** 2
        return sqrt(d)