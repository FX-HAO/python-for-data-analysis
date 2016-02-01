#!/usr/bin/env python
# -*- coding: utf8 -*-

from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os
import json

os.chdir(r'D:\github\pydata-book\ch02\names')

years = xrange(1880, 2011)

pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    filename = 'yob%d.txt' % year
    frame = pd.read_csv(filename, names=columns)
    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)

print len(names)