from services.normalize_scores_service import NormalizeScoresService


class DistanceScoreService(object):

    def __init__(self, rows):
        self.rows = rows

    def call(self):
        # it there's only one word, everybody wins!
        if len(self.rows[0]) <= 2:
            return dict([(row[0], 1.0) for row in self.rows])

        # Initialize the dict with large values
        min_distance = dict([(row[0], 1000000) for row in self.rows])

        for row in self.rows:
            dist = sum([abs(row[i] - row[i - 1])for i in range(2, len(row))])
            if dist < min_distance[row[0]]:
                min_distance[row[0]] = dist

        return NormalizeScoresService(min_distance).call()
