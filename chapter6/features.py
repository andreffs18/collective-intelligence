import re
import math

def get_words(document, min_words=2, max_words=20):
    """
    From given document (string) return list of words between min_words and max_words
    """
    splitter = re.compile('\\W*')
    # Split the words by non-alpha characters and lower splitted words
    words = splitter.split(document)
    words = map(lambda w: w.lower(), words)
    # Only words that are between "min_words" and "max_words" characters
    words = filter(lambda w: min_words < len(w) < max_words, words)
    # Return the unique set of words only
    words = list(set(words))
    return dict(map(lambda w: (w, 1), words))


def entry_features(entry):
    """
    From a given entry return complex dictionary of features
    """
    features = {}
    # Extract the title words and annotate
    for w, c in get_words(entry['title']).items():
        features['Title:' + w] = c

    # Extract the summary words
    upper_count = 0
    summary_words = get_words(entry['summary']).items()
    for i, (w, c) in enumerate(summary_words):
        features[w] = c
        if w.isupper():
            upper_count += 1

        if i < len(summary_words) - 1:
            two_words = " ".join(map(lambda w: w[0], summary_words[i:i + 1]))
            features[two_words] = 1

    # Keep creator and publisher whole
    features['Publisher:' + entry['publisher']] = 1

    # UPPERCASE is a virtual word flagging too much shouting
    if float(upper_count) / len(summary_words) > 0.3:
        features['UPPERCASE'] = 1
    return features
