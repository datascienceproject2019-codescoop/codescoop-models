import numpy as np
import pandas as pd


'''
Merge into a single csv the chronological values for:
   - stars count
   - forks count
   - watchers count
   - contributors count
   - rating

In which the _1 denote values from July 21, 2017
             _2 denote values from November 29, 2017
             _3 denote values from March 13, 2018
             _4 denote values from December 22, 2018

Store also the name of the repository, UUID, create and update timestamps.

Saves the data as a csv in ../data/repositories-timeseries.csv
'''


PATH1 = "../data/repositories-1.0.0-2017-06-15-rating.csv"
PATH2 = "../data/repositories-1.1.0-2017-11-29-rating.csv"
PATH3 = "../data/repositories-1.2.0-2018-03-12-rating.csv"
PATH4 = "../data/repositories-1.4.0-2018-12-22-rating.csv"


data1 = pd.read_csv(PATH1, usecols = ['Stars Count', 'Forks Count', 'Watchers Count', 'Contributors Count',
                                      'Rating', 'UUID'], index_col = False)
data2 = pd.read_csv(PATH2, usecols = ['Stars Count', 'Forks Count', 'Watchers Count', 'Contributors Count',
                                      'Rating', 'UUID'], index_col = False)
data3 = pd.read_csv(PATH3, usecols = ['Stars Count', 'Forks Count', 'Watchers Count', 'Contributors Count',
                                      'Rating', 'UUID'], index_col = False)
data4 = pd.read_csv(PATH4, usecols = ['Stars Count', 'Forks Count', 'Watchers Count', 'Contributors Count',
                                      'Rating', 'UUID', 'Name with Owner', 'Description', 'Created Timestamp',
                                      'Updated Timestamp'], index_col = False)


data1['Stars Count']        = data1['Stars Count'].fillna(0)
data1['Forks Count']        = data1['Forks Count'].fillna(0)
data1['Watchers Count']     = data1['Watchers Count'].fillna(0)
data1['Contributors Count'] = data1['Contributors Count'].fillna(0)

data2['Stars Count']        = data2['Stars Count'].fillna(0)
data2['Forks Count']        = data2['Forks Count'].fillna(0)
data2['Watchers Count']     = data2['Watchers Count'].fillna(0)
data2['Contributors Count'] = data2['Contributors Count'].fillna(0)

data3['Stars Count']        = data3['Stars Count'].fillna(0)
data3['Forks Count']        = data3['Forks Count'].fillna(0)
data3['Watchers Count']     = data3['Watchers Count'].fillna(0)
data3['Contributors Count'] = data3['Contributors Count'].fillna(0)

data4['Stars Count']        = data4['Stars Count'].fillna(0)
data4['Forks Count']        = data4['Forks Count'].fillna(0)
data4['Watchers Count']     = data4['Watchers Count'].fillna(0)
data4['Contributors Count'] = data4['Contributors Count'].fillna(0)


data1['UUID'] = data1['UUID'].astype(int)
data2['UUID'] = data2['UUID'].astype(int)
data3['UUID'] = data3['UUID'].astype(int)
data4['UUID'] = data4['UUID'].astype(int)


data4 = data4.merge(data1[['UUID', 'Stars Count', 'Forks Count', 'Watchers Count', 'Contributors Count', 'Rating']],
                    left_on = 'UUID', right_on = 'UUID', suffixes = ('_4', '_1'))
data4 = data4.merge(data2[['UUID', 'Stars Count', 'Forks Count', 'Watchers Count', 'Contributors Count', 'Rating']],
                    left_on = 'UUID', right_on = 'UUID', suffixes = ('_4', '_2'))
data4 = data4.merge(data3[['UUID', 'Stars Count', 'Forks Count', 'Watchers Count', 'Contributors Count', 'Rating']],
                    left_on = 'UUID', right_on = 'UUID', suffixes = ('_2', '_3'))


data4.to_csv("../data/repositories-timeseries.csv", index = False)
