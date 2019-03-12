
# coding: utf-8

# **THIS Notebook does a simple linear regression on data from Libraries.io** 
# The getting the data part is very much hacked together but it is placeholder data anyway,
# The regression stuff should be quite solid.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.datasets import load_boston
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score




pd.set_option('display.max_columns', 500)


# In[2]:


N_SAMPLES = 200000
VERBOSE = True
ALPHA = [0.1, 1]
PATH ="/home/rick/UH-Spring-2019/Project/codescoop-models/Libraries_io_data/repositories-1.2.0-2018-03-12.csv"


# In[3]:


#Functions for factorizing and getting dummies
def gnumeric_func (data, columns):
    data[columns] = data[columns].apply(lambda x: pd.factorize(x)[0])
    return data

def getDummies (data, feature):
    dummies = pd.get_dummies(data[feature])
    data = pd.concat([data, dummies], axis=1)
    data = data.drop([feature],axis=1)
    return data

def runOLS(featureList, target):

    dataxStats = datax[featureList]
    statsmodel = sm.OLS(target, dataxStats).fit()

    print(statsmodel.summary())
    return statsmodel.pvalues


# In[9]:


#getting the explanatory variables, and changing categorial values to dummies
data = pd.read_csv(PATH, usecols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38], 
                   nrows = N_SAMPLES)


droplist = ['SourceRank','Description', 'Name with Owner', 'Created Timestamp', "Updated Timestamp", 'Last pushed Timestamp', 'Homepage URL', 'Mirror URL', 'UUID', 'Last Synced Timestamp','Fork Source Name with Owner', 'Changelog filename', 'Contributing guidelines filename', 'License filename','Code of Conduct filename', 'Security Threat Model filename', 'Security Audit filename', 'SCM type', 'Logo URL', 'Keywords', 'Stars Count' ]
factorizelist = ['Host Type', 'Fork', 'Issues enabled', 'Wiki enabled', 'Pages enabled', 'Default branch', 'Display Name', 'Pull requests enabled'] 
dummieslist = ['Language', 'License', 'Status']

datax = data.drop(droplist, axis=1)
datax = datax.drop(['Readme filename'], axis=1) #idk why I need to do it separately, cleaning is for later

datax = gnumeric_func(datax, factorizelist)

for item in dummieslist:
    datax = getDummies(datax,item)

datax.head()


# In[5]:


data.head()


# In[10]:


# This code demonstrates how to use lasso regression for choosing optimal variables
# for a linear model.

# x should be a dataframe containing the explanatory variables (forks, language, etc)
x = datax

# y should be a vector containing the target variable (number of stars)
y = list(data["Stars Count"])

# split the data in to train and test part
X_train, X_test, y_train, y_test = train_test_split(x, y)


## trying different alphas and choosing the optimal model

# if fitting of the model is really slow, you can drop last values of alpha to make it faster
alphas = ALPHA
n = len(alphas)
test_scores = np.zeros(n)

for i in range(0,n):
    a = alphas[i]
    print("alpha = ", a)
    lasso = Lasso(alpha = a, max_iter = 10e5)
    lasso.fit(X_train, y_train)
    train_score=lasso.score(X_train,y_train)
    test_score=lasso.score(X_test,y_test)
    test_scores[i] = test_score
    coeff_used = np.sum(lasso.coef_!=0)
    
    if VERBOSE:
        print("Training score:", train_score)
        print("Test score: ", test_score)
        print("Number of features used: ", coeff_used)
        print(" ")

# pick the alpha value with best score
best_alpha = alphas[np.argmax(test_scores)]
print("Optimal alpha = ", best_alpha)
lasso = Lasso(alpha = best_alpha, max_iter = 10e5)
lasso.fit(X_train, y_train)

# create a dataframe with the coefficents of the features
df_coef = pd.DataFrame({'Features':x.columns,'coeff': lasso.coef_})
df_coef = df_coef.sort_values(by = ['coeff'])
df_coef = df_coef[df_coef.coeff != -0.0]
    


# model summary
predicted = lasso.predict(X_test)
expected = y_test
# expected vs predicted values
if VERBOSE:
    plt.scatter(expected, predicted)
    plt.show()
    print("Mean squared error: ", mean_squared_error(expected, predicted))
    print("Model R² score: ", r2_score(expected, predicted))


# In[11]:


df_coef
featureList = list(df_coef.Features)


# In[13]:


pvals_first = runOLS(featureList=featureList, target=data['Stars Count'])

keylist_second = list(dict(pvals[pvals < 0.01]).keys())


runOLS(keylist_second, data['Stars Count'])

