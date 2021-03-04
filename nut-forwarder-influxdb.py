import argparse
import json
import logging
import os
import sched
import sys
from telnetlib import EC
import time
from datetime import datetime
from lib.config import generateConfig
from lib.influx import send, test
from lib.nut import getNutData

s = sched.scheduler(time.time, time.sleep)

def pushNut2Influx(sc, nutservers, influxserver):
    nutdata = getNutData(nutservers)
    for nd in nutdata:
        send(influxserver, {
            "measurement": "ups",
            "tags": {
                "server": nd["server"],
                "name": nd["name"],
                "description": nd["description"],
                "serial": nd["serial"]
            },
            "fields": nd["data"],
            "time": datetime.utcnow()
        })
    s.enter(60, 1, pushNut2Influx, (sc, nutservers, influxserver,))

def main():
    parser = argparse.ArgumentParser(description="Forwards NUT data to InfluxDB")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--generateconfig", action="store_true", help="Generate configuration file")
    group.add_argument("-r", "--run", action="store_true", help="Run the program")
    parser.add_argument("-d", "--debug", action="store_true", help="Run in debug mode")
    options = parser.parse_args()

    logginglevel = logging.INFO
    if options.debug:
        logginglevel = logging.DEBUG
    logger = logging.getLogger("nut-forwarder-influxdb")
    logger.setLevel(logginglevel)
    formatter = logging.Formatter(
        '%(asctime)s %(name)s [%(levelname)s] %(message)s')
    cs = logging.StreamHandler()
    cs.setFormatter(formatter)
    logger.addHandler(cs)

    if options.generateconfig:
        generateConfig()
    elif options.run:
        if os.path.exists("config.json"):
            config = None
            with open("config.json", "rb") as f:
                config = f.read()
                config = json.loads(config)
                f.close()
            if config["influxserver"] is not None and config["nutservers"] is not None:
                logger.info("connecting to Influx server %s", config["influxserver"]["server"])
                if test(config["influxserver"]):
                    logger.info("logging data to Influx server")
                    if getNutData(config["nutservers"]) is not None:
                        logger.info("connected to NUT server(s)")
                        s.enter(0, 1, pushNut2Influx, (s, config["nutservers"], config["influxserver"],))
                        s.run()
                    else:
                        exit()
                else:
                    exit()
        else:
            logger.error("configuration file does not exist. Rerun this program with the '-g' parameter.")
            exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
