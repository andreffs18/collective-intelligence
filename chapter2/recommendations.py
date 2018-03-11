import math
import random
from distances import pearson, euclidean


def transform_dataset(dataset):
    """invert json"""
    result = {}
    for person in dataset:
        for item in dataset[person]:
            result.setdefault(item, {})

            # flip item and person
            result[item][person] = dataset[person][item]
    return result


def top_matches(dataset, person, n=5, similarity=pearson):
    """return the best matches for a person from the dataset dictionary
    number of results and similarity function are optional params"""
    scores = [(similarity(dataset, person, other), other)
              for other in dataset if other != person]
    # sort the list so the highest score appear on top
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommendations(dataset, person, similarity=pearson):
    """get recommendations for a person by using a weighted average of every
    other user's rankings"""
    totals = {}
    sim_sums = {}
    for other in dataset:
        # not me
        if other == person:
            continue
        sim = similarity(dataset, person, other)
        # ignore below or equal to zero
        if sim <= 0:
            continue
        for item in dataset[other]:
            # only score movies i haven't seen yet
            if item not in dataset[person] or dataset[person][item] == 0:
                # similarity * score
                totals.setdefault(item, 0)
                totals[item] += dataset[other][item] * sim
                # sum
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim
    # create normalize list
    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]

    # return sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def calculate_similar_items(dataset, n=10, similarity=euclidean):
    """create dataset of items instead of persons create a dicitonary of items
    showing which other items they are most similar to"""
    result = {}
    # invert the preference matrix to be item centric
    item_dataset = transform_dataset(dataset)
    c = 0
    for item in item_dataset:
        # status updates for large datasets
        c += 1
        if c % 100 == 0:
            print "{}/{}".format(c, len(item_dataset))

        # find the most_similar items to this one
        scores = top_matches(item_dataset, item, n=n, similarity=similarity)
        result[item] = scores
    return result


def get_recommended_items(dataset, item_match, user):
    """"""
    user_ratings = dataset[user]
    scores = {}
    total_sim = {}

    # loop over items rated by this user
    for (item, rating) in user_ratings.items():
        # loop over items similar to this one
        for (similarity, item2) in item_match[item]:
            # ignore if this user has already rated this item
            if item2 in user_ratings:
                continue

            # weighted sum of rating time similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # sum of all the similarities
            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity
    # divide each total score by total wieghting to et an average
    rankings = [(score / total_sim[item], item)
                for item, score in scores.items()]
    # return ordered rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings
