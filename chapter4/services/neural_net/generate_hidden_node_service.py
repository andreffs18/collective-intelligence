class GenerateHiddenNodeService(object):

    def __init__(self, neural_net, word_ids, urls):
        self.neural_net = neural_net
        self.word_ids = word_ids
        self.urls = urls

    def call(self):
        if len(self.word_ids) > 3:
            return None

        # Check if we already created a note for this set of words
        create_key = "_".join(sorted(map(str, self.word_ids)))
        if self._is_already_created(create_key):
            return None

        hidden_id = self._create_new_hidden_key(create_key)
        for word_id in self.word_ids:
            self.neural_net.set_strength(word_id, hidden_id, 0, 1.0 / len(self.word_ids))
        for url_id in self.urls:
            self.neural_net.set_strength(hidden_id, url_id, 1, 0.1)

        self.neural_net.con.commit()

    def _is_already_created(self, create_key):
        return self.neural_net.con.execute(
            "SELECT rowid FROM hiddennode WHERE create_key='{}'".format(create_key)
        ).fetchone() is not None

    def _create_new_hidden_key(self, create_key):
        return self.neural_net.con.execute(
            "INSERT INTO hiddennode (create_key) VALUES ('{}')".format(create_key)
        ).lastrowid
