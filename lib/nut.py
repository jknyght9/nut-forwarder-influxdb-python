import logging
from lib.nut2 import PyNUTClient, PyNUTError

logger = logging.getLogger('nut-forwarder-influxdb.nut')

datastruct = [
    "battery.charge",
	"battery.runtime",
	"battery.voltage",
	"input.voltage",
	"output.voltage",
    "ups.load",
    "ups.power.nominal",    #watts
    "ups.serial",
	"ups.status",
]

def convertToMinutes(runtime):
    return int(runtime) / 60

def getNutData(nutservers):
    upsdata = []
    for server in nutservers:
        try:
            if logger.getEffectiveLevel == 10:
                client = PyNUTClient(host=server['server'], debug=True)
            else:
                client = PyNUTClient(host=server['server'])
            upss = client.list_ups()
            if upss:
                for ups in upss:
                    fields = pruneData(client.list_vars(ups))
                    data = {"server": server["name"], "name": ups, "description": upss[ups], "serial": fields["ups.serial"] if "ups.serial" in fields is not None else "", "data": fields}
                    logger.debug(data)
                    upsdata.append(data)
            else:
                logger.error('no UPSs found connected to server')
        except PyNUTError as e:
            logger.error('could not connect to %s, %s', server['server'], e)
    return upsdata


def lookupStatus(status):
    lookuptable = {
        "LB": "Low battery",
        "OB": "On battery",
        "OB DISCHRG": "On battery",
        "OL": "On line",
        "OL CHRG": "On line (Charging)",
        "SD": "Shutdown load"
    }
    return lookuptable.get(status, "Unknown")

def pruneData(nutdata):
    prunedData = {}
    for data in datastruct:
        if data in nutdata:
            if data == "ups.status":
                prunedData[data] = lookupStatus(nutdata[data])
            elif data == "battery.runtime":
                prunedData[data] = convertToMinutes(nutdata[data])
            elif data == "ups.serial" and nutdata[data] is not None:
                prunedData[data] = nutdata[data]
            else:
                prunedData[data] = float(nutdata[data])
    return prunedData
