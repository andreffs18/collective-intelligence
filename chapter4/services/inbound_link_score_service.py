from services.normalize_scores_service import NormalizeScoresService


class InboundLinkScoreService(object):

    def __init__(self, searcher, rows):
        self.searcher = searcher
        self.rows = rows

    def call(self):
        # it there's only one word, everybody wins!
        unique_urls = set([row[0] for row in self.rows])

        inbound_count = dict(
            [(u, self._get_count(u))
             for u in unique_urls]
        )

        return NormalizeScoresService(inbound_count).call()

    def _get_count(self, urlid):
        return self.searcher.con.execute(
            "SELECT count(*) FROM link WHERE toid='{}'".format(urlid)
        ).fetchone()[0]
