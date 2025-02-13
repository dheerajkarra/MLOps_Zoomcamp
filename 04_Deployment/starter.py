#!/usr/bin/env python
# coding: utf-8


# get_ipython().system('pip freeze | grep scikit-learn')

import pickle
import pandas as pd
import sys
import numpy as np

with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)

categorical = ['PUlocationID', 'DOlocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def get_preds(df):
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    return y_pred

def run():
    
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    output_file = f'C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\MLOps_Zoomcamp\\04_Deployment\\homework\\predictions_{year:04d}_{month:02d}.parquet'
    df = read_data(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet')
    
    y_pred = get_preds(df)
    print(f'The mean predicted duration is {np.mean(y_pred)}')
    df_result = pd.DataFrame()
    df_result['predicted_duration'] = y_pred
    df_result['ride_id'] = f'{year:04d}/{month:02d}_' + df_result.index.astype('str')
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )
    
    
if __name__ == '__main__':
    run()    
    
# year = 2021
# month = 2
# output_file = f'C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\MLOps_Zoomcamp\\04_Deployment\\homework\\predictions_{year:04d}_{month:02d}.parquet'
# df_result = pd.DataFrame()
# df_result['predicted_duration'] = y_pred
# df_result['ride_id'] = f'{year:04d}/{month:02d}_' + df_result.index.astype('str')
# df_result.to_parquet(
#     output_file,
#     engine='pyarrow',
#     compression=None,
#     index=False
# )
