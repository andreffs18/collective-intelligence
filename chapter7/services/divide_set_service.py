from math import log
from services import CountUniqueElementsService


class DivideSetService:

    def __init__(self, rows, column, value):
        self.rows = rows
        self.column = column
        self.value = value

    def match(self, element, value):
        """
        Use string comparison if value is basestring, otherwise (int or float) use bigger or equal
        """
        if isinstance(value, basestring):
            return element == value

        if isinstance(value, int) or isinstance(value, float):
            return element >= value

        raise TypeError("Value \"{}\" ({}) is neither basestring, int or float.".format(value, type(value)))

    def call(self):
        """
        Divides a set on a specific column. Can handle numeric or nominal values
        """
        set1 = list()
        set2 = list()

        for row in self.rows:
            element = row[self.column]
            if self.match(element, self.value):
                set1.append(row)
            else:
                set2.append(row)

        return set1, set2
