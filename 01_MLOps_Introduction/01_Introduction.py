# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:05:23 2022

@author: Dheeraj
"""

import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# np.set_printoptions(precision = 4, suppress = True)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

os.chdir('C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\')

jan21 = pd.read_parquet('Data\\fhv_tripdata_2021-01.parquet', engine='pyarrow') # 1154112
feb21 = pd.read_parquet('Data\\fhv_tripdata_2021-02.parquet', engine='pyarrow') # , engine='fastparquet')
jan21_head = jan21.head(100)
jan21.dtypes
jan21.columns

jan21['duration'] = (jan21['dropOff_datetime'] - jan21['pickup_datetime'])/ pd.Timedelta(minutes=1) 

np.mean(jan21['duration']) # 19.167 minutes
jan21['duration'].describe()

jan211 = jan21[ ~((jan21['duration'] >= 1) & (jan21['duration'] <= 60))] # 44,286
jan21 = jan21[(jan21['duration'] >= 1) & (jan21['duration'] <= 60)] # 

jan21['PUlocationID'].describe() # 182818
jan21.DOlocationID.describe() # 961919

missing_df = jan21.isnull().sum() # PU - 927008 and DO - 147907
missing_df['PUlocationID']/jan21.shape[0] # 83.52%

jan21['PUlocationID'].fillna(-1, inplace = True)
jan21['DOlocationID'].fillna(-1, inplace = True)

# Modelling 

jan21_df = jan21[['PUlocationID','DOlocationID']]
jan21_df.apply(lambda x: x.nunique(),axis =0) # 262 and 263

# Create Vectorizer
vectorizer = DV( sparse = False )
# Convert Panda Data frame to Dict
jan21_dict = jan21_df.T.to_dict().values()
# Create Fit
jan21_vect  = vectorizer.fit_transform(jan21_dict)

# list(jan21_dict)[:3]

one_hot_enc = OneHotEncoder().fit(jan21_vect)
jan21_vect = one_hot_enc.transform(jan21_vect).toarray()

reg = LinearRegression().fit(jan21_vect, jan21['duration'])
train_predict = reg.predict(jan21_vect)

mean_squared_error(jan21['duration'], train_predict, squared=False) #

########################################################################
# Q6 -  Validation data 
########################################################################

feb21['duration'] = (feb21['dropOff_datetime'] - feb21['pickup_datetime'])/ pd.Timedelta(minutes=1) 

np.mean(feb21['duration']) #  minutes
feb21['duration'].describe()

feb211 = feb21[ ~((feb21['duration'] >= 1) & (feb21['duration'] <= 60))] # 44,286
feb21 = feb21[(feb21['duration'] >= 1) & (feb21['duration'] <= 60)] # 

feb21['PUlocationID'].describe() # 182818
feb21.DOlocationID.describe() # 961919

missing_df = feb21.isnull().sum() # PU - 927008 and DO - 147907
missing_df['PUlocationID']/feb21.shape[0] # 83.52%

feb21['PUlocationID'].fillna(-1, inplace = True)
feb21['DOlocationID'].fillna(-1, inplace = True)

# Modelling 

feb21_df = feb21[['PUlocationID','DOlocationID']]
feb21_df.apply(lambda x: x.nunique(),axis =0) # 262 and 263

# # Create Vectorizer
# vectorizer = DV( sparse = False )

# Convert Panda Data frame to Dict
feb21_dict = feb21_df.T.to_dict().values()
# Create Fit
feb21_vect  = vectorizer.fit_transform(feb21_dict)

# list(feb21_dict)[:3]

one_hot_enc = OneHotEncoder().fit(feb21_vect)
feb21_vect = one_hot_enc.transform(feb21_vect).toarray()

# reg = LinearRegression().fit(feb21_vect, feb21['duration'])
test_predict = reg.predict(feb21_vect)

mean_squared_error(feb21['duration'], test_predict, squared=False) #


# Next Steps 
# Can be written as functions for modularization

