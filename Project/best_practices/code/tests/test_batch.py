import math

import batch


def test_predict():

    energy_usage = {
        "Visibility": 59.166667,
        "RH_5": 55.200000,
        "Windspeed": 6.666667,
        "RH_out": 92.000000,
    }
    # Actual output from data   = 60

    actual_prediction = math.floor(batch.predict(energy_usage))

    expected_prediction = 104

    assert actual_prediction == expected_prediction
