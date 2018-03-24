import re


class SeparateWordsService(object):

    def __init__(self,  text):
        self.text = text

    def call(self):
        splitter = re.compile("\\W*")
        output = []
        for s in splitter.split(self.text):
            if s != '':
                output.append(s.lower())
        return output
