from random import random


class DivideDataService:
    def __init__(self, data, test_racio=0.05):
        self.data = data
        self.test_racio = test_racio

    def call(self):
        train_set = []
        test_set = []
        for row in self.data:
            if random() < self.test_racio:
                test_set.append(row)
            else:
                train_set.append(row)
        return train_set, test_set


class TestAlgorithmService:
    def __init__(self, algorithm, data=None, train_set=None, test_set=None):
        self.algorithm = algorithm
        self.data = data
        self.train_set = train_set
        self.test_set = test_set

        if not data:
            if not train_set and not test_set:
                raise ValueError("If no data is given, train_set and test_set are required!")

        if data:
            self.train_set, self.test_set = DivideDataService(data).call()

    def call(self):
        error = 0.0
        for row in self.test_set:
            guess = self.algorithm(self.train_set, row['input'])
            error += (row['result'] - guess) ** 2
        return error / len(self.test_set)


class CrossValidateService:
    def __init__(self, algorithm, data, trials=100, test=0.1):
        self.algorithm = algorithm
        self.data = data
        self.trials = trials
        self.test = test

    def call(self):
        error = 0.0
        for i in range(self.trials):
            error += TestAlgorithmService(self.algorithm, self.data).call()
        return error / self.trials
