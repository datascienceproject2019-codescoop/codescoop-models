import time
import numpy as np
import pandas as pd

'''
Find 500000 entries that are from Github, are not unmaintained, and occur in all four dump.
For each set of entries compute a rating of the overall success of the repository then save
this rating with the their corresponding data.
Combine all the ratings with the entries from the latest dump and save it separately.
'''

PATH100 = "../data/repositories-1.0.0-2017-06-15.csv"
PATH110 = "../data/repositories-1.1.0-2017-11-29.csv"
PATH120 = "../data/repositories-1.2.0-2018-03-12.csv"
PATH140 = "../data/repositories-1.4.0-2018-12-22.csv"

# get NROWS entries that are from Github
NROWS  = 500000
SAFETY = NROWS * 2

data100 = pd.read_csv(PATH100, nrows = SAFETY, index_col = False)
data110 = pd.read_csv(PATH110, nrows = SAFETY, index_col = False)
data120 = pd.read_csv(PATH120, nrows = SAFETY, index_col = False)
data140 = pd.read_csv(PATH140, nrows = SAFETY, index_col = False)

# drop Unmaintained entries
data100 = data100.drop(data100[data100['Status'] == 'Unmaintained'].index)
data110 = data110.drop(data110[data110['Status'] == 'Unmaintained'].index)
data120 = data120.drop(data120[data120['Status'] == 'Unmaintained'].index)
data140 = data140.drop(data140[data140['Status'] == 'Unmaintained'].index)

# drop GitLab entries
data100 = data100.drop(data100[data100['Host Type'] == 'GitLab'].index)
data110 = data110.drop(data110[data110['Host Type'] == 'GitLab'].index)
data120 = data120.drop(data120[data120['Host Type'] == 'GitLab'].index)
data140 = data140.drop(data140[data140['Host Type'] == 'GitLab'].index)

# drop entries from the latest data set that are not in the older data sets
data140 = data140.drop(data140[data140['UUID'].isin(data100['UUID']) == False].index)
data140 = data140.drop(data140[data140['UUID'].isin(data110['UUID']) == False].index)
data140 = data140.drop(data140[data140['UUID'].isin(data120['UUID']) == False].index)

# reduce the latest data set to NROWS
data140 = data140.reset_index().drop('index', axis = 1)
data140 = data140.drop(data140[data140.index >= NROWS].index)

# get the other data sets to contain the same entries
data100 = data100.drop(data100[data100['UUID'].isin(data140['UUID']) == False].index)
data110 = data110.drop(data110[data110['UUID'].isin(data140['UUID']) == False].index)
data120 = data120.drop(data120[data120['UUID'].isin(data140['UUID']) == False].index)

# create some dummy fields that will be used to compute the score, shall be dropped later
# for data100
data100['_Fork']           = data100['Fork'].fillna(False)
data100['_Issues enabled'] = data100['Issues enabled'].fillna(False)
data100['_Wiki enabled']   = data100['Wiki enabled'].fillna(False)
data100['_Pages enabled']  = data100['Pages enabled'].fillna(False)

data100['_Stars Count']        = data100['Stars Count'].fillna(0)
data100['_Forks Count']        = data100['Forks Count'].fillna(0)
data100['_Open Issues Count']  = data100['Open Issues Count'].fillna(0)
data100['_Watchers Count']     = data100['Watchers Count'].fillna(0)
data100['_Contributors Count'] = data100['Contributors Count'].fillna(0)

data100['_Fork']           = data100['_Fork'].astype(int)
data100['_Issues enabled'] = data100['_Issues enabled'].astype(int)
data100['_Wiki enabled']   = data100['_Wiki enabled'].astype(int)
data100['_Pages enabled']  = data100['_Pages enabled'].astype(int)

data100['_Updated Timestamp'] = data100['Updated Timestamp'].apply(pd.to_datetime)
data100['_Updated Timestamp'] = data100['_Updated Timestamp'] - data100['_Updated Timestamp'].min()
data100['_Updated Timestamp'] = data100['_Updated Timestamp'].apply(lambda value: value.days)

# for data110
data110['_Fork']           = data110['Fork'].fillna(False)
data110['_Issues enabled'] = data110['Issues enabled'].fillna(False)
data110['_Wiki enabled']   = data110['Wiki enabled'].fillna(False)
data110['_Pages enabled']  = data110['Pages enabled'].fillna(False)

data110['_Stars Count']        = data110['Stars Count'].fillna(0)
data110['_Forks Count']        = data110['Forks Count'].fillna(0)
data110['_Open Issues Count']  = data110['Open Issues Count'].fillna(0)
data110['_Watchers Count']     = data110['Watchers Count'].fillna(0)
data110['_Contributors Count'] = data110['Contributors Count'].fillna(0)

data110['_Fork']           = data110['_Fork'].astype(int)
data110['_Issues enabled'] = data110['_Issues enabled'].astype(int)
data110['_Wiki enabled']   = data110['_Wiki enabled'].astype(int)
data110['_Pages enabled']  = data110['_Pages enabled'].astype(int)

data110['_Updated Timestamp'] = data110['Updated Timestamp'].apply(pd.to_datetime)
data110['_Updated Timestamp'] = data110['_Updated Timestamp'] - data110['_Updated Timestamp'].min()
data110['_Updated Timestamp'] = data110['_Updated Timestamp'].apply(lambda value: value.days)

# for data120
data120['_Fork']           = data120['Fork'].fillna(False)
data120['_Issues enabled'] = data120['Issues enabled'].fillna(False)
data120['_Wiki enabled']   = data120['Wiki enabled'].fillna(False)
data120['_Pages enabled']  = data120['Pages enabled'].fillna(False)

data120['_Stars Count']        = data120['Stars Count'].fillna(0)
data120['_Forks Count']        = data120['Forks Count'].fillna(0)
data120['_Open Issues Count']  = data120['Open Issues Count'].fillna(0)
data120['_Watchers Count']     = data120['Watchers Count'].fillna(0)
data120['_Contributors Count'] = data120['Contributors Count'].fillna(0)

data120['_Fork']           = data120['_Fork'].astype(int)
data120['_Issues enabled'] = data120['_Issues enabled'].astype(int)
data120['_Wiki enabled']   = data120['_Wiki enabled'].astype(int)
data120['_Pages enabled']  = data120['_Pages enabled'].astype(int)

data120['_Updated Timestamp'] = data120['Updated Timestamp'].apply(pd.to_datetime)
data120['_Updated Timestamp'] = data120['_Updated Timestamp'] - data120['_Updated Timestamp'].min()
data120['_Updated Timestamp'] = data120['_Updated Timestamp'].apply(lambda value: value.days)

# for data140
data140['_Fork']           = data140['Fork'].fillna(False)
data140['_Issues enabled'] = data140['Issues enabled'].fillna(False)
data140['_Wiki enabled']   = data140['Wiki enabled'].fillna(False)
data140['_Pages enabled']  = data140['Pages enabled'].fillna(False)

data140['_Stars Count']        = data140['Stars Count'].fillna(0)
data140['_Forks Count']        = data140['Forks Count'].fillna(0)
data140['_Open Issues Count']  = data140['Open Issues Count'].fillna(0)
data140['_Watchers Count']     = data140['Watchers Count'].fillna(0)
data140['_Contributors Count'] = data140['Contributors Count'].fillna(0)

data140['_Fork']           = data140['_Fork'].astype(int)
data140['_Issues enabled'] = data140['_Issues enabled'].astype(int)
data140['_Wiki enabled']   = data140['_Wiki enabled'].astype(int)
data140['_Pages enabled']  = data140['_Pages enabled'].astype(int)

data140['_Updated Timestamp'] = data140['Updated Timestamp'].apply(pd.to_datetime)
data140['_Updated Timestamp'] = data140['_Updated Timestamp'] - data140['_Updated Timestamp'].min()
data140['_Updated Timestamp'] = data140['_Updated Timestamp'].apply(lambda value: value.days)

# compute the score
dummy_scores100 = np.log(data100.loc[:, '_Stars Count'] + 1) - data100.loc[:, '_Fork'] + \
                  data100.loc[:, '_Issues enabled'] + data100.loc[:, '_Wiki enabled'] + \
                  data100.loc[:, '_Pages enabled'] + np.log(data100.loc[:, '_Forks Count'] + 1) - \
                  np.log(data100.loc[:, '_Open Issues Count'] + 1) + np.log(data100.loc[:, '_Watchers Count'] + 1) + \
                  np.log(data100.loc[:, '_Contributors Count'] + 1) + np.log(data100.loc[:, '_Updated Timestamp'] + 1)
dummy_scores110 = np.log(data110.loc[:, '_Stars Count'] + 1) - data110.loc[:, '_Fork'] + \
                  data110.loc[:, '_Issues enabled'] + data110.loc[:, '_Wiki enabled'] + \
                  data110.loc[:, '_Pages enabled'] + np.log(data110.loc[:, '_Forks Count'] + 1) - \
                  np.log(data110.loc[:, '_Open Issues Count'] + 1) + np.log(data110.loc[:, '_Watchers Count'] + 1) + \
                  np.log(data110.loc[:, '_Contributors Count'] + 1) + np.log(data110.loc[:, '_Updated Timestamp'] + 1)
dummy_scores120 = np.log(data120.loc[:, '_Stars Count'] + 1) - data120.loc[:, '_Fork'] + \
                  data120.loc[:, '_Issues enabled'] + data120.loc[:, '_Wiki enabled'] + \
                  data120.loc[:, '_Pages enabled'] + np.log(data120.loc[:, '_Forks Count'] + 1) - \
                  np.log(data120.loc[:, '_Open Issues Count'] + 1) + np.log(data120.loc[:, '_Watchers Count'] + 1) + \
                  np.log(data120.loc[:, '_Contributors Count'] + 1) + np.log(data120.loc[:, '_Updated Timestamp'] + 1)
dummy_scores140 = np.log(data140.loc[:, '_Stars Count'] + 1) - data140.loc[:, '_Fork'] + \
                  data140.loc[:, '_Issues enabled'] + data140.loc[:, '_Wiki enabled'] + \
                  data140.loc[:, '_Pages enabled'] + np.log(data140.loc[:, '_Forks Count'] + 1) - \
                  np.log(data140.loc[:, '_Open Issues Count'] + 1) + np.log(data140.loc[:, '_Watchers Count'] + 1) + \
                  np.log(data140.loc[:, '_Contributors Count'] + 1) + np.log(data140.loc[:, '_Updated Timestamp'] + 1)

# scale the scores
dummy_scores100 = (dummy_scores100 - dummy_scores100.min()) / (dummy_scores100.max() - dummy_scores100.min())
dummy_scores100 = round(dummy_scores100 * 5, 2)

dummy_scores110 = (dummy_scores110 - dummy_scores110.min()) / (dummy_scores110.max() - dummy_scores110.min())
dummy_scores110 = round(dummy_scores110 * 5, 2)

dummy_scores120 = (dummy_scores120 - dummy_scores120.min()) / (dummy_scores120.max() - dummy_scores120.min())
dummy_scores120 = round(dummy_scores120 * 5, 2)

dummy_scores140 = (dummy_scores140 - dummy_scores140.min()) / (dummy_scores140.max() - dummy_scores140.min())
dummy_scores140 = round(dummy_scores140 * 5, 2)

# drop extra columns
data100 = data100.drop(['_Fork', '_Issues enabled', '_Wiki enabled', '_Pages enabled', '_Stars Count', '_Forks Count', '_Open Issues Count', '_Watchers Count', '_Contributors Count', '_Updated Timestamp'], axis = 1)
data110 = data110.drop(['_Fork', '_Issues enabled', '_Wiki enabled', '_Pages enabled', '_Stars Count', '_Forks Count', '_Open Issues Count', '_Watchers Count', '_Contributors Count', '_Updated Timestamp'], axis = 1)
data120 = data120.drop(['_Fork', '_Issues enabled', '_Wiki enabled', '_Pages enabled', '_Stars Count', '_Forks Count', '_Open Issues Count', '_Watchers Count', '_Contributors Count', '_Updated Timestamp'], axis = 1)
data140 = data140.drop(['_Fork', '_Issues enabled', '_Wiki enabled', '_Pages enabled', '_Stars Count', '_Forks Count', '_Open Issues Count', '_Watchers Count', '_Contributors Count', '_Updated Timestamp'], axis = 1)

# add the ratings to the data frames
data100           = data100.reset_index().drop('index', axis = 1)
data100['Rating'] = dummy_scores100.reset_index().drop('index', axis = 1)

data110           = data110.reset_index().drop('index', axis = 1)
data110['Rating'] = dummy_scores110.reset_index().drop('index', axis = 1)

data120           = data120.reset_index().drop('index', axis = 1)
data120['Rating'] = dummy_scores120.reset_index().drop('index', axis = 1)

data140           = data140.reset_index().drop('index', axis = 1)
data140['Rating'] = dummy_scores140.reset_index().drop('index', axis = 1)

# store the data for each dump
data100.to_csv("../data/repositories-1.0.0-2017-06-15-rating.csv", index = False)
data110.to_csv("../data/repositories-1.1.0-2017-11-29-rating.csv", index = False)
data120.to_csv("../data/repositories-1.2.0-2018-03-12-rating.csv", index = False)
data140.to_csv("../data/repositories-1.4.0-2018-12-22-rating.csv", index = False)

# save the multiple ratings in the same csv with all the columns from the latest dump
data100['UUID'] = data100['UUID'].astype(int)
data110['UUID'] = data110['UUID'].astype(int)
data120['UUID'] = data120['UUID'].astype(int)
data140['UUID'] = data140['UUID'].astype(int)

data140 = data140.merge(data100[['UUID', 'Rating']], left_on = 'UUID', right_on = 'UUID', suffixes = ('_140', '_100'))
data140 = data140.merge(data110[['UUID', 'Rating']], left_on = 'UUID', right_on = 'UUID', suffixes = ('_140', '_110'))
data140 = data140.merge(data120[['UUID', 'Rating']], left_on = 'UUID', right_on = 'UUID', suffixes = ('_110', '_120'))

data140 = data140.rename(index = str, columns = {'Rating_140': 'December 22, 2018', 'Rating_100': 'July 21, 2017', 'Rating_110': 'November 29, 2017', 'Rating_120': 'March 13, 2018'})

data140.to_csv("../data/repositories-rating.csv", index = False)
