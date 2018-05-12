class MatchRow:

    def __init__(self, row, all_numerical=False):
        if all_numerical:
            self.data = [float(row[i]) for i in range(len(row) - 1)]
        else:
            self.data = row[0:len(row) - 1]

        self.match = int(row[len(row) - 1])