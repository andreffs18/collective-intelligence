class GetAllHiddenIdsService(object):

    def __init__(self, neural_net, word_ids, urls_ids):
        self.neural_net = neural_net
        self.word_ids = word_ids
        self.urls_ids = urls_ids

    def call(self):
        l1 = {}
        for word_id in self.word_ids:
            rows = self._get_from_nn("toid", "wordhidden", "fromid", word_id)
            for row in rows:
                l1[row[0]] = 1

        for url_id in self.urls_ids:
            rows = self._get_from_nn("fromid", "hiddenurl", "toid", url_id)
            for row in rows:
                l1[row[0]] = 1

        return l1.keys()

    def _get_from_nn(self, table, field, clause, value):
        return self.neural_net.con.execute("SELECT {} FROM {} WHERE {}={}".format(table, field, clause, value))
