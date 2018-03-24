from services.searcher.normalize_scores_service import NormalizeScoresService


class LinkTextScoreService(object):

    def __init__(self, searcher, rows, word_ids):
        self.searcher = searcher
        self.rows = rows
        self.word_ids = word_ids
        self._vsmall = 0.000001  # prevent zero division errors

    def call(self):
        scores = dict([(row[0], 0) for row in self.rows])

        for word_id in self.word_ids:
            references = self._get_link_references(word_id)
            for (from_id, to_id) in references:
                if to_id in scores:
                    score = self._get_link_page_rank_score(from_id)
                    scores[toid] += score

        max_score = max(scores.values())
        if max_score == 0:
            max_score = self._vsmall
        return dict([(u, float(l) / max_score) for (u, l) in scores.items()])

    def _get_link_references(self, word_id):
        return self.searcher.con.execute(
            "SELECT link.fromid, link.toid "
            "FROM linkwords, link "
            "WHERE wordid={} and linkwords.linkid=link.rowid".format(word_id)
        )

    def _get_link_page_rank_score(self, from_id):
        return self.searcher.con.execute(
            "SELECT score FROM pagerank WHERE urlid={}".format(from_id)
        ).fetchone()[0]
