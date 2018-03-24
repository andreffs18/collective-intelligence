from services.searcher.normalize_scores_service import NormalizeScoresService
from nn import SearchNet


class NNScoreService(object):

    def __init__(self, rows, word_ids):
        self.rows = rows
        self.word_ids = word_ids
        self.search_net = SearchNet()

    def call(self):
        # get unique url ids as an ordered list
        url_ids = [url_id for url_id in set([row[0] for row in self.rows])]
        nn_res = self.search_net.get_results(self.word_ids, url_ids)
        scores = dict([(url_ids[i], nn_res[i]) for i in range(len(url_ids))])
        return NormalizeScoresService(scores).call()
