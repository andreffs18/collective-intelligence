class GetStrengthService(object):

    LAYER_TABLE_MAP = {
        0: "wordhidden",
        1: "hiddenurl"
    }

    def __init__(self, neural_net, from_id, to_id, layer):
        self.neural_net = neural_net
        self.from_id = from_id
        self.to_id = to_id
        self.layer = layer
        self.table = self.LAYER_TABLE_MAP.get(layer)

    def call(self):
        result = self.neural_net.con.execute(
            "SELECT strength FROM {} WHERE fromid={} AND toid={}".format(self.table, self.from_id, self.to_id)
        ).fetchone()
        if result:
            return result[0]

        if self.layer == 0:
            return -0.2
        elif self.layer == 1:
            return 0.0
        else:
            raise ValueError("Invalid Layer value \"{}\"".format(self.layer))
