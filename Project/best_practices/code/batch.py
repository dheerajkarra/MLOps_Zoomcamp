import os
import pickle

import pandas as pd


def get_input_path():
    # default_input_pattern = 'github.com/data/energy_train.csv'
    default_input_pattern = 'energy_val.csv'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern


def get_output_path():
    # default_output_pattern = 's3://energy-usage/predictions.csv'
    default_output_pattern = 'integration-test/predictions.csv'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern


def predict(features):

    with open('lin_reg.bin', 'rb') as f_in:
        (dv, model) = pickle.load(f_in)

    X = dv.transform(features)
    preds = model.predict(X)
    return float(preds[0])


def read_data(filename):
    # S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT")
    # options = {'client_kwargs': {'endpoint_url': S3_ENDPOINT_URL}}
    return pd.read_csv(filename)


def save_data(df, filename):
    # S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT")
    # options = {'client_kwargs': {'endpoint_url': S3_ENDPOINT_URL}}
    df.to_csv(filename, index=False)


def main():

    input_file = get_input_path()
    output_file = get_output_path()

    with open('lin_reg.bin', 'rb') as f_in:
        (dv, lr) = pickle.load(f_in)

    select_features = ['Visibility', 'RH_5', 'Windspeed', 'RH_out']

    df = read_data(input_file)   

    dicts = df[select_features].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    df_result = pd.DataFrame()
    df_result['predicted_energy_usage'] = y_pred

    save_data(df_result, output_file)


if __name__ == '__main__':
    main()
