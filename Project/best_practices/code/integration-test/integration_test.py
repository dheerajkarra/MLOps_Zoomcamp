#!/usr/bin/env python
# coding: utf-8

import os

import pandas as pd

# options = {"client_kwargs": {"endpoint_url": "http://localhost:4566"}}
# input_file = f"s3://energy-usage/in/energy_train.csv"
input_file = "energy_sample.csv"

data = [
    (43.833333, 55.030000, 5.333333, 92.000000),  #       50
    (63.000000, 55.200000, 7.000000, 92.000000),  #      60
    (40.000000, 56.933333, 6.000000, 88.500000),  #         70
]

select_features = ['Visibility', 'RH_5', 'Windspeed', 'RH_out']
df_input = pd.DataFrame(data, columns=select_features)

df_input.to_csv(input_file, index=False)

os.system(f"cd .. && conda run python batch.py")

df = pd.read_csv("predictions.csv")
print("Showing output of predictions.csv....")
print(df)
