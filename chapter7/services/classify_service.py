class ClassifyService:

    def __init__(self, observation, tree):
        self.observation = observation
        self.tree = tree

    def call(self):
        if self.tree.results:
            return self.tree.results

        v = self.observation[self.tree.col]
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

        return ClassifyService(self.observation, branch).call()
