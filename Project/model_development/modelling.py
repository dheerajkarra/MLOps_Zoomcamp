# -*- coding: utf-8 -*-
"""
@author: Dheeraj

"""

import pandas as pd
import pickle
import os

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
# from sklearn.feature_selection import mutual_info_regression

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# os.chdir("F:\\Projects\\MLOps\\MLOps_Zoomcamp\\Project\\model_development\\")

data = pd.read_csv("energydata_complete.csv")

data = data.drop('date', axis = 1)
data = data[0:5000]

X = data.drop(['Appliances','lights', 'T6','RH_6','T_out','rv1','rv2','Tdewpoint'],axis=1)
y = data['Appliances']

# Get scores for best features
best_features = SelectKBest(score_func=chi2, k=10)
fit = best_features.fit(X,y)
feature_scores = pd.concat([pd.DataFrame(X.columns),pd.DataFrame(fit.scores_)], axis=1)
feature_scores.columns = ['Specs','Score']
feature_scores

print(feature_scores.nlargest(4,'Score'))

# Select best features
select_features = ['Visibility','RH_5','Windspeed','RH_out']
train_dicts = data[select_features].to_dict(orient='records')

# Fit and Predict on Train data
dv = DictVectorizer()
X_train = dv.fit_transform(train_dicts)
target = 'Appliances'
y_train = data[target].values

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_train)
mean_squared_error(y_train, y_pred, squared=False)
# 115.57

# Do train test split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size = 0.2, random_state = 37)
X_tr, X_va, y_tr, y_va = train_test_split(X_tr, y_tr, test_size=0.2, random_state=37)
len(X_tr), len(X_va)

# Fit on Train data and Predict on Validation data to check there is no overfit
# so that the features selected are good enough

dv = DictVectorizer()
train_dicts = X_tr[select_features].to_dict(orient='records')
X_train = dv.fit_transform(train_dicts)

val_dicts = X_va[select_features].to_dict(orient='records')
X_val = dv.transform(val_dicts)
y_va.head()

target = 'quality'
y_train = y_tr.values
y_val = y_va.values
lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_val)
mean_squared_error(y_val, y_pred, squared=False)
# 117.70

with open('lin_reg.bin', 'wb') as f_out:
    pickle.dump((dv, lr), f_out)
