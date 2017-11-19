import bluetooth
import sensor
import SensorScript
import datetime
import sys
import time


def node():
    # Gpio pin where the sensor is attached
    GPIO_PIN = sys.argv[1]

    USER_ID = sys.argv[2]

    # number of times the loop will run
    Loop = int(sys.argv[3])

    # mac address of windows 10
    bd_addr = "B8:27:EB:A9:C1:02"

    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    # iterator
    i = 0

    while i < Loop:

        # date and time object to log current time
        date_time_object = datetime.datetime.now()

        # assembling data received from the sensor
        data = SensorScript.assembler(date_time_object,
                                      sensor.temp(GPIO_PIN),
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
