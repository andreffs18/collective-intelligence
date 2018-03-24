class SetStrengthService(object):

    LAYER_TABLE_MAP = {
        0: "wordhidden",
        1: "hiddenurl"
    }

    def __init__(self, neural_net, from_id, to_id, layer, strength):
        self.neural_net = neural_net
        self.from_id = from_id
        self.to_id = to_id
        self.layer = layer
        self.table = self.LAYER_TABLE_MAP.get(layer)
        self.strength = strength

    def call(self):
        result = self.neural_net.con.execute(
            "SELECT rowid FROM {} WHERE fromid={} AND toid={}".format(self.table, self.from_id, self.to_id)
        ).fetchone()
        if result:
            row_id = result[0]
            return self.neural_net.con.execute(
                "UPDATE {} SET strength={} WHERE rowid={}".format(self.table, self.strength, row_id))

        return self.neural_net.con.execute(
            "INSERT INTO {} (fromid, toid, strength) VALUES ({}, {}, {})".format(
                self.table, self.from_id, self.to_id, self.strength))
