# client script

import RPi.GPIO as GPIO
import time
import os

gpio = 4
user_id = os.uname()[1]


def bin2dec(string_num):
    return str(int(string_num, 2))


def temp():
    data = []
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.HIGH)
    time.sleep(0.025)
    GPIO.output(gpio, GPIO.LOW)
    time.sleep(0.02)
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        #print("ERR_RANGE")
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
        #print("ERR_RANGE")
        return temp()

    # Display
    humidity = float(bin2dec(HumidityBit))
    humidity_decimal = float(bin2dec(HumidityDecimalBit)) / 10
    temperature_decimal = float(bin2dec(TemperatureDecimalBit)) / 10
    temperature = float(bin2dec(TemperatureBit))

    # adding the decimal bits
    humidity = humidity + humidity_decimal
    temperature = temperature + temperature_decimal

    # Returning the values parsed from the sensor
    return humidity, temperature, user_id
