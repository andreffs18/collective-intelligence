class IncompleteClassifyService:
    def __init__(self, observation, tree):
        self.observation = observation
        self.tree = tree

    def call(self):
        if self.tree.results:
            return self.tree.results

        v = self.observation[self.tree.col]
        if not v:
            return self.guess()

        if isinstance(v, int) or isinstance(v, float):
            if v >= self.tree.value:
                branch = self.tree.tb
            else:
                branch = self.tree.fb
        else:
            if v == self.tree.value:
                branch = self.tree.tb
            else:
                branch = self.tree.fb

        return IncompleteClassifyService(self.observation, branch).call()

    def guess(self):
        tr, fr = (IncompleteClassifyService(self.observation, self.tree.tb).call(),
                  IncompleteClassifyService(self.observation, self.tree.fb).call())
        tcount = sum(tr.values())
        fcount = sum(fr.values())
        tw = float(tcount) / (tcount + fcount)
        fw = float(fcount) / (tcount + fcount)
        result = {}
        for k, v in tr.items():
            result[k] = v * tw
        for k, v in fr.items():
            result[k] = v * fw
        return result
