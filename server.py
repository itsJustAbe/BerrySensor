#!/usr/bin/python

import time
import os
import select
from datetime import datetime
import bluetooth
import paho.mqtt.client as mqtt
from logentries import LogentriesHandler
import logging
import pyowm

# sensor utils
import sensor


# Getting external weather data to compare with internal temperature and humididty 
def get_weather():

    user_id = os.uname()[1]
    protocol="EXTERNAL"

    owm = pyowm.OWM('1d11da8b7fd7895acd7d78bf97be9839')
    observation = owm.weather_at_place('Dublin,IE')
    weather = observation.get_weather()
    humidity = weather.get_humidity()
    temperature = weather.get_temperature('celsius')["temp"]
    
    format_string = '{}  Protocol={} SensorID={}, temperature={}, humidity={} \n'.format(str(datetime.now()), protocol,
                                                                                             user_id,temperature, humidity)
    log.info(format_string)

# Format string to be sent to log entries
def get_reading(protocol):
    humidity, temperature, user_id = sensor.temp()

    format_string = '{}  Protocol={} SensorID={}, temperature={}, humidity={} \n'.format(str(datetime.now()), protocol,
                                                                                             user_id,temperature, humidity)
    return format_string 

# Connect to the mqtt publisher
def mqtt_connect():
    # create mqtt connection
    client = mqtt.Client()
    client.connect("127.0.0.1",1883,60)
    client.loop_start()
    return client

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/test")


def on_message(client, userdata, msg):
    # get mqtt message and send to logentries
    mqtt_msg = msg.payload.decode()
    if mqtt_msg:
        print "Mqtt message:", mqtt_msg
        log.info(mqtt_msg)

def send_mqtt_data(client):
    client.on_connect = on_connect
    client.on_message = on_message

# Creating bluetooth server
def bluetooth_connect():
    # set bluetooth
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)
    client_sock,address = server_sock.accept()
    print "Accepted connection from ",address
    return client_sock

# Recieve data coming from bluetooth and send to log entries
def send_bluetooth_data(client_sock):
    try:
        print "checking for bluetooth message!"
        client_sock.setblocking(0)
        
        ready = select.select([client_sock], [], [], 1)
        if ready[0]:
            remote_data = client_sock.recv(4096)
        #remote_data = client_sock.recv(1024)
        if remote_data:
            print "Remote data:", remote_data
            log.info(remote_data)
    except:
        pass

# send data from local gateway server
def send_local_log():
    log_line = get_reading("LOCAL")
    log.info(log_line)


# Set lognetires
log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
log.addHandler(LogentriesHandler('68664606-5dfc-4ea0-971f-5fa77b4fa558'))

client_sock = bluetooth_connect()
client = mqtt_connect()
send_mqtt_data(client)

while True:
    get_weather()
    send_local_log()
    print "Receive data from MQTT\n"
    send_mqtt_data(client)
    print "Receive data from Bluetooth\n"
    send_bluetooth_data(client_sock)
    time.sleep(2)


client_sock.close()
server_sock.close()

