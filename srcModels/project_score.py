import time
import numpy as np
import pandas as pd

PATH   = "../data/repositories-1.4.0-2018-12-22.csv"

# get NROWS entries that are from Github
NROWS  = 500000
SAFETY = 100000

data = pd.read_csv(PATH, nrows = NROWS + SAFETY, index_col = False)
print(data.head())

# remove GitLab entries, reset the index then drop the aditional entries so that we are left with NROWS entries
data = data.drop(data[data['Host Type'] == 'GitLab'].index)
data = data.reset_index().drop('index', axis = 1)
data = data.drop(data[data.index >= NROWS].index)
print(data.head())

# create some dummy fields that will be used to compute the score, shall be dropped later
data['_Fork']           = data['Fork'].fillna(False)
data['_Issues enabled'] = data['Issues enabled'].fillna(False)
data['_Wiki enabled']   = data['Wiki enabled'].fillna(False)
data['_Pages enabled']  = data['Pages enabled'].fillna(False)

data['_Stars Count']        = data['Stars Count'].fillna(0)
data['_Forks Count']        = data['Forks Count'].fillna(0)
data['_Open Issues Count']  = data['Open Issues Count'].fillna(0)
data['_Watchers Count']     = data['Watchers Count'].fillna(0)
data['_Contributors Count'] = data['Contributors Count'].fillna(0)

data['_Fork']           = data['_Fork'].astype(int)
data['_Issues enabled'] = data['_Issues enabled'].astype(int)
data['_Wiki enabled']   = data['_Wiki enabled'].astype(int)
data['_Pages enabled']  = data['_Pages enabled'].astype(int)

data['_Updated Timestamp'] = data['Updated Timestamp'].apply(pd.to_datetime)
data['_Updated Timestamp'] = data['_Updated Timestamp'] - data['_Updated Timestamp'].min()
data['_Updated Timestamp'] = data['_Updated Timestamp'].apply(lambda value: value.days)

# compute the score
dummy_scores = np.log(data.loc[:, '_Stars Count'] + 1) - data.loc[:, '_Fork'] + data.loc[:, '_Issues enabled'] + \
               data.loc[:, '_Wiki enabled'] + data.loc[:, '_Pages enabled'] + np.log(data.loc[:, '_Forks Count'] + 1) - \
               np.log(data.loc[:, '_Open Issues Count'] + 1) + np.log(data.loc[:, '_Watchers Count'] + 1) + \
               np.log(data.loc[:, '_Contributors Count'] + 1) + np.log(data.loc[:, '_Updated Timestamp'] + 1)
scaled_dummy = (dummy_scores - dummy_scores.min()) / (dummy_scores.max() - dummy_scores.min())
scaled_dummy = round(scaled_dummy * 5, 2)

# add the score column and remove the dummy columns
data['Rating'] = scaled_dummy
data = data.drop(['_Fork', '_Issues enabled', '_Wiki enabled', '_Pages enabled', '_Stars Count', \
                 '_Forks Count', '_Open Issues Count', '_Watchers Count', '_Contributors Count', \
                 '_Updated Timestamp'], axis = 1)

# store the data
data.to_csv("../data/repositories-1.4.0-2018-12-22-rating.csv", index = False)
