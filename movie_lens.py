#!/usr/bin/env python
# -*- coding: utf8 -*-

from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os
import json

os.chdir('D:\github\pydata-book\ch02\movielens')

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('users.dat', sep='::', header=None,
                      names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('ratings.dat', sep='::', header=None,
                        names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('movies.dat', sep='::', header=None,
                       names=mnames)

# print users[:5]
# print ratings[:5]
# print movies[:5]

data = pd.merge(pd.merge(ratings, users), movies)

print data.ix[0]

mean_rating = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')

# print mean_rating[:5]

ratings_by_title = data.groupby('title').size()

active_titles = ratings_by_title.index[ratings_by_title >= 250]

mean_ratings = mean_rating.ix[active_titles]

print mean_ratings

top_female_ratings = mean_ratings.sort_index(by='F', ascending=False)

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']

rating_std_by_title = data.groupby('title')['rating'].std()

rating_std_by_title = rating_std_by_title.ix[active_titles]

# print rating_std_by_title.order(ascending=False)[:10]
print rating_std_by_title