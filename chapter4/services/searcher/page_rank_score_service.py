from services.searcher.normalize_scores_service import NormalizeScoresService


class PageRankScoreService(object):

    def __init__(self, searcher, rows):
        self.searcher = searcher
        self.rows = rows

    def call(self):
        page_ranks = dict([(row[0], self._get_page_rank_score(row[0])) for row in self.rows])
        max_rank = max(page_ranks.values())
        return dict([(u, float(l) / max_rank)
                     for (u, l) in page_ranks.items()])

    def _get_page_rank_score(self, url_id):
        return self.searcher.con.execute(
            "SELECT score FROM pagerank WHERE urlid={}".format(url_id)
        ).fetchone()[0]
