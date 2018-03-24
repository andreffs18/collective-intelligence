from services.neural_net.make_tables_service import MakeTablesService
from services.neural_net.get_strength_service import GetStrengthService
from services.neural_net.set_strength_service import SetStrengthService
from services.neural_net.generate_hidden_node_service import GenerateHiddenNodeService
from services.neural_net.get_all_hidden_ids_service import GetAllHiddenIdsService
from services.neural_net.setup_network_service import SetupNetworkService
from services.neural_net.feed_forward_service import FeedForwardService
from services.neural_net.back_propagate_service import BackPropagateService
from services.neural_net.update_database_service import UpdateDatabaseService
from sqlite3 import dbapi2 as sqlite


class SearchNet(object):

    def __init__(self, dbname="nn.db"):
        """
        Initialize the Crawler with the name of the database
        """
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def dtanh(self, y):
        """
        Return the slope of the given tanh result
        """
        return 1.0 - y * y

    def make_tables(self):
        """
        Create initial tables for Neural Network
        """
        MakeTablesService(self).call()

    def get_strength(self, from_id, to_id, layer):
        """
        Get strength of link from given layer (0 or 1)
        """
        return GetStrengthService(self, from_id, to_id, layer).call()

    def set_strength(self, from_id, to_id, layer, strength):
        """
        Set strength of link from given layer (0 or 1)
        """
        return SetStrengthService(self, from_id, to_id, layer, strength).call()

    def generate_hidden_node(self, word_ids, urls):
        """
        From given list of word_ids and urls, generate hidden nodes
        """
        return GenerateHiddenNodeService(self, word_ids, urls).call()

    def get_all_hidden_ids(self, word_ids, urls_ids):
        """
        Return all hidden nodes from nn database ids
        """
        return GetAllHiddenIdsService(self, word_ids, urls_ids).call()


    def train_query(self, word_ids, url_ids, selected_url, n=0.5):
        """
        Training algorithm
        """
        # populate database with network information
        GenerateHiddenNodeService(self, word_ids, url_ids).call()
        # setup network in memory
        values, inputs, weights = SetupNetworkService(self, word_ids, url_ids).call()
        # send values thought network
        values, inputs, weights = FeedForwardService(values, inputs, weights).call()
        # update targets with expected result
        targets = [0.0] * len(url_ids)
        targets[url_ids.index(selected_url)] = 1.0
        # run back propagation to fix network
        update_weights = BackPropagateService(self, values, inputs, weights, targets, n).call()
        UpdateDatabaseService(self, values, update_weights).call()

    def get_results(self, word_ids, url_ids):
        """
        Given list of words and urls, runs "setup_network" and pushes all inputs through the network
        """
        values, inputs, weights = SetupNetworkService(self, word_ids, url_ids).call()
        _, inputs, _ = FeedForwardService(values, inputs, weights).call()
        return inputs[2][:]
