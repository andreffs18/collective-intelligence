from random import randint

class BuildHiddenDatasetService:

    def __init__(self, dataset_size=200, x_interval=[0, 40], y_interval=[0, 40]):
        self.dataset_size = dataset_size
        self.x_interval = x_interval
        self.y_interval = y_interval

    @staticmethod
    def _hidden_function(x, y):
        return x ** 2 + 2 * y + 3 * x + 5

    def call(self):
        rows = []
        for i in range(self.dataset_size):
            x = randint(*self.x_interval)
            y = randint(*self.y_interval)
            rows.append([x, y, self._hidden_function(x, y)])
        return rows
