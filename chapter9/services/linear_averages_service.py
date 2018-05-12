class LinearAveragesService:

    def __init__(self, dataset):
        self.dataset = dataset

    def call(self):
        averages = {}
        counts = {}

        for row in self.dataset:
            # Get the class of this point
            cl = row.match

            averages.setdefault(cl, [0.0] * (len(row.data)))
            counts.setdefault(cl, 0)

            # Add this point to the averages
            for i in range(len(row.data)):
                averages[cl][i] += float(row.data[i])

            # Keep track of how many points in each class
            counts[cl] += 1

        # Divide sums by counts to get the averages
        for cl, avg in averages.items():
            for i in range(len(avg)):
                avg[i] /= counts[cl]

        return averages
