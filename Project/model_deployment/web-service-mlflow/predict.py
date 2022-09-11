import os

import mlflow
from flask import Flask, request, jsonify

# RUN_ID = os.getenv('RUN_ID')
RUN_ID = '314ef1fd7ef04fe086e32af07948c74b'
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

# logged_model = f's3://{enter-the-name-of-your-S3-bucket-here}/1/{RUN_ID}/artifacts/model'
logged_model = f'F:\\Projects\\MLOps\\MLOps_Zoomcamp\\Project\\model_deployment\\web-service-mlflow\\mlruns\\8\\{RUN_ID}\\artifacts\\model'

model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(energy_usage):
    features = {}
    features = energy_usage
    return features

def predict(features):
    preds = model.predict(features)
    return float(preds[0])

app = Flask('energy-usage-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():    
    energy_usage = request.get_json()
    features = prepare_features(energy_usage)
    pred = predict(features)
    
    result = {
        'energy_usage': pred,
        'model_version': RUN_ID
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)