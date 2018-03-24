class MakeTablesService(object):

    def __init__(self, neural_net):
        self.neural_net = neural_net

    def call(self):
        self.neural_net.con.execute("CREATE TABLE IF NOT EXISTS wordhidden(fromid, toid, strength)")
        self.neural_net.con.execute("CREATE TABLE IF NOT EXISTS hiddennode(create_key)")
        self.neural_net.con.execute("CREATE TABLE IF NOT EXISTS hiddenurl(fromid, toid, strength)")
        self.neural_net.con.commit()
