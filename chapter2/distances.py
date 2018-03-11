# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
To check more distance silimaritie functions go here

https://en.wikipedia.org/wiki/Metric_%28mathematics%29#Examples
http://ag.arizona.edu/classes/rnr555/lecnotes/10.html
http://dataaspirant.com/2015/04/11/five-most-popular-similarity-measures-implementation-in-python/
"""
from math import sqrt, pow

def euclidean(dataset, u1, u2):
    """Get distance between user1 and user2"""
    shared_movies = {}
    # for each movie id in user1
    for movie in dataset[u1]:
        if movie in dataset[u2]:
            shared_movies[movie] = {'u1': u1, 'u2': u2}
    # no movies in common
    if len(shared_movies) == 0:
        return 0
    # add up all the squares of all rating diferences
    sum_of_squares = sum([pow(dataset[users.get('u1')][movie] -
                              dataset[users.get('u2')][movie], 2)
                          for movie, users in shared_movies.iteritems()
                          if movie in dataset[users.get('u2')]])
    # return 1/(sqrt(1+sum_of_squares)) whats on the book
    return 1 / (1 + sqrt(sum_of_squares))



def pearson(dataset, u1, u2):
    """Calculates and returns pearson correlation coefficient between user1 and user2"""
    # get list of mutual rated items
    shared_movies = dict((movie, 1)
                         for movie in dataset[u1]
                         if movie in dataset[u2])
    # if they are no ratings in common, return 0
    if len(shared_movies) == 0:
        return 0
    # add up all the preferneces
    sum_u1 = sum([dataset[u1][movie] for movie in shared_movies])
    sum_u2 = sum([dataset[u2][movie] for movie in shared_movies])
    # sum up all the squares
    sum_u1_pow = sum([pow(dataset[u1][movie], 2) for movie in shared_movies])
    sum_u2_pow = sum([pow(dataset[u2][movie], 2) for movie in shared_movies])
    # sum up the products
    prod_sum = sum([dataset[u1][movie] * dataset[u2][movie] for movie in shared_movies])
    # calculate pearson score
    n = len(dataset)
    num = prod_sum - ((sum_u1 * sum_u2) / n)
    den = sqrt((sum_u1_pow - pow(sum_u1, 2) / n) * (sum_u2_pow - pow(sum_u2, 2) / n))
    if den == 0:
        return 0
    return num / den


def jaccard(dataset, u1, u2):
    """
    https://en.wikipedia.org/wiki/Jaccard_index
    http://people.revoledu.com/kardi/tutorial/Similarity/Jaccard.html
    """
    raise NotImplementedError()


def manhattan(dataset, u1, u2):
    """
    http://www.improvedoutcomes.com/docs/WebSiteDocs/Clustering/Clustering_Parameters/Manhattan_Distance_Metric.htm
    http://simeon.wikia.com/wiki/Manhattan_distance
    """
    raise NotImplementedError()
