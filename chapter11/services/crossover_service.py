from random import random, choice
from copy import deepcopy


class CrossoverService:
    def __init__(self, t1, t2, probswap=0.7, top=1):
        self.t1 = t1
        self.t2 = t2
        self.probswap = probswap
        self.top = top

    def call(self):
        if random() < self.probswap and not self.top:
            return deepcopy(self.t2)
        else:
            result = deepcopy(self.t1)
            if hasattr(self.t1, 'children') and hasattr(self.t2, 'children'):
                result.children = [CrossoverService(c, choice(self.t2.children), self.probswap, 0)
                                   for c in self.t1.children]
            return result
