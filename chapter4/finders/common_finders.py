class CommonFinders(object):

    @classmethod
    def get_ignore_words(cls):
        return set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
