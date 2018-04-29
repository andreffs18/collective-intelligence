from services import CalculateEntropyService
from services import CountUniqueElementsService


class PruneTreeService:

    def __init__(self, tree, minimum_gain, score_func=None):
        self.tree = tree
        self.minimum_gain = minimum_gain
        self.score_func = score_func or CalculateEntropyService

    def call(self):

        # If the branches aren't leaves, then prune them
        if not self.tree.tb.results:
            PruneTreeService(self.tree.tb, self.minimum_gain).call()
        if not self.tree.fb.results:
            PruneTreeService(self.tree.fb, self.minimum_gain).call()

        # If both the subbranches are now leaves, see if they should merged
        if self.tree.tb.results and self.tree.fb.results:
            # Build a combined dataset
            tb, fb = [], []
            for v, c in self.tree.tb.results.items():
                tb += [[v]] * c
            for v, c in self.tree.fb.results.items():
                fb += [[v]] * c

            # Test the reduction in entropy
            delta = self.score_func(tb + fb).call() - ((self.score_func(tb).call() + self.score_func(fb).call()) / 2)

            if delta < self.minimum_gain:
                # Merge the branches
                self.tree.tb, self.tree.fb = None, None
                self.tree.results = CountUniqueElementsService(tb + fb).call()
