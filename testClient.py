import paho.mqtt.client as mqtt
import time

# This is the Publisher

# Add client Ip address on the same network
CLIENT_IP = "" 
client = mqtt.Client()

client.connect(CLIENT_IP, 1883, 60)
i = 0
word = 'give me that mac!'

while i < 10:
    word = word + " " + str(i)
    print "sending data"
    client.publish("topic/test", word)
    i = i + 1
    time.sleep(2)
    
print "disconnecting..."    
client.disconnect()
