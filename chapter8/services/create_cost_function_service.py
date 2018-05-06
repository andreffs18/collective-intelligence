
class RescaleDatasetService:
    def __init__(self, data, scale):
        self.data = data
        self.scale = scale

    def call(self):
        scaled_data = []
        for row in self.data:
            scaled = [self.scale[i] * row['input'][i]
                      for i in range(len(self.scale))]
            scaled_data.append({
                'input': scaled,
                'result': row['result']
            })
        return scaled_data


class CreateCostFunctionService:
    def __init__(self, algorithm, data, scale, trials=20):
        self.algorithm = algorithm
        self.data = data
        self.scale = scale
        self.trials = trials

    def call(self):
        from services import CrossValidationService
        data = RescaleDatasetService(self.data, self.scale)
        return CrossValidationService(self.algorithm, data, trials=self.trials)

