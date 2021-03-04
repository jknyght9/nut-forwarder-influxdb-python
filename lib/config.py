import json

config = {}

def getNut():
    name = input("NUT Server Name: ")
    server = input("NUT Server IP address: ")
    username = input("Username: ")
    password = input("Password: ")
    return {"name": name, "server": server, "username": username, "password": password}

def getInfluxDb():
    influxdb = {}
    while (True):
        version2 = input("InfluxDB Version2: (Y|N): ")
        if version2.upper() == "Y":
            server = input("InfluxDB Server IP address: ")
            token = input("Token: ")
            bucket = input("Bucket: ")
            organization = input("Organization: ")
            influxdb = {"server": server, "version": "2", "token": token, "bucket": bucket, "organization": organization}
            break
        elif version2.upper() == "N":
            server = input("InfluxDB Server IP address: ")
            database = input("Database: ")
            username = input("Username: ")
            password = input("Password: ")
            influxdb = {"server": server, "version": "1", "database": database, "username": username, "password": password}
            break
    return influxdb

def generateConfig():
    nutserver = []
    while(True):
        nutserver.append(getNut())
        prompt = input("More NUT Servers? (Y|N): ")
        if prompt.upper() == "N":
            break
    influxserver = getInfluxDb()
    config = {"nutservers": nutserver, "influxserver": influxserver}
    with open("config.json", "w") as f:
        f.write(json.dumps(config))
        f.close()