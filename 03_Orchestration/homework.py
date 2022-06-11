# C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\Data

import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner

import prefect



@task
def read_data(path):
    df = pd.read_parquet(path)
    return df

@task
def prepare_features(df, categorical, train=True):
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        print(f"The mean duration of training is {mean_duration}")
    else:
        print(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

@task
def train_model(df, categorical):

    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    print(f"The shape of X_train is {X_train.shape}")
    print(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    print(f"The MSE of training is: {mse}")
    return lr, dv

@task
def run_model(df, categorical, dv, lr):
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    print(f"The MSE of validation is: {mse}")
    # logger = prefect.context.get("logger")
    logger = get_run_logger()
    logger.info(f"The MSE of validation is: {mse}")
    return

from datetime import date
from datetime import datetime 
import dateutil.relativedelta   

@task
def get_paths(date_par):
    if date_par is None:
        date_run = date.today()
    else:
        date_run = date_par
        date_run = datetime.strptime(date_run, '%Y-%m-%d')             
    train_date = date_run - dateutil.relativedelta.relativedelta(months=1)
    test_date = date_run - dateutil.relativedelta.relativedelta(months=2)
     
    train_path = 'C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\Data\\fhv_tripdata_' + str(train_date.year) + '-' + f'{train_date.month:02d}' + '.parquet' 
    val_path = 'C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\Data\\fhv_tripdata_' + str(test_date.year) + '-' + f'{test_date.month:02d}' + '.parquet'
    return train_path, val_path

import pickle
@flow
def main(date_par=None):
    train_path, val_path = get_paths(date_par).result()

    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path).result()
    df_train = df_train.head(1000)
    df_train_processed = prepare_features(df_train, categorical)

    df_val = read_data(val_path).result()
    df_val = df_val.head(1000)
    df_val_processed = prepare_features(df_val, categorical, False)

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()
    with open("C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\Data\\model-"+ str(date_par) + '.bin', "wb") as f_out:
        pickle.dump(dv, f_out)
    # lr.save('C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\Data\\model-' + str(date_par) + '.bin' )
    with open("C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\Data\\dv-"+ str(date_par) + '.b', "wb") as f_out:
        pickle.dump(dv, f_out)
    run_model(df_val_processed, categorical, dv, lr)

main(date_par="2021-08-15")


# C:\\Users\\Satya\\Desktop\\Projects\\MLOps\\Data
# @flow(task_runner=SequentialTaskRunner())

# train_model
# The MSE of validation is: 11.859451053072702
# 13,000 bytes
# 0 9 15 * *   - 9 AM 15th of every month
# 
# prefect work-queue ls

# C:\\Users\\Satya\\.prefect

from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import IntervalSchedule, CronSchedule
from prefect.flow_runners import SubprocessFlowRunner
# from datetime import timedelta

DeploymentSpec(
    flow=main,
    name="model_training",
    # schedule=IntervalSchedule(interval=timedelta(weeks=1)),
    schedule=CronSchedule(cron='0 9 15 * *', timezone='CET', day_or=False),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml"],
)