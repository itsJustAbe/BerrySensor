import bluetooth
import sensor
import datetime
import sys
import time


def bluetooth_msg():
    # Kruno's Bluetooth
    bd_addr = "B8:27:EB:94:1F:03"

    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    while True:
        try:
             # assembling data received from the sensor
             log_line = sensor.temp()
             # sending data
             sock.send(log_line)
             # sleep time
             time.sleep(5)
       
        except:
            print("connection error")
            
bluetooth_msg()
