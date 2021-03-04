# Network UPS Tool Forwarder to InfluxDB (Python)

Forwards Network UPS Tool data to InfluxDB for monitoring and alerting. Program polls all configured NUT servers and the UPS's connected to them. All data is pushed to the **ups** bucket in the InfluxDB server.

## Standalone
The program can be ran in standalone mode. Access the help menu with the `-h` argument.

```bash
# help menu
python3 nut-forwarder-influxdb.py -h
usage: nut-forwarder-influxdb.py [-h] [-g | -r] [-d]

Forwards NUT data to InfluxDB

optional arguments:
  -h, --help            show this help message and exit
  -g, --generateconfig  Generate configuration file
  -r, --run             Run the program
  -d, --debug           Run in debug mode
```

Here create a configuration file with the `-g` argument. You will be asked for:

```bash
# generate the configuration file
python3 nut-forwarder-influxdb.py -g

or 

python3 nut-forwarder-influxdb.py --generateconfig
```

**NUT Parameters**

Parameter|Description
---|---
Name|NUT server description
Server|NUT server IP or hostname
Username|NUT server credential
Password|NUT server credential

**InfluxDB Parameters**

Parameter|Description
---|---
Server|InfluxDB server IP or hostname
Version|InfluxDB server version
Token|Base64 user token
Bucket|Target bucket for all information
Organization|InfluxDB organization

Once the configuration file is generated, run the program with the `-r` argument.

```bash
# running the forwarder
python3 nut-forwarder-influxdb.py -r

or

python3 nut-forwarder-influxdb.py --run
```

You can also generate debugging information using the `-d` argument.

```bash
# running with debug
python3 nut-forwarder-influxdb.py -r -d

or 

python3 nut-forwarder-influxdb.py --run --debug
```

## Docker

Once the configuration file has been generated, the program can also be ran in a docker container using the following commands

#### Build (after config.json file is generated)

`docker build -t nut-forwarder-influxdb .`

#### Running container

`docker run nut-forwarder-python`

#### Saving container

`docker save nut-forwarder-influx-python:latest | gzip > nut-forwarder-influx.tar.gz`