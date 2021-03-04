from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
import logging

logger = logging.getLogger('nut-forwarder-influxdb.influx')

def send(options, influxdata):
    client = InfluxDBClient(url=options["server"], token=options["token"], org=options["organization"], timeout=6000)
    logger.debug("connection established")
    write_api = client.write_api(write_options=ASYNCHRONOUS)
    write_api.write(options["bucket"], options["organization"], influxdata)
    logger.debug("writing to bucket %s", options["bucket"])
    logger.debug("writing to organization %s", options["organization"])
    logger.debug("writing data %s", influxdata)
    write_api.__del__()
    client.__del__()
    logger.debug("closing connection")

def test(options):
    answer = False
    try:
        client = InfluxDBClient(url=options["server"], token=options["token"], org=options["organization"], timeout=10000)
        query_api = client.query_api()
        query_api.query_stream('from(bucket:"ups") |> range(start: -10m)')
        answer = True
    except Exception as e:
        logger.error('could not connect to InfluxDB server: %s.', str(e))
    finally:
        client.__del__()
        return answer
