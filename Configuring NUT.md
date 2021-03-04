# Network UPS Tools (NUT)

## NUT on Synology

By default, NUT is installed on Synology, you will have to enable network UPS server and input the device that will be connecting to the NUT server

## NUT Client Setup

1. Install the NUT client on the device
2. Edit the `/etc/nut/nut.conf` file and input the following

```
MODE=netclient
```

3. Edit the `/etc/nut/upsmon.conf` and input the following

```
# MONITOR <system> <powervalue> <username> <password> ("master"|"slave")
MONITOR ups@IPADDR 1 monuser secret slave
```

4. Restart the service

## NUT Server Setup

1. Install the NUT server on the device
2. Edit the `/etc/nut/nut.conf` file and input the following

```
MODE=nutserver
```

3. Edit the `/etc/nut/ups.conf` file and input the following

```
[ups]
        driver = usbhid-ups
        port = auto
        desc = "APC SmartUPS 1500"
```

4. Edit the `/etc/nut/upsd.conf` file and input the following

```
LISTEN 127.0.0.1 3493
LISTEN 0.0.0.0 3493
```

5. Edit the `/etc/nut/upsmon.conf` file and input the following

```
MONITOR ups@localhost 1 upsmon_local secret master
```

# References
[https://yegor.pomortsev.com/post/monitoring-everything/](https://yegor.pomortsev.com/post/monitoring-everything/)
[https://www.reddit.com/r/synology/comments/gtkjam/use_synology_nas_as_ups_server_to_safely_power/](https://www.reddit.com/r/synology/comments/gtkjam/use_synology_nas_as_ups_server_to_safely_power/)
[https://diktiosolutions.eu/en/synology/synology-ups-nut-en/](https://diktiosolutions.eu/en/synology/synology-ups-nut-en/)