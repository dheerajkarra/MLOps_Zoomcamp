import argparse
import os
import pickle
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def dump_pickle(obj, filename):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)
    
def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

# def read_dataframe(filename: str):
#     df = pd.read_csv(filename)
#     return df

# raw_data_path = 'F:\\Projects\\MLOps\\MLOps_Zoomcamp\\Project\\experiment_tracking_and_model_registry\\'
# dest_path = 'F:\\Projects\\MLOps\\MLOps_Zoomcamp\\Project\\experiment_tracking_and_model_registry\\'

def run(raw_data_path: str, dest_path: str):
    
    energy_df = pd.read_csv(os.path.join(raw_data_path, "energydata_complete.csv"))
    energy_df = energy_df.drop('date', axis = 1)
    energy_df = energy_df[0:5000]

    y = energy_df['Appliances']
    X = energy_df.drop('Appliances', axis = 1)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 37)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2, random_state=37)
    
    sc = StandardScaler()
    
    X_train = sc.fit_transform(X_train)
    X_valid = sc.fit_transform(X_valid)
    X_test = sc.fit_transform(X_test)
    
    # create folder unless it already exists
    os.makedirs(dest_path, exist_ok=True)
    
    dump_pickle((X_train, y_train), os.path.join(dest_path, "train.pkl"))
    dump_pickle((X_valid, y_valid), os.path.join(dest_path, "valid.pkl"))
    dump_pickle((X_test, y_test), os.path.join(dest_path, "test.pkl"))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_data_path",
        default="./input",
        help="Path of raw data"
    )
    parser.add_argument(
        "--dest_path",
        default="./output",
        help="Path for output files"
    )
    args = parser.parse_args()

    run(args.raw_data_path, args.dest_path)

