class BackPropagateService(object):

    def __init__(self, neural_net, values, inputs, weights, targets, n=5):
        self.neural_net = neural_net
        self.values = values
        self.inputs = inputs
        self.weights = weights
        self.targets = targets
        self.n = n

    def call(self):
        # calculate errors for output layer
        output_deltas = [0.0] * len(self.values[2])
        for k in range(len(self.values[2])):
            error = self.targets[k] - self.inputs[2][k]
            output_deltas[k] = self.neural_net.dtanh(self.inputs[2][k]) * error

        # calculate errors for hidden layer
        hidden_deltas = [0.0] * len(self.values[1])
        for j in range(len(self.values[1])):
            error = 0.0
            for k in range(len(self.values[2])):
                error += output_deltas[k] * self.weights[1][j][k]
            hidden_deltas[j] = self.neural_net.dtanh(self.inputs[1][j]) * error

        # update output weights
        for j in range(len(self.values[1])):
            for k in range(len(self.values[2])):
                change = output_deltas[k] * self.inputs[1][j]
                self.weights[1][j][k] += self.n * change

        # update input weights
        for i in range(len(self.values[0])):
            for j in range(len(self.values[1])):
                change = hidden_deltas[j] * self.inputs[0][i]
                self.weights[0][i][j] += self.n * change

        return self.weights
