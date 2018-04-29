from services import DivideSetService
from services import CalculateEntropyService
from services import CountUniqueElementsService
from models import Node

class BuildTreeService:

    def __init__(self, rows, score_func=None):
        self.rows = rows
        self.score_func = score_func or CalculateEntropyService

    def call(self):

        if not len(self.rows):
            return Node()

        current_score = self.score_func(self.rows).call()

        # Set up some variables to track the best criteria
        best_gain = 0.0
        best_criteria = None
        best_sets = None

        column_count = len(self.rows[0]) - 1
        for col in range(0, column_count):
            # Generate the list of different values in this column
            column_values = {}
            for row in self.rows:
                column_values[row[col]] = 1

            # Now try dividing the rows up for each value in this column
            for value in column_values.keys():
                (set1, set2) = DivideSetService(self.rows, col, value).call()

                # Information gain
                p = float(len(set1)) / len(self.rows)
                gain = current_score - p * self.score_func(set1).call() - (1 - p) * self.score_func(set2).call()
                if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                    best_gain = gain
                    best_criteria = (col, value)
                    best_sets = (set1, set2)

        # Create the sub branches
        if best_gain > 0:
            true_branch = BuildTreeService(best_sets[0], score_func=self.score_func).call()
            false_branch = BuildTreeService(best_sets[1], score_func=self.score_func).call()
            return Node(col=best_criteria[0], value=best_criteria[1], tb=true_branch, fb=false_branch)
        else:
            return Node(results=CountUniqueElementsService(self.rows).call())
