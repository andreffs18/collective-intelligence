# !/usr/bin/python
# -*- coding: utf-8 -*-
from math import sqrt, pow


def pearson(v1, v2):
    """Calculates and returns pearson correlation coefficient between two sets of data"""
    # sum all elements for each value
    sum_v1 = sum(v1)
    sum_v2 = sum(v2)
    # sum up all the squares
    sum_v1_pow = sum([pow(v, 2) for v in v1])
    sum_v2_pow = sum([pow(v, 2) for v in v2])
    # sum up the products
    prod_sum = sum([v1[i] * v2[i] for i in range(len(v1))])
    # calculate pearson score
    n = len(v1)
    num = prod_sum - ((sum_v1 * sum_v2) / n)
    den = sqrt((sum_v1_pow - pow(sum_v1, 2) / n) * (sum_v2_pow - pow(sum_v2, 2) / n))
    if den == 0: 
        return 0
    return 1.0 - (num / den)

