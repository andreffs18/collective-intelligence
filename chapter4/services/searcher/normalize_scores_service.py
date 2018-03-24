class NormalizeScoresService(object):

    def __init__(self, scores, small=True):
        self.scores = scores
        self.small = small
        self._vsmall = 0.000001  # to avoid zero division error

    def call(self):
        min_score = min(self.scores.values())
        max_score = max(self.scores.values())

        if self.small:
            return dict(
                [(u, float(min_score) / max(self._vsmall, l))
                 for (u, l) in self.scores.items()]
            )

        if max_score == 0:
            max_score = self._vsmall

        return dict(
            [(u, float(c) / max_score)
             for (u, c) in self.scores.items()]
        )
