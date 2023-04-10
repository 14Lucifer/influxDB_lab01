import requests
import yaml
import json
from datetime import datetime

# Load configuration from yaml file
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# yaml.load() function to load the YAML data into a Python object. 
# We pass the Loader=yaml.FullLoader argument to specify the YAML parser to use.

# InfluxDB connection details
api_key = config["weather_api"]["api_key"]
city = config["weather_api"]["city"]


# Define the API URL
url = 'http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no'.format(api_key,city[6])

# Call the API
response = requests.get(url)

# Print the response data
resp_data = response.json()

# Timestamp for input
timestmp = datetime.utcnow().isoformat()

# data formating
data_dict = {
            "measurement": "weather",
            "tags": {"region": resp_data["location"]["region"], "country": resp_data["location"]["country"]},
            "fields": {"temp_c": resp_data["current"]["temp_c"],
                       "temp_f": resp_data["current"]["temp_f"],
                       "wind_mph": resp_data["current"]["wind_mph"],
                       "wind_kph": resp_data["current"]["wind_kph"],
                       "wind_degree": resp_data["current"]["wind_degree"],
                       "wind_dir": resp_data["current"]["wind_dir"],
                       "pressure_mb": resp_data["current"]["pressure_mb"],
                       "pressure_in": resp_data["current"]["pressure_in"],
                       "precip_mm": resp_data["current"]["precip_mm"],
                       "precip_in": resp_data["current"]["precip_in"],
                       "humidity": resp_data["current"]["humidity"],
                       "cloud": resp_data["current"]["cloud"],
                       "feelslike_c": resp_data["current"]["feelslike_c"],
                       "feelslike_f": resp_data["current"]["feelslike_f"],
                       "vis_km": resp_data["current"]["vis_km"],
                       "vis_miles": resp_data["current"]["vis_miles"],
                       "uv": resp_data["current"]["uv"],
                       "gust_mph": resp_data["current"]["gust_mph"],
                       "gust_kph": resp_data["current"]["gust_kph"]
            },
            "time": timestmp
        }

print(data_dict)