import requests

url = 'http://127.0.0.1:9696/predict'

energy_usage = {
    "Visibility": 40,
    "RH_5": 53.5,
    "Windspeed": 5,
    "RH_out": 89
}

response = requests.post(url, json=energy_usage)
print(response.json())
# {'energy_usage': 99.32116962266376}  -> output obtained