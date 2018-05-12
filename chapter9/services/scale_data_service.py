from models import MatchRow


class ScaleDataService:

    def __init__(self, rows):
        self.rows = rows

    def call(self):
        low = [999999999.0] * len(self.rows[0].data)
        high = [-999999999.0] * len(self.rows[0].data)
        # Find the lowest and highest values
        for row in self.rows:
            d = row.data
            for i in range(len(d)):
                if d[i] < low[i]: low[i] = d[i]
                if d[i] > high[i]: high[i] = d[i]

        # Create a function that scales data
        def scaleinput(d):
            return [(d[i] - low[i]) / (high[i] - low[i]) for i in range(len(low))]

        # Scale all the data
        newrows = [MatchRow(scaleinput(row.data) + [row.match]) for row in self.rows]

        # Return the new data and the function
        return newrows, scaleinput
