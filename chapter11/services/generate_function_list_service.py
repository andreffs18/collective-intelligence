from gp import FunctionWrapper


class GenerateFunctionListService:

    def call(self):
        addw = FunctionWrapper(lambda l: l[0] + l[1], 2, 'add')
        subw = FunctionWrapper(lambda l: l[0] - l[1], 2, 'subtract')
        mulw = FunctionWrapper(lambda l: l[0] * l[1], 2, 'multiply')

        def iffunc(l):
            if l[0] > 0:
                return l[1]
            else:
                return l[2]

        ifw = FunctionWrapper(iffunc, 3, 'if')

        def isgreater(l):
            if l[0] > l[1]:
                return 1
            else:
                return 0

        gtw = FunctionWrapper(isgreater, 2, 'isgreater')

        return [addw, mulw, ifw, gtw, subw]
