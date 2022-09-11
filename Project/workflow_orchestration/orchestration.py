import pandas as pd
import pickle
import requests as req
import os

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from prefect import flow, task, get_run_logger 
# from prefect.logging import get_run_logger
from prefect.task_runners import SequentialTaskRunner
# from prefect.context import ContextModel
# from prefect.filesystems import S3

# os.chdir("F:\\Projects\\MLOps\\MLOps_Zoomcamp\\Project\\workflow_orchestration\\")

data_dir = "data"

@task
def read_data(filename: str):
    df = pd.read_csv(filename)
    return df

@task
def train_model(df, select_features):
    
    logger = get_run_logger()
    # logger = prefect.context.get("logger")
    train_dicts = df[select_features].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.Appliances.values

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    logger.info(f"The MSE of training is: {mse}")
    return (lr, dv)

@task
def run_model(df, select_features, dv, lr):
    logger = get_run_logger()
    val_dicts = df[select_features].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.Appliances.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"The MSE of validation is: {mse}")
    return
        
@flow(name="main", task_runner=SequentialTaskRunner())
def main():
    
    df_train = read_data(os.path.join(data_dir, "energy_train.csv"))
    df_val = read_data(os.path.join(data_dir, "energy_val.csv"))
    
    select_features = ['Visibility', 'RH_5', 'Windspeed', 'RH_out']
    
    # train the model
    output = train_model(df_train, select_features).result()
    lr = output[0]
    dv = output[1]
    run_model(df_val, select_features, dv, lr)
    
    with open('models/lin_reg.pkl', 'wb') as f_out:
        pickle.dump((lr), f_out)
    
    with open('models/dv.pkl', 'wb') as f_out:
        pickle.dump((dv), f_out)
    
    # block = S3(bucket_path="{bucket-name}/prefect-orion", aws_access_key_id="{your aws_access_key_id}", aws_secret_access_key="{your aws_secret_access_key}")
    # block.save("mlops-project-block", overwrite=True)

main()

# Setting the deployment periodically using crontab such that only one deployment 
# is scheduled for this run

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
