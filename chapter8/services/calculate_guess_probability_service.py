from services import CalculateGaussianScoreService


class CalculateGuessProbabilityService:
    def __init__(self, data, vec1, low, high, k=5, score_func=CalculateGaussianScoreService):
        self.data = data
        self.vec1 = vec1
        self.low = low
        self.high = high
        self.k = k
        self.score_func = score_func

    def call(self):
        dlist = self._get_distances()
        nweight = 0.0
        tweight = 0.0

        for i in range(self.k):
            dist = dlist[i][0]
            idx = dlist[i][1]
            weight = self.score_func(dist).call()
            v = self.data[idx]['result']

            # Is this point in the range?
            if self.low <= v <= self.high:
                nweight += weight
            tweight += weight
        if tweight == 0:
            return 0

        # The probability is the weights in the range
        # divided by all the weights
        return nweight / tweight


    def _get_distances(self):
        distance_list = []

        # Loop over every item in the dataset
        for i in range(len(self.data)):
            vec2 = self.data[i]['input']

            # Add the distance and the index
            distance_list.append((self.score_func(self.vec1, vec2).call(), i))

        # Sort by distance
        distance_list.sort()
        return distance_list
