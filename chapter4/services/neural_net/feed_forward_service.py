from math import tanh


class FeedForwardService(object):

    def __init__(self, values, inputs, weights):
        self.values = values
        self.inputs = inputs
        self.weights = weights

    def call(self):
        # the only inputs are the query words
        for i in range(len(self.values[0])):
            self.inputs[0][i] = 1.0

        # hidden activations
        for j in range(len(self.values[1])):
            sum = 0.0
            for i in range(len(self.values[0])):
                sum += self.inputs[0][i] * self.weights[0][i][j]
            self.inputs[1][j] = tanh(sum)

        # output activations
        for k in range(len(self.values[2])):
            sum = 0.0
            for j in range(len(self.values[1])):
                sum += self.inputs[1][j] * self.weights[1][j][k]
            self.inputs[2][k] = tanh(sum)

        return (self.values, self.inputs, self.weights)
