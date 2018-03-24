from services.normalize_scores_service import NormalizeScoresService

class LocationScoreService(object):

    def __init__(self, rows):
        self.rows = rows

    def call(self):
        locations = dict([(row[0], 1000000) for row in self.rows])

        for row in self.rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]:
                locations[row[0]] = loc

        return NormalizeScoresService(locations, small=False).call()
