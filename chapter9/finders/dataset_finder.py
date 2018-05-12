from models import MatchRow


class DatasetFinder:

    @classmethod
    def load_match(cls, filename, all_numerical=False):
        """"""
        rows = []
        for line in file(filename):
            row = MatchRow(line.split(","), all_numerical)
            rows.append(row)
        return rows
