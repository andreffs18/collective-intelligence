from services import CalculateEuclideanDistanceService


class CalculateKNNService:

    def __init__(self, data, vec1, k=5, score_func=CalculateEuclideanDistanceService):
        self.data = data
        self.vec1 = vec1
        self.k = k
        self.score_func = score_func

    def call(self):
        # Get sorted distances
        dlist = self._get_distances()
        avg = 0.0

        # Take the average of the top k results
        for i in range(self.k):
            idx = dlist[i][1]
            avg += self.data[idx]['result']

        avg /= float(self.k)
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
