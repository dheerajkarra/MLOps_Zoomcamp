import argparse
import os
import pickle

import mlflow
import numpy as np
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# os.environ["AWS_PROFILE"] = "default"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("energy-hyperopt-random-forest_2")


def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def run(data_path, num_trials):
    
    mlflow.sklearn.autolog(disable=True)

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_valid, y_valid = load_pickle(os.path.join(data_path, "valid.pkl"))
    

    def objective(params):
        
        with mlflow.start_run():
            mlflow.set_tag("developer","Dheeraj")
            mlflow.set_tag("model", "randomforest")
            mlflow.log_params(params)
            rf = RandomForestRegressor(**params)
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_valid)
            rmse = mean_squared_error(y_valid, y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)
            mlflow.sklearn.log_model(rf, artifact_path="model")

        return {'loss': rmse, 'status': STATUS_OK}

    search_space = {
        'max_depth': scope.int(hp.quniform('max_depth', 1, 8, 1)),
        'n_estimators': scope.int(hp.quniform('n_estimators', 10, 50, 1)),
        'min_samples_split': scope.int(hp.quniform('min_samples_split', 2, 5, 1)),
        'min_samples_leaf': scope.int(hp.quniform('min_samples_leaf', 1, 5, 1)),
        'random_state': 37
    }

    rstate = np.random.default_rng(37)  # for reproducible results
    fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=num_trials,
        trials=Trials(),
        rstate=rstate
    )


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default="./output",
        help="Path of processed data"
    )
    parser.add_argument(
        "--max_evals",
        default=10,
        help="Maximum number of parameter combinations of optimizer"
    )
    args = parser.parse_args()

    run(args.data_path, args.max_evals)