class LoadCSVService:

    def __init__(self, standard=False, filename="data.csv"):
        self.standard = standard
        self.filename = filename

    def call(self):
        """
        For this example purpuses, we return the book example, instead of reading an actual file.
        """
        if not self.standard:
            return self._baseball()

        # ['Referrer', 'Location', 'Read FAQ', 'Page Viewed', 'Pricing Plan']
        return [
            ['slashdot', 'USA', 'yes', 18, 'None'],
            ['google', 'France', 'yes', 23, 'Premium'],
            ['digg', 'USA', 'yes', 24, 'Basic'],
            ['kiwitobes', 'France', 'yes', 23, 'Basic'],
            ['google', 'UK', 'no', 21, 'Premium'],
            ['(direct)', 'New Zealand', 'no', 12, 'None'],
            ['(direct)', 'UK', 'no', 21, 'Basic'],
            ['google', 'USA', 'no', 24, 'Premium'],
            ['slashdot', 'France', 'yes', 19, 'None'],
            ['digg', 'USA', 'no', 18, 'None'],
            ['google', 'UK', 'no', 18, 'None'],
            ['kiwitobes', 'UK', 'no', 19, 'None'],
            ['digg', 'New Zealand', 'yes', 12, 'Basic'],
            ['slashdot', 'UK', 'no', 21, 'None'],
            ['google', 'UK', 'yes', 18, 'Basic'],
            ['kiwitobes', 'France', 'yes', 19, 'Basic']
        ]

    def _baseball(self):
        """
        From https://github.com/jayelm/decisiontrees/blob/master/example_data/baseball.csv
        """
        data = """Outlook,Temperature,Humidity,Wind,Play ball?
Sunny,Hot,High,Weak,No
Sunny,Hot,High,Strong,No
Overcast,Hot,High,Weak,Yes
Rain,Mild,High,Weak,Yes
Rain,Cool,Normal,Weak,Yes
Rain,Cool,Normal,Strong,No
Overcast,Cool,Normal,Strong,Yes
Sunny,Mild,High,Weak,No
Sunny,Cool,Normal,Weak,Yes
Rain,Mild,Normal,Weak,Yes
Sunny,Mild,Normal,Strong,Yes
Overcast,Mild,High,Strong,Yes
Overcast,Hot,Normal,Weak,Yes
Rain,Mild,High,Strong,No"""
        # clean data
        data = data.split("\n")
        data = filter(None, data)
        data = map(lambda d: d.strip().split(","), data)
        return data[1:]