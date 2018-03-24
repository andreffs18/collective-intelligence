from services.searcher.frequency_score_service import FrequencyScoreService
from services.searcher.location_score_service import LocationScoreService
from services.searcher.distance_score_service import DistanceScoreService
from services.searcher.inbound_link_score_service import InboundLinkScoreService
from services.searcher.page_rank_score_service import PageRankScoreService
from services.searcher.link_text_score_service import LinkTextScoreService
from services.searcher.nn_score_service import NNScoreService


class GetScoredListService(object):

    def __init__(self, searcher, rows, word_ids):
        self.searcher = searcher
        self.rows = rows
        self.word_ids = word_ids

    def call(self):
        total_scores = dict([(row[0], 0) for row in self.rows])

        weights = [
            (1.0, FrequencyScoreService(self.rows).call()),
            (0.4, LocationScoreService(self.rows).call()),
            (0.6, DistanceScoreService(self.rows).call()),
            (0.8, InboundLinkScoreService(self.searcher, self.rows).call()),
            (1.0, PageRankScoreService(self.searcher, self.rows).call()),
            (1.0, LinkTextScoreService(self.searcher, self.rows, self.word_ids).call()),
            (5.0, NNScoreService(self.rows, self.word_ids).call())
        ]

        for (weight, scores) in weights:
            for url in total_scores:
                total_scores[url] += weight * scores[url]
        return total_scores
