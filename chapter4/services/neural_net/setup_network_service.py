class SetupNetworkService(object):

    def __init__(self, neural_net, word_ids, url_ids):
        self.neural_net = neural_net
        self.word_ids = word_ids
        self.url_ids = url_ids

    def call(self):
        hidden_ids = self.neural_net.get_all_hidden_ids(self.word_ids, self.url_ids)

        # node outputs
        a_input = [1.0] * len(self.word_ids)
        a_hidden = [1.0] * len(hidden_ids)
        a_output = [1.0] * len(self.url_ids)

        # weight matrix
        weight_input = [[self.neural_net.get_strength(word_id, hidden_id, 0)
                         for hidden_id in hidden_ids]
                        for word_id in self.word_ids]
        weight_output = [[self.neural_net.get_strength(hidden_id, url_id, 1)
                          for url_id in self.url_ids]
                         for hidden_id in hidden_ids]
        # return tuple of values, nodes and weights
        return ((self.word_ids, hidden_ids, self.url_ids),
                (a_input, a_hidden, a_output),
                (weight_input, weight_output))
