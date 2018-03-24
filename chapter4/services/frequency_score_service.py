from services.normalize_scores_service import NormalizeScoresService

class FrequencyScoreService(object):

    def __init__(self, rows):
        self.rows = rows

    def call(self):
        counts = dict([(row[0], 0) for row in self.rows])

        for row in self.rows:
            counts[row[0]] += 1
        return NormalizeScoresService(counts).call()
