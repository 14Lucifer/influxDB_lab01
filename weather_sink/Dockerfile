# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install any needed packages
RUN pip install influxdb-client==1.36.1
RUN pip install PyYAML==6.0
RUN pip install requests==2.28.2

# Copy the rest of the application code into the container
COPY ./config.yaml .
COPY ./weather_sink.py .

# Set the environment variable to indicate the application's entry point
ENV WEATHER_APP=weather_sink.py

# Run the command to start the application
CMD ["python","WEATHER_APP"]
