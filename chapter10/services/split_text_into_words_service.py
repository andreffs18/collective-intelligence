import re


class SplitTextIntoWordsService:
    def __init__(self, text):
        self.text = text

    def call(self):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(self.text) if len(s) > 3]

