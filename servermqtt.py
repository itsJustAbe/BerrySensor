#!/usr/bin/env python

import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
  #if msg.payload.decode() == "Hello world!":
  print(msg.payload.decode())


client = mqtt.Client()
#client.connect("192.148.43.57",1883,60)
client.connect("127.0.0.1",1883,60)

client.on_connect = on_connect
#client.on_message = on_message

while True:
    client.on_message = on_message
    print "sleep for 1 sec"
    time.sleep(1)

#client.loop_forever()

#client.disconnect()