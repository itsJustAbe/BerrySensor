import bluetooth
import sensor
import SensorScript
import datetime
import sys
import time


def node():

    USER_ID = sys.argv[2]

    # Kruno's Bluetooth
    bd_addr = "B8:27:EB:94:1F:03"

    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    # iterator
    i = 0

    while True:

        # date and time object to log current time
        date_time_object = datetime.datetime.now()

        # assembling data received from the sensor
        data = SensorScript.assembler(date_time_object,
                                      sensor.temp(),
                                      USER_ID)

        # sending data
        sock.send(data)

        # sleep time
        time.sleep(5)

        # Iterator
        i = i + 1

    sock.close()


if len(sys.argv) > 4:
    print("Accepted parameter format : <gpio-pin number> <user-id> <loop>")

else:
    node()
