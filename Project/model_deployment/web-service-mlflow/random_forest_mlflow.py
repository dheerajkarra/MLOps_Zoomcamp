import pickle
import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("energy-prediction-deploy")

def read_dataframe(filename: str):
    df = pd.read_csv(filename)
    return df


def prepare_dictionaries(df: pd.DataFrame):
    select_features = ['Visibility', 'RH_5', 'Windspeed', 'RH_out']
    dicts = df[select_features].to_dict(orient='records')
    return dicts

df_train = read_dataframe('data/energy_train.csv')
df_val = read_dataframe('data/energy_val.csv')

target = 'Appliances'
y_train = df_train[target].values
y_val = df_val[target].values

dict_train = prepare_dictionaries(df_train)
dict_val = prepare_dictionaries(df_val)
with mlflow.start_run():
    params = dict(max_depth=20, n_estimators=100, min_samples_leaf=10, random_state=0)
    mlflow.log_params(params)

    pipeline = make_pipeline(
        DictVectorizer(),
        RandomForestRegressor(**params, n_jobs=-1)
    )

    pipeline.fit(dict_train, y_train)
    y_pred = pipeline.predict(dict_val)

    rmse = mean_squared_error(y_pred, y_val, squared=False)
    print(params, rmse)
    mlflow.log_metric('rmse', rmse)

    mlflow.sklearn.log_model(pipeline, artifact_path="model")