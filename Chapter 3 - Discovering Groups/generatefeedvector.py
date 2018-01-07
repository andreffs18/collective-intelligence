import feedparser
import re

feedlist = [
    'http://feeds.feedburner.com/porfalarnoutracoisa',
    'http://www.marinamele.com/feed',
    'http://feeds.feedburner.com/makeuseof',
    'http://feeds.feedburner.com/jumbojoke',
    'http://feeds.gawker.com/lifehacker/full',
]

def get_word_counts(url):
    # Parse the feed
    d = feedparser.parse(url)
    counter = {}

    # Loop over all entries
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description

        # Extract list of words
        words = get_words(e.title + ' ' + summary)
        for word in words:
            counter.setdefault(word, 0)
            counter[word] += 1

    return d.feed.title, counter


def get_words(html):
    # Remove all html tags
    txt = re.compile(r'<[^>]+>').sub('', html)
    # Split words by all non-alpha caracters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    # Conver to lower case
    return [word.lower() for word in words if word != '']

apcount = {}
wordcounts = {}
for feedurl in feedlist:
    title, wc = get_word_counts(feedurl)
    wordcounts[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1



wordlist = []
for w, bc in apcount.items():
    frac = float(bc)/len(feedlist)
    if frac > 0.1 and frac < 0.5:
        wordlist.append(w)

out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist:
    out.write('\t{}'.format(word))
out.write('\n')
for blog, wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t{}'.format(wc[word]))
        else:
            out.write('\t0')
    out.write('\n')




