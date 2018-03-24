class UpdateDatabaseService(object):

    def __init__(self, neural_net, values, new_weights):
        self.neural_net = neural_net
        self.values = values
        self.new_weights = new_weights

    def call(self):

        for i in range(len(self.values[0])):
            for j in range(len(self.values[1])):
                self.neural_net.set_strength(
                    self.values[0][i],
                    self.values[1][j],
                    0,
                    self.new_weights[0][i][j]
                )

        for j in range(len(self.values[1])):
            for k in range(len(self.values[2])):
                self.neural_net.set_strength(
                    self.values[1][j],
                    self.values[2][k],
                    1,
                    self.new_weights[1][j][k]
                )
        self.neural_net.con.commit()
