# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Created by andresilva on 9/21/16

To check more distance silimaritie functions go here

https://en.wikipedia.org/wiki/Metric_%28mathematics%29#Examples
http://ag.arizona.edu/classes/rnr555/lecnotes/10.html
http://dataaspirant.com/2015/04/11/five-most-popular-similarity-measures-implementation-in-python/
"""
import math

def euclidean(dataset, u1, u2):
    """Get distance between item1 and item2"""
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
    return 1/(1+sqrt(sum_of_squares))



def pearson(dataset, u1, u2):
    """calculates and returns pearson correlation coefficient for p1 and p2"""
    # get list of mutual rated items
    shared_movies = dict((movie, 1)
                         for movie in dataset[u1]
                         if movie in dataset[u2])
    # if they are no ratings in common, return 0
    if len(shared_movies) == 0:
        return 0
    # add up all the preferneces
    sum_p1 = sum([dataset[u1][movie] for movie in shared_movies])
    sum_p2 = sum([dataset[u2][movie] for movie in shared_movies])
    # sum up all the squares
    sum_p1_pow = sum([pow(dataset[u1][movie], 2) for movie in shared_movies])
    sum_p2_pow = sum([pow(dataset[u2][movie], 2) for movie in shared_movies])
    # sum up the products
    prod_sum = sum([dataset[u1][movie] * dataset[u2][movie]
                    for movie in shared_movies])
    # calculate persaon score
    num = prod_sum - (sum_p1 * sum_p2)/n
    den = math.sqrt((sum_p1_pow - pow(sum_p1, 2)/n) *
                    (sum_p2_pow - pow(sum_p2, 2)/n))
    if den == 0:
        return 0
    return num/den


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


__author__ = "andresilva"
__email__ = "andre@unbabel.com"
