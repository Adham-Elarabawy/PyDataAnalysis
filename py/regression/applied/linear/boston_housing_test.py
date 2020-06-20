from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns
import matplotlib as mpl

from sklearn.datasets import load_boston
boston_dataset = load_boston()
# load data from boston dataset into panda dataframe
boston = pd.DataFrame(boston_dataset.data,
                      columns=boston_dataset.feature_names)

# show the first 5 rows(head)
# print(boston.head())

# add a column of target value to the dataframe
boston['MEDV'] = boston_dataset.target

# check to see if there are any null values in the dataset
# print(boston.isnull().sum())

# EXPLORATORY DATA ANALYSIS(visualizations to understand the relationship of the target var with other feeatures):

# ---plot distribution of target variable
sns.set(rc={'figure.figsize': (11.7, 8.27)})
sns.distplot(boston['MEDV'], bins=30)
plt.show()

# ---create a correlation matrix that measures the linear relationships between the variables
correlation_matrix = boston.corr().round(2)
sns.heatmap(data=correlation_matrix, annot=True)
# ---=== basically you want to select feature variables that have a storng correlation with the target variable, but not a strong correlation with each other.

# ---plot a scatterplot to see how the selected fatures vary with MEDV
plt.figure(figsize=(20, 5))

features = ['LSTAT', 'RM']
target = boston['MEDV']

for i, col in enumerate(features):
    plt.subplot(1, len(features), i+1)
    x = boston[col]
    y = target
    plt.scatter(x, y, marker='o')
    plt.title(col)
    plt.xlabel(col)
    plt.ylabel('MEDV')
plt.show()

# PREPARING DATA FOR TRAINING MODEL
# ---concatenate feature variables using np.c_ from numpy
X = pd.DataFrame(np.c_[boston['LSTAT'], boston['RM']], columns=['LSTAT', 'RM'])
Y = boston['MEDV']


X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=5)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

# TRAINING & TESTING THE MODEL
lin_model = LinearRegression()
lin_model.fit(X_train, Y_train)

# ---model evaluation for training set
y_train_predict = lin_model.predict(X_train)
rmse = (np.sqrt(mean_squared_error(Y_train, y_train_predict)))
r2 = r2_score(Y_train, y_train_predict)

print("The model performance for training set")
print("--------------------------------------")
print('RMSE is {}'.format(rmse))
print('R2 score is {}'.format(r2))
print("\n")

# ---model evaluation for testing set
y_test_predict = lin_model.predict(X_test)
rmse = (np.sqrt(mean_squared_error(Y_test, y_test_predict)))
r2 = r2_score(Y_test, y_test_predict)

print("The model performance for testing set")
print("--------------------------------------")
print('RMSE is {}'.format(rmse))
print('R2 score is {}'.format(r2))