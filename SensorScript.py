import time
import datetime
import bluetooth
import sensor

USER_ID = "shivam"
GPIO_user = 4
bd_addr = "B8:27:EB:A9:C1:02"



def send_to_bt(dt, a, b):
    # sending data to the bluetooth device
    sock.send('{}-{}-{} {}:{}:{}.{} User ID: {} temperature = {} humidity = {} \n'.format(dt.year, dt.month, dt.day,
                                                                                          dt.hour, dt.minute, dt.second,
                                                                                          dt.microsecond, USER_ID, b, a);

# Bluetooth connection
port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

sock.connect((bd_addr, port))

# running the program to transfer output to a file
output = []
i = 0

# running the loop 40 times to capture 15 outputs
while i < 40:
    dt = datetime.datetime.now()

    hum, temp, humD, tempD = sensor.temp(GPIO_user)

    # converting them to float
    humidity = (float)hum
    temperature = (float)temp
    humidity_decimal = (float)humD
    temperature_decimal = (float)tempD

    # adding the decimal bits
    humidity = humidity + humidity_decimal
    temperature = temperature + temperature_decimal

    # To Define Alerts
    send_to_bt(dt, humidity, temperature)

    # to iterate the loop
    i = i + 1

    # waiting 5 seconds before taking the input
    time.sleep(5)

# closing the connection
#sock.close()
