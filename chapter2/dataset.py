# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
DATASET_PATH = os.getcwd() + '/dataset'


def get_movie_dict():
    """Build movie dictitonary"""
    movie_dict = {}
    with open(DATASET_PATH + "/u.item", "r") as uitem:
        for row in uitem.readlines():
            data = row.split("|")
            movie_id, movie_title, imdb_url = data[0], data[1], data[4]
            movie_dict[movie_id] = {
                'title': movie_title,
                'imdb': imdb_url
            }
    return movie_dict


def get_dataset():
    """Merge data from two different files and build critics dictionary"""
    dataset = dict()
    with open(DATASET_PATH + "/u.data", "r") as udata:
        for row in udata.readlines():
            u_id, i_id, rating, _ = row.split("\t")
            if u_id not in dataset:
                dataset[u_id] = {}
            dataset[u_id][i_id] = float(rating)

    return dataset
