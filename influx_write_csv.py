import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import csv
import time
import logging
import yaml


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


# Create an InfluxDB client instance
client = influxdb_client.InfluxDBClient(url=url,token=token,org=org)

# Ping the InfluxDB instance
is_connected = client.ping()

# Check the ping response
if is_connected:
    logging.info("InfluxDB client is successfully connected.")
else:
    logging.info("Failed to connect to InfluxDB client.")


# Configure write api client
write_api = client.write_api(write_options=SYNCHRONOUS)

# write_type: The write consistency level for the data points. \\
# Valid values are "sync" (write to disk and return when complete) and "async" (write to cache and return immediately). \\
#  If not specified, the default write type of "sync" will be used.


# To detect empty string in csv rows and convert into 0.0
def emptystr_processor(row_value):
    if row_value == '':
        return float(0.0)
    else:
        return float(row_value)

# To count total rows of csv file
counter = 0

# read sample data
with open('Toronto_temp.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:

        # Timestamp for input
        timestmp = datetime.utcnow().isoformat()

        # InfluxDB time error : 
        # I noticed, that the time was not correctly formatted in the json.
        # So I had to correct the time format to datetime.datetime.utcnow().isoformat() which will be '2020-08-15T14:36:24.025388'
        # https://github.com/influxdata/influxdb-python/issues/762


        # Use default dictionary structure
        data_dict = {
            "measurement": "weather",
            "tags": {"location": "Toronto", "season": row["season"]},
            "fields": {"Mean Temp (C)": emptystr_processor(row["Mean Temp (C)"]),
            "Max Temp (C)": emptystr_processor(row["Max Temp (C)"]),
            "Min Temp (C)": emptystr_processor(row["Min Temp (C)"]),
            "Total Rain (mm)": emptystr_processor(row["Total Rain (mm)"]),
            "Total Snow (cm)": emptystr_processor(row["Total Snow (cm)"]),
            "Total Precip (mm)": emptystr_processor(row["Total Precip (mm)"]),
            },
            "time": timestmp
        }

        # Build Data Dict as point 
        data_point = influxdb_client.Point.from_dict(data_dict)

        # Write data to InfluxDB
        write_result = write_api.write(bucket=bucket, org=org, record=data_point)

        # increase counter
        counter = counter + 1

        logging.info("Data write success. Row number : {}".format(counter))

        time.sleep(5)


