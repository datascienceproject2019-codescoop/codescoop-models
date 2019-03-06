# This code demonstrates how to use lasso regression for choosing optimal variables
# for a linear model.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# I used a toy dataset, this should be replaced with the actual data
data = load_boston()

# x should be a dataframe containing the explanatory variables (forks, language, etc)
x = data.data

# y should be a vector containing the target variable (number of stars)
y = data.target

# split the data in to train and test part
X_train, X_test, y_train, y_test = train_test_split(x, y)


## trying different alphas and choosing the optimal model

# if fitting of the model is really slow, you can drop last values of alpha to make it faster
alphas = [0.0001, 0.001, 0.01, 0.05, 0.1, 1, 5, 10]
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
    print("Training score:", train_score)
    print("Test score: ", test_score)
    print("Number of features used: ", coeff_used)
    print(" ")

# pick the alpha value with best score
best_alpha = alphas[np.argmax(test_scores)]
print("Optimal alpha = ", best_alpha)
lasso = Lasso(alpha = best_alpha, max_iter = 10e5)
lasso.fit(X_train, y_train)


# model summary
predicted = lasso.predict(X_test)
expected = y_test
# expected vs predicted values
plt.scatter(expected, predicted)
plt.show()
print("Mean squared error: ", mean_squared_error(expected, predicted))
print("Model R² score: ", r2_score(expected, predicted))
