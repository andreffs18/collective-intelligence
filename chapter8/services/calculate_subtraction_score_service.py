class CalculateSubtractionScoreService:

    def __init__(self, value=0, const=1.0):
        self.value = value
        self.constant = const

    def call(self):
        if self.value > self.constant:
            return 0

        return self.constant - self.value
