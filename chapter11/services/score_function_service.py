
class ScoreFunctionService:

    def __init__(self, data, tree):
        self.data = data
        self.tree = tree

    def call(self):
        dif = 0
        for data in self.data:
            v = self.tree.evaluate([data[0], data[1]])
            dif += abs(v - data[2])
        return dif
