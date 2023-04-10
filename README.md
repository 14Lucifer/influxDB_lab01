# influxDB_lab01
The repo contains the python scripts/simple app to test influxDB.

The weather_sink is a containerized application which will call weather API at every configured interval and sink the data into influxDB. Sinked data will be visualized and monitored from InfluxDB UI.

The weather API is from https://www.weatherapi.com/my/ and "Weather API" provide free API package which will allow you to call 1 million API per month.

With current config, weather application will gather the real time weather information of emirates of UAE.

This is very simple application created for learning purpose only and the sane scenarios can be applied to montior exchange rate of crypto currencies, metric data from IOT devices and more.


Python and library versions
---------------------------
Python 3.10.8

Package            Version
------------------ ---------
influxdb-client    1.36.1
PyYAML             6.0
requests           2.28.2