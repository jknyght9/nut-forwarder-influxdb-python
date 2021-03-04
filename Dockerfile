FROM python:3.9.2-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python3", "nut-forwarder-influxdb.py", "-r" ]