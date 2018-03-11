import feedparser
import re
from collections import Counter
from tqdm import tqdm

feedlist = [
    'http://feeds.feedburner.com/porfalarnoutracoisa',
    'http://www.marinamele.com/feed',
    'http://feeds.feedburner.com/makeuseof',
    'http://feeds.feedburner.com/jumbojoke',
    'http://feeds.gawker.com/lifehacker/full',
    "http://feeds.feedburner.com/DicasDeTreino",
    "http://feeds.feedburner.com/neilarey",
    "http://www.musculacao.net/feed/",
    "http://shariblaukopf.com/feed/",
    "http://feeds.feedburner.com/TheDoughRoller",
    "https://www.forumfinancas.pt/forum/10-poupar-dinheiro.xml/",
    "http://www.nomorewaffles.com/feed/",
    "https://www.forumfinancas.pt/forum/7-investimentos.xml/",
    "http://www.empiricus.com.br/feed/",
    "https://www.forumfinancas.pt/forum/20-bancos.xml/",
    "http://blogempiricus.blogspot.com/feeds/posts/default",
    "http://feeds.feedburner.com/pedropais",
    "http://feeds.feedburner.com/investidor-pt",
    "http://feeds.feedburner.com/DocumentaryHeaven",
    "http://feeds.feedburner.com/DocumentariesRssFeed",
    "http://www.docspt.com/index.php?type=rss;action=.xml;sa=news;limit=20",
    "http://feeds.feedburner.com/c7nema",
    "http://feeds.topdocumentaryfilms.com/TopDocumentaryFilms",
    "http://www.djangosnippets.org/feeds/latest/",
    "http://blog.jetbrains.com/pycharm/feed/",
    "http://feeds.feedburner.com/ProgrammableWeb",
    "http://www.hackerfactor.com/blog/index.php?/feeds/index.rss2",
    "http://www.djangoproject.com/rss/weblog/",
    "http://pyvideo.org/feeds/all.atom.xml",
    "https://realpython.com/atom.xml",
    "http://feeds.feedburner.com/Pyimagesearch",
    "http://feeds.feedburner.com/WebDesignLedger",
    "http://www.unheap.com/feed/",
    "http://feeds.feedburner.com/speckboy-design-magazine",
    "http://feeds2.feedburner.com/Webappers",
    "http://feeds.feedburner.com/alistapart/main",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCNYrK4tc5i1-eL8TXesH2pg",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC5O84sz_dGXE0kPGr0Cdofg",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCX6b17PVsYBQ0ip5gyeme-Q",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCduKuJToxWPizJ7I2E6n1kA",
    "https://www.youtube.com/playlist?list=UUekQr9znsk2vWxBo3YiLq2w",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCbochVIwBCzJb9I2lLGXGjQ",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCxrd1I7wmE2chwpoqD4DSTA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCOYWgypDktXdb-HfZnSMK6A",
    "https://www.youtube.com/playlist?list=UUNwpsnvl4W7s1pGsUfRGwPw",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCUHW94eEFW7hkUMVaZz4eDg",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCWXCrItCF6ZgXrdozUS-Idw",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC9Ntx-EF3LzKY1nQ5rTUP2g",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCadiU6WTKl65HUwEih1XLYg",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCVJK2AT3ea5RTXNRjX_kz8A",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCiC9uvJxy0Ax5-jcd5QDkmA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCBB-sWImDYCl_AxDRI956Lw",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCt_t6FwNsqr3WWoL6dFqG9w",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCn8zNIfYAQNdrFRrr8oibKw",
    "https://www.youtube.com/playlist?list=UUq6aw03lNILzV96UvEAASfQ",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCJ0-OtVpF0wOKEqT2Z1HEtA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC9kMnSZQd53hE-1sb1f9sdA",
    "https://www.youtube.com/playlist?list=PLH5Nb1HOTXfzdE0Bmc2c1M7GY-6ETEjUs",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC6nSFpj9HTCZ5t-N3Rm3-HA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCC552Sd-3nyi_tk2BudLUzA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCsXVk37bltHxD1rDPwtNM8Q",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCeE3lj6pLX_gCd0Yvns517Q",
    "https://www.youtube.com/playlist?list=UULG2sesmHKHC6ZpM1lBdQEQ",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCUKi4zY5ETSqrKAjTBgjM-g",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCIh6suDBrM7H8kIiiHkYXfA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCVVAnxQ2YMC_qlc7QfPA2YQ",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCR4s1DE9J4DHzZYXMltSMAg",
    "https://www.youtube.com/playlist?list=UUwe6Xe92HwbMNuthIen9e9g",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCH6vXjt-BA7QHl0KnfL-7RQ",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCqDSLtXeZsGc3dtVb5MW13g",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCuXUSj8lBpcJPI5h0CbeMjA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCr3cBLTYmIK9kY0F_OdFWFQ",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCJbPGzawDH1njbqV-D5HqKw",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UChT-l10Pm5m-xOeYOl_37Xw",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCsooa4yRKGN_zEE8iknghZA",
    "http://lucumr.pocoo.org/feed.atom",
    "http://martinfowler.com/bliki/bliki.atom",
    "http://bost.ocks.org/mike/index.rss",
    "https://www.rdegges.com/index.xml",
    "http://peadarcoyle.wordpress.com/feed/",
    "http://feeds.feedburner.com/porfalarnoutracoisa",
    "http://feeds.feedburner.com/FlowingData",
    "http://www.sarahmei.com/blog/feed/",
    "http://jamesclear.com/feed",
    "http://www.nelsoncarvalheiro.com/blog/feed/",
    "http://minimaxir.com/rss.xml",
    "http://www.marinamele.com/feed",
    "http://feeds.feedburner.com/nvie",
    "http://simblob.blogspot.com/feeds/posts/default",
    "http://feeds.feedburner.com/expresso-geral",
    "http://www.publico.clix.pt/rss.asp?idCanal=10",
    "http://diferencial.tecnico.pt/feed/",
    "https://medium.com/feed/hacker-daily",
    "http://hnbest.heroku.com/rss",
    "http://oneplus.net/blog/feed/",
    "http://macro.ycombinator.com/feed.xml",
    "http://www.ondelisboa.com/feed/",
    "http://www.worldofwanderlust.com/feed/",
]


def get_word_counts(url):
    """From given url, parse html and extract all word count"""
    # Parse the feed
    d = feedparser.parse(url)
    list_of_words = []

    # Loop over all entries
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description

        # Extract list of words
        words = get_words(e.title + ' ' + summary)
        list_of_words.extend(words)

    return Counter(list_of_words)


def get_words(html):
    # Remove all html tags
    txt = re.compile(r'<[^>]+>').sub('', html)
    # Split words by all non-alpha caracters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    # Conver to lower case
    return map(lambda word: word.lower(), filter(None, words))


def generate_word_file(filename='blogdata.txt'):
    print('Build dictionary of key = "word" value = "nr_of_words" for all urls in "feedlist"...')
    apcount = {}
    wordcounts = {}
    for feedurl in feedlist:
        wc = get_word_counts(feedurl)
        wordcounts[feedurl] = wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1

    print("Calculate % of words on the whole document...")
    wordlist = []
    for w, wc in apcount.items():
        # frac = float(wc) / len(feedlist)
        # if frac > 0.1 and frac < 0.5:
        wordlist.append(w)

    print("Writing info into \"{}\".".format(filename))
    with file(filename, 'w') as out:
        out.write('Blog')
        for word in wordlist:
            out.write('\t{}'.format(word))
        out.write('\n')

        for url, wc in wordcounts.items():
            out.write(url)
            for word in wordlist:
                if word in wc:
                    out.write('\t{}'.format(wc[word]))
                else:
                    out.write('\t0')
            out.write('\n')


def readfile(filename):
    lines = [line for line in file(filename)]

    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this rows is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data

