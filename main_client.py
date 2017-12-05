import time
from datetime import datetime
import bluetooth
import sensor
import paho.mqtt.client as mqtt

CLIENT_IP = "" 

def mqtt_connect():
    # Connect to MQTT
    client = mqtt.Client()
    client.connect(CLIENT_IP, 1883, 60)
    return client
    

def bluetooth_connect(sock):
    # Kruno's Bluetooth
    bd_addr = "B8:27:EB:94:1F:03"
    port = 1
    # connecting to the said device
    sock.connect((bd_addr, port))
    

def get_reading(protocol):
    humidity, temperature, user_id = sensor.temp()
    # formatting data to be sent to the bluetooth device
    format_string = '{}  Protocol={} SensorID={}, temperature={}, humidity={} \n'.format(str(datetime.now()), protocol,
                                                                                             user_id,temperature, humidity)
    return format_string 

def bluetooth_msg(sock):
    try:
        # assembling data received from the sensor
        log_line = get_reading("RFCOMM")
        # sending data
        sock.send(log_line)
        # sleep time
        time.sleep(5)

    except:
        print("connection error")


def mqtt_msg(client):
    # The message
    log_line = get_reading("MQTT")
    print ("sending data")
    # Publishing message to be recived by the other pi
    client.publish("topic/test", log_line)
    # SLeep timer
    time.sleep(5)

# Connect to the bluetooth device
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
bluetooth_connect(sock)

while True:
    
    # The time constraint 1 hour =  10 seconds, runs for 2 minutes
    t_end = time.time() + 60 * 2
    client = mqtt_connect()

    #start sending with MQTT
    while time.time() < t_end:
            mqtt_msg(client) 
    # Console Output         
    print ("Handing off to RFCOMM")
    
    # Time constraint running for 2 minutes
    t_end = time.time() + 60 * 2
    
    # Start Bluetooth
    while time.time() < t_end:
        bluetooth_msg(sock)
    # Console output
    print ("Handing off to MQTT") 
   








