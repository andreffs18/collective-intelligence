from .score_function_service import ScoreFunctionService

class GetRankFunctionService:

    def __init__(self, dataset):
        self.dataset = dataset

    def call(self):
        def rankfunction(population):
            scores = [(ScoreFunctionService(self.dataset, t).call(), t) for t in population]
            scores.sort()
            return scores

        return rankfunction
