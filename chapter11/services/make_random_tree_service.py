from random import random, choice, randint
from gp import Node, ParamNode, ConstNode

from .generate_function_list_service import GenerateFunctionListService


class MakeRandomTreeService:

    def __init__(self, input_size, max_depth=4, fpr=0.5, ppr=0.6):
        self.input_size = input_size
        self.max_tree_depth = max_depth
        self.prob_func_node = fpr
        self.prob_param_node = ppr

    def call(self):
        if random() < self.prob_func_node and self.max_tree_depth > 0:
            f = choice(GenerateFunctionListService().call())
            children = [MakeRandomTreeService(self.input_size, self.max_tree_depth - 1,
                                              self.prob_func_node, self.prob_param_node).call()
                        for _ in range(f.child_count)]
            return Node(f, children)
        elif random() < self.prob_param_node:
            return ParamNode(randint(0, self.input_size - 1))
        else:
            return ConstNode(randint(0, 10))
