#!/usr/bin/env python
# -*- coding: utf8 -*-
from pandas import DataFrame, Series
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import os
import json

matplotlib.style.use('ggplot')

# os.chdir('D:\github\pydata-book\ch05')

data = {
    'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
    'year': [2000, 2001, 2002, 2001, 2002],
    'pop': [1.5, 1.7, 3.6, 2.4, 2.9]
}

frame2 = DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
                   index=['one', 'two', 'three', 'four', 'five'])

print frame2

# print frame2.ix['three']

frame2['debt'] = np.arange(5.)

print frame2

df3 = pd.DataFrame(np.random.randn(3, 2), columns=['B', 'C']).cumsum()

print df3

df3['A'] = pd.Series(list(range(len(df3))))

print df3

df3.plot(x='A', y='B')

plt.show()


