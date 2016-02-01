#!/usr/bin/env python
# -*- coding: utf8 -*-
from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import os
import json
import re

matplotlib.style.use('ggplot')

os.chdir('D:\github\pydata-book\ch02')

unames = ['company', 'scale', 'min_salary', 'max_salary', 'occupation', 'industry', 'city',
          'min_exp', 'max_exp', 'education']
data = pd.read_table('lagou.data', sep=',', header=None,
                      names=unames, encoding='gbk')

def fx(x, y):
    return x.encode('gbk') + '-' + y.encode('gbk')

data['experience'] = np.vectorize(fx)(data['min_exp'], data['max_exp'])

data['min_salary'] = data['min_salary'].astype(unicode).convert_objects(convert_numeric=True)
data['max_salary'] = data['max_salary'].astype(unicode).convert_objects(convert_numeric=True)

data = data[data.min_salary.notnull()]
data = data[data.max_salary.notnull()]

data['min_exp'] = data['min_exp'].astype(unicode).convert_objects(convert_numeric=True)
data['max_exp'] = data['max_exp'].astype(unicode).convert_objects(convert_numeric=True)

data = data[data.min_exp.notnull()]
data = data[data.max_exp.notnull()]

# 过滤工作经验1 - 3年
data = data[data['experience'] == '1-3']
# 过滤深圳
data = data[data['city'].str.contains(u'深圳', case=False)]

data.loc[data['occupation'].str.contains('ios', case=False), 'occupation'] = 'ios'
data.loc[data['occupation'].str.contains('ui', case=False), 'occupation'] = 'ui'
data.loc[data['occupation'].str.contains('android', case=False), 'occupation'] = 'android'
data.loc[data['occupation'].str.contains('python', case=False), 'occupation'] = 'python'
data.loc[data['occupation'].str.contains('hrbp', case=False), 'occupation'] = 'hrbp'

ios = data[data['occupation'].str.contains('ios', case=False)]
python = data[data['occupation'].str.contains('python', case=False)]
ui = data[data['occupation'].str.contains('ui', case=False)]
android = data[data['occupation'].str.contains('android', case=False)]
hrbp = data[data['occupation'].str.contains('hrbp', case=False)]

# ios = ios[ios['city'].str.contains(u'深圳', case=False)]

print 'data specimen ' + str(len(data))
print 'ios specimen ' + str(len(ios))
print 'android specimen ' + str(len(android))
print 'ui specimen ' + str(len(ui))
print 'python specimen' + str(len(python))
print 'hrbp specimen ' + str(len(hrbp))

print ios.describe()
print ios[:5]

ios = ios[ios['min_salary'] >= 10]
print ios[:5]

# ios_subset = ios[ios['min_salary'] <= 10]
# ios_subset = ios_subset[ios_subset['max_salary'] >= 10]
# print len(ios_subset)
# print ios_subset[:5]
#
# python_subset = python[python['min_salary'] <= 10]
# python_subset = python_subset[python_subset['max_salary'] >= 10]
#
# print len(python_subset)
#
# android_subset = android[android['min_salary'] <= 10]
# android_subset = android_subset[android_subset['max_salary'] >= 10]
#
# print len(android_subset)
# print android_subset[:5]

# def fx(x, y):
#     return x.encode('gbk') + '-' + y.encode('gbk')
#
# ios['salary'] = np.vectorize(fx)(ios['min_salary'], ios['max_salary'])
#
# import operator
# select_dict = {
#                "min_salary": (operator.ge, 10),
#                # "max_salary": (operator.ge, 10),
#               }
#
# def pandas_select(dataframe, select_dict):
#
#     inds = dataframe.apply(lambda x: reduce(lambda v1,v2: v1 and v2,
#                            [elem[0](x[key], elem[1])
#                            for key,elem in select_dict.iteritems()]), axis=1)
#     return dataframe[inds]
#
# i = pandas_select(ios, select_dict).to_string()
#
# print i[:5]
#
# # ios1 = ios[ios['min_salary'] > 10]
# # print ios1[:5]
# # print ios1[ios['max_salary'] >= 10]
#
# salary_by_ios = ios.groupby('salary').size()
# # salary_by_ios.plot()
#
# # print ios[:5]
#
# # print data[-5:]
# plt.show()

# ios_min_salary_plot = ios['min_salary'].hist(bins=20)
# ios_min_salary_plot.set_title(u'shenzhen 1-3 ios_min_salary_plot')
# ios_min_salary_plot.set_xlabel('min_salary')
# ios_min_salary_plot.set_ylabel('Number of companies')

# ios_max_salary_plot = ios['max_salary'].hist(bins=20)
# ios_max_salary_plot.set_title('ios_max_salary_plot')
# ios_max_salary_plot.set_xlabel('max_salary')
# ios_max_salary_plot.set_ylabel('Number of companies')

# android_max_salary_plot = android['max_salary'].hist(bins=20, color='red')
# android_max_salary_plot.set_title('android_max_salary_plot')
# android_max_salary_plot.set_xlabel('max_salary')
# android_max_salary_plot.set_ylabel('Number of companies')

# android_min_salary_plot = android['min_salary'].hist(bins=20, color='red')
# android_min_salary_plot.set_title('android_min_salary_plot')
# android_min_salary_plot.set_xlabel('min_salary')
# android_min_salary_plot.set_ylabel('Number of companies')

# python_min_salary_plot = python['min_salary'].hist(bins=20, color='green')
# python_min_salary_plot.set_title('python_min_salary_plot')
# python_min_salary_plot.set_xlabel('min_salary')
# python_min_salary_plot.set_ylabel('Number of companies')

# python_max_salary_plot = python['max_salary'].hist(bins=20, color='green')
# python_max_salary_plot.set_title('python_max_salary_plot')
# python_max_salary_plot.set_xlabel('max_salary')
# python_max_salary_plot.set_ylabel('Number of companies')

# ui_max_salary_plot = ui['max_salary'].hist(bins=20, color='blue')
# ui_max_salary_plot.set_title('ui_max_salary_plot')
# ui_max_salary_plot.set_xlabel('max_salary')
# ui_max_salary_plot.set_ylabel('Number of companies')

# ui_min_salary_plot = ui['min_salary'].hist(bins=20, color='blue')
# ui_min_salary_plot.set_title('ui_min_salary_plot')
# ui_min_salary_plot.set_xlabel('min_salary')
# ui_min_salary_plot.set_ylabel('Number of companies')

plt.show()
# ios.plot(x='')