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

data.to_csv('d:/dataframe.csv', index=False)

mean_rating = data.pivot_table('rating', rows='title', cols='gender', aggfunc='mean')

mean_rating[:5]