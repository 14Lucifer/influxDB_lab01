import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta, timezone
import yaml

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
# Create an InfluxDB client instance
client = influxdb_client.InfluxDBClient(url=url,token=token,org=org)

# Ping the InfluxDB instance
is_connected = client.ping()

# Check the ping response
if is_connected:
    print("InfluxDB client is successfully connected.")
else:
    print("Failed to connect to InfluxDB client.")


# Define an InfluxDB query to retrieve data
query = f'from(bucket:"{bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "weather")'

# Query data from InfluxDB
result = client.query_api().query(org=org, query=query)

# Print the query result
for table in result:
    for record in table.records:
        print(record)