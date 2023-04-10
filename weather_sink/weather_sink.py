import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import time
import logging
import yaml
import requests
import sys


# Configure the logging module
logging.basicConfig(filename='write.log', level=logging.INFO,format='%(asctime)s : %(levelname)s : %(message)s')

# Create a StreamHandler to log messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
logging.getLogger().addHandler(console_handler)



# Load configuration from yaml file
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# yaml.load() function to load the YAML data into a Python object. 
# We pass the Loader=yaml.FullLoader argument to specify the YAML parser to use.

# InfluxDB connection details
url = config["influxDB"]["url"]
token = config["influxDB"]["token"]
org = config["influxDB"]["org"]
bucket = config["influxDB"]["bucket"]
measurement = config["influxDB"]["measurement"]

# Weather API details
api_key = config["weather_api"]["api_key"]
city = config["weather_api"]["city"]

# data sync interval
sync_interval = city = config["data_sink_interval"]


# Create an InfluxDB client instance
client = influxdb_client.InfluxDBClient(url=url,token=token,org=org)

# Ping the InfluxDB instance
is_connected = client.ping()

# Check the ping response
if is_connected:
    logging.info("InfluxDB client is successfully connected.")
else:
    logging.info("Failed to connect to InfluxDB client.")
    sys.exit(1)


# Configure write api client
write_api = client.write_api(write_options=SYNCHRONOUS)

# write_type: The write consistency level for the data points. \\
# Valid values are "sync" (write to disk and return when complete) and "async" (write to cache and return immediately). \\
#  If not specified, the default write type of "sync" will be used.


#  function to call weather API based on region and put the response influxDB data syntax
def weather_api(region, timestmp):
    # calling weather API
    url = 'http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no'.format(api_key,region)

    # API response
    response = requests.get(url)

    # getting weather data
    resp_data = response.json()

    # data formating
    weather_data = {
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
    
    return weather_data


while True:

    try:
        # Timestamp for input
        timestmp = datetime.utcnow().isoformat()

        influx_data_dict = []

        # get weather data for each city and append to list
        for i in config["weather_api"]["city"]:
            influx_data_dict.append(weather_api(region=i,timestmp=timestmp))
            
        logging.info("Getting weather data for cities successful.\ncities : {} ,{} ,{} ,{} ,{} ,{} ,{}".format(
            config["weather_api"]["city"][0],
            config["weather_api"]["city"][1],
            config["weather_api"]["city"][2],
            config["weather_api"]["city"][3],
            config["weather_api"]["city"][4],
            config["weather_api"]["city"][5],
            config["weather_api"]["city"][6]
            ))

        # inserting data into influxDB
        write_call = write_api.write(bucket, org, influx_data_dict)

        logging.info("InfluxDB data insert successful")

        # call the API every 5 sec
        time.sleep(10)
        
    except Exception as e:
        logging.error(e)
        sys.exit(1)


 