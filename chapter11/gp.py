class FunctionWrapper:
    def __init__(self, function, child_count, name):
        self.function = function
        self.child_count = child_count
        self.name = name


class Node:
    def __init__(self, function_wrapper, children):
        self.function = function_wrapper.function
        self.name = function_wrapper.name
        self.children = children

    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self, indent=0):
        print(' ' * indent) + self.name
        for c in self.children:
            c.display(indent + 1)


class ParamNode:
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, inp):
        return inp[self.idx]

    def display(self, indent=0):
        print('%sp%d' % (' ' * indent, self.idx))


class ConstNode:
    def __init__(self, v):
        self.v = v

    def evaluate(self, inp):
        return self.v

    def display(self, indent=0):
        print('%s%d' % (' ' * indent, self.v))

