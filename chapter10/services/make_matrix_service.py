
class MakeMatrixService:

    def __init__(self, all_words, article_words):
        self.all_words = all_words
        self.article_words = article_words

    def call(self):
        word_vector = []

        # Only take words that are common but not too common
        for w, c in self.all_words.items():
            if 3 < c < len(self.article_words) * 0.6:
                word_vector.append(w)

        # Create the word matrix
        matrix = [[(word in f and f[word] or 0)
                   for word in word_vector]
                  for f in self.article_words]
        return matrix, word_vector

