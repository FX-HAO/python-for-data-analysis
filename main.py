#!/usr/bin/env python
# -*- coding: utf8 -*-
from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os
import json

os.chdir('D:\github\pydata-book\ch02')

path = 'usagov_bitly_data2012-03-16-1331923249.txt'

records = [json.loads(line) for line in open(path)]

time_zones = [rec['tz'] for rec in records if 'tz' in rec]

frame = DataFrame(records)

tz_counts = frame['tz'].value_counts()

clean_tz = frame['tz'].na('Missing')

clean_tz[clean_tz == ''] = 'Unknown'

tz_counts = clean_tz.value_counts()

# print tz_counts[:10]
tz_counts[:10].plot(kind='barh', rot=0)

# print records['']['a']
# print frame['a'][:5]
# print frame.a[:10]
# plt.show()

# print frame.a.dropna()[:5]

results = Series([x.split()[0] for x in frame.a.dropna()])

# print results.value_counts()[:10]

cframe = frame[frame.a.notnull()]

# print len(frame)
# print len(cframe)

operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')

# print operating_system[:5]

by_tz_os = cframe.groupby(['tz', operating_system])

print by_tz_os.size().fillna('NA')

agg_counts = by_tz_os.size().unstack().fillna(0)

print agg_counts[:10]

indexer = agg_counts.sum(1).argsort()

print indexer[:10]

count_subset = agg_counts.take(indexer)[-10:]

print count_subset

count_subset.plot(kind='barh', stacked=True)

plt.show()