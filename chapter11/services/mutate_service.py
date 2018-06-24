from random import random, choice
from copy import deepcopy

from .make_random_tree_service import MakeRandomTreeService


class MutateService:
    def __init__(self, t, pc, probchange=0.1):
        self.t = t
        self.pc = pc
        self.probchange = probchange

    def call(self):
        if random() < self.probchange:
            return MakeRandomTreeService(self.pc).call()
        else:
            result = deepcopy(self.t)
            if hasattr(self.t, "children"):
                result.children = [MutateService(c, self.pc, self.probchange).call() for c in self.t.children]
            return result
