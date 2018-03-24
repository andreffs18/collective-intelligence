from services.frequency_score_service import FrequencyScoreService
from services.location_score_service import LocationScoreService
from services.distance_score_service import DistanceScoreService
from services.inbound_link_score_service import InboundLinkScoreService


class GetScoredListService(object):

    def __init__(self, searcher, rows, word_ids):
        self.searcher = searcher
        self.rows = rows
        self.word_ids = word_ids

    def call(self):
        total_scores = dict([(row[0], 0) for row in self.rows])

        weights = [
            (1.0, FrequencyScoreService(self.rows)),
            (1.5, LocationScoreService(self.rows)),
            (1.5, DistanceScoreService(self.rows)),
            (2.0, InboundLinkScoreService(self.searcher, self.rows))
        ]

        for (weight, scores) in weights:
            for url in total_scores:
                total_scores[url] += weight * scores[url]
        return total_scores
