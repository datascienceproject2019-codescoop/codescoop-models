import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor

PATH = "../data/repositories-rating.csv"

'''
Creates a model used to predict the rating of a repository
'''

# load the data, fill in the NaNs and convert it to ints
data = pd.read_csv(PATH, sep = ',', usecols = ['Fork', 'Issues enabled', 'Wiki enabled', 'Pages enabled',
                                               'Stars Count', 'Forks Count', 'Open Issues Count',
                                               'Watchers Count', 'Contributors Count', 'December 22, 2018'])


data['Fork']               = data['Fork'].fillna(False)
data['Issues enabled']     = data['Issues enabled'].fillna(False)
data['Wiki enabled']       = data['Wiki enabled'].fillna(False)
data['Pages enabled']      = data['Pages enabled'].fillna(False)
data['Stars Count']        = data['Stars Count'].fillna(0)
data['Forks Count']        = data['Forks Count'].fillna(0)
data['Open Issues Count']  = data['Open Issues Count'].fillna(0)
data['Watchers Count']     = data['Watchers Count'].fillna(0)
data['Contributors Count'] = data['Contributors Count'].fillna(0)

data['Fork']           = data['Fork'].astype(int)
data['Issues enabled'] = data['Issues enabled'].astype(int)
data['Wiki enabled']   = data['Wiki enabled'].astype(int)
data['Pages enabled']  = data['Pages enabled'].astype(int)


# split the data
x_train, x_test, y_train, y_test = train_test_split(data.drop(['December 22, 2018'], axis = 1),
                                                    data['December 22, 2018'], test_size = 0.2)


# used model
model = make_pipeline(
    PolynomialFeatures(degree = 2, include_bias = False, interaction_only = False),
    DecisionTreeRegressor(max_depth = 9, min_samples_leaf = 8, min_samples_split = 14)
)


# do some cross validation to check how well does the model perform
cv = cross_validate(model, data.drop(['December 22, 2018'], axis = 1), data['December 22, 2018'], cv = 10,
                    return_train_score = True)

print('train score: \n{}'.format(cv['train_score']))
print('test score: \n{}'.format(cv['test_score']))


# train the model
model = make_pipeline(
    PolynomialFeatures(degree = 2, include_bias = False, interaction_only = False),
    DecisionTreeRegressor(max_depth = 9, min_samples_leaf = 8, min_samples_split = 14)
)

model.fit(x_train, y_train)
print('train score: {}'.format(model.score(x_train, y_train)))
print('test score: {}'.format(model.score(x_test, y_test)))

# pickle the model
pickle.dump(model, open('../models/predict_rating_model', 'wb'))
