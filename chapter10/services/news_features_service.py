import codecs
import feedparser

from services.split_text_into_words_service import SplitTextIntoWordsService


class NewsFeaturesService:

    def __init__(self, filepath):
        self.filepath = filepath
        self.article_titles = []
        self.article_words = []
        self.all_words = {}

    def _get_feedlist(self):
        with codecs.open(self.filepath, "rb", "utf8") as feedlist:
            feedlist = feedlist.readlines()
        return feedlist

    def _handle_feed(self, feed, feed_counter):
        # Loop over every article
        for e in feed.entries:
            # Ignore identical articles
            if e.title in self.article_titles:
                continue

            # Extract the words
            txt = e.title.encode('utf8') + stripHTML(e.description.encode('utf8'))
            words = SplitTextIntoWordsService(txt).call()
            self.article_words.append({})
            self.article_titles.append(e.title)

            # Increase the counts for this word in allwords and in articlewords
            for word in words:
                self.all_words.setdefault(word, 0)
                self.all_words[word] += 1
                self.article_words[feed_counter].setdefault(word, 0)
                self.article_words[feed_counter][word] += 1

    def call(self):
        # Loop over every feed
        for counter, feed in enumerate(self._get_feedlist()):
            f = feedparser.parse(feed)
            self._handle_feed(f, counter)

        return self.all_words, self.article_words, self.article_titles


def stripHTML(h):
    p = ''
    s = 0
    for c in h:
        if c == '<':
            s = 1
        elif c == '>':
            s = 0
            p += ' '
        elif s == 0:
            p += c
    return p




from numpy import *


def showfeatures(w, h, titles, wordvec, out='features.txt'):
    outfile = file(out, 'w')
    pc, wc = shape(h)
    toppatterns = [[] for i in range(len(titles))]
    patternnames = []

    # Loop over all the features
    for i in range(pc):
        slist = []
        # Create a list of words and their weights
        for j in range(wc):
            slist.append((h[i, j], wordvec[j]))
        # Reverse sort the word list
        slist.sort()
        slist.reverse()

        # Print the first six elements
        n = [s[1] for s in slist[0:6]]
        outfile.write(str(n) + '\n')
        patternnames.append(n)

        # Create a list of articles for this feature
        flist = []
        for j in range(len(titles)):
            # Add the article with its weight
            flist.append((w[j, i], titles[j]))
            toppatterns[j].append((w[j, i], i, titles[j]))

        # Reverse sort the list
        flist.sort()
        flist.reverse()

        # Show the top 3 articles
        for f in flist[0:3]:
            outfile.write(str(f) + '\n')
        outfile.write('\n')

    outfile.close()
    # Return the pattern names for later use
    return toppatterns, patternnames


def showarticles(titles, toppatterns, patternnames, out='articles.txt'):
    outfile = file(out, 'w')

    # Loop over all the articles
    for j in range(len(titles)):
        outfile.write(titles[j].encode('utf8') + '\n')

        # Get the top features for this article and
        # reverse sort them
        toppatterns[j].sort()
        toppatterns[j].reverse()

        # Print the top three patterns
        for i in range(3):
            outfile.write(str(toppatterns[j][i][0]) + ' ' +
                          str(patternnames[toppatterns[j][i][1]]) + '\n')
        outfile.write('\n')

    outfile.close()
