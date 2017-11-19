import time
import datetime
import RPi.GPIO as GPIO
import bluetooth

# noinspection PyUnresolvedReferences
from logentries import LogentriesHandler
import logging

USER_ID = "shivam"
GPIO_user = 4
bd_addr = "B8:27:EB:A9:C1:02"

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)


def bin2dec(string_num):
    return str(int(string_num, 2))


# function testing the room temperature according to which table will be created for alerts
def generate_val(dt, a, b):
    # sending data to the bluetooth device
    sock.send('{}-{}-{} {}:{}:{}.{} User ID: {} temperature = {} humidity = {} \n'.format(dt.year, dt.month, dt.day,
                                                                                          dt.hour, dt.minute, dt.second,
                                                                                          dt.microsecond, USER_ID, b,
                                                                                          a))


def temp():
    values = []
    data = []

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(GPIO_user, GPIO.OUT)
    GPIO.output(GPIO_user, GPIO.HIGH)
    time.sleep(0.025)
    GPIO.output(GPIO_user, GPIO.LOW)
    time.sleep(0.02)

    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for i in range(0, 3500):
        data.append(GPIO.input(4))

    bit_count = 0
    tmp = 0
    count = 0
    HumidityBit = ""
    TemperatureBit = ""
    HumidityDecimalBit = ""
    TemperatureDecimalBit = ""
    crc = ""

    try:
        while data[count] == 1:
            tmp = 1
            count = count + 1

        for i in range(0, 32):
            bit_count = 0

            while data[count] == 0:
                tmp = 1
                count = count + 1

            while data[count] == 1:
                bit_count = bit_count + 1
                count = count + 1

            if bit_count > 16:
                # Humidity bit
                if 0 <= i < 8:
                    HumidityBit = HumidityBit + "1"
                # Humidity decimal
                if 8 <= i < 16:
                    HumidityDecimalBit = HumidityDecimalBit + "1"
                # Temperature
                if 16 <= i < 24:
                    TemperatureBit = TemperatureBit + "1"
                # Temperature decimal
                if 24 <= i < 32:
                    TemperatureDecimalBit = TemperatureDecimalBit + "1"

            else:
                # Humidity bit
                if 0 <= i < 8:
                    HumidityBit = HumidityBit + "0"
                # Humidity decimal
                if 8 <= i < 16:
                    HumidityDecimalBit = HumidityDecimalBit + "0"
                # Temperature
                if 16 <= i < 24:
                    TemperatureBit = TemperatureBit + "0"
                # Temperature decimal
                if 24 <= i < 32:
                    TemperatureDecimalBit = TemperatureDecimalBit + "0"
    except:
        print("ERR_RANGE")
        return temp()

    try:
        for i in range(0, 8):
            bit_count = 0

            while data[count] == 0:
                tmp = 1
                count = count + 1

            while data[count] == 1:
                bit_count = bit_count + 1
                count = count + 1

            if bit_count > 16:
                crc = crc + "1"
            else:
                crc = crc + "0"
    except:
        print("ERR_RANGE")
        return temp()

    # Display
    humidity = bin2dec(HumidityBit)
    humidityDecimal = bin2dec(HumidityDecimalBit)
    temperatureDecimal = bin2dec(TemperatureDecimalBit)
    temperature = bin2dec(TemperatureBit)

    # Putting both the outputs in a list
    values.append(humidity)
    values.append(temperature)
    values.append(humidityDecimal)
    values.append(temperatureDecimal)

    # Returning the list
    return values


''' not required at the moment  '''
# logentries token
#log.addHandler(LogentriesHandler('8b6afd9f-4f3f-4650-bcaa-2aab406306d3'))

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

    mylist = temp()

    hum1 = float(mylist[0])
    temp1 = float(mylist[1])

    c = float(mylist[2]) / 10
    d = float(mylist[3]) / 10

    # adding the decimal bits
    hum = hum1 + c
    temp = temp1 + d

    # To Define Alerts
    generate_val(dt, hum, temp)

    # to iterate the loop
    i = i + 1

    # waiting 5 seconds before taking the input
    time.sleep(5)

# closing the connection
sock.close()
