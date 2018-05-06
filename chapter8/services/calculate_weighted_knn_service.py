from services import CalculateGaussianScoreService


class CalculateWeightedKNNService:

    def __init__(self, data, vec1, k=5, score_func=CalculateGaussianScoreService):
        self.data = data
        self.vec1 = vec1
        self.k = k
        self.score_func = score_func


    def call(self):
        # Get distances
        dlist = self._get_distances()

        avg = 0.0
        total_weight = 0.0

        # Get weighted average
        for i in range(self.k):
            dist = dlist[i][0]
            idx = dlist[i][1]

            weight = self.score_func(dist).call()
            avg += weight * self.data[idx]['result']
            total_weight += weight

        if total_weight == 0:
            return 0
        avg /= total_weight
        return avg

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
