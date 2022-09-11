import requests

energy_usage = {
    "Visibility": 40,
    "RH_5": 53.5,
    "Windspeed": 5,
    "RH_out": 89
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=energy_usage)
print(response.json())

