import RPi.GPIO as GPIO
import time

# The GPIO pin
#GPIO_user = 4


def bin2dec(string_num):
    return str(int(string_num, 2))


def temp(GPIO_user):
    data = []
    value = []

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(GPIO_user, GPIO.OUT)
    GPIO.output(GPIO_user, GPIO.HIGH)
    time.sleep(0.025)
    GPIO.output(GPIO_user, GPIO.LOW)
    time.sleep(0.02)

    GPIO.setup(GPIO_user, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        return temp(GPIO_user)

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
        return temp(GPIO_user)

    # Display
    humidity = bin2dec(HumidityBit)
    humidityDecimal = bin2dec(HumidityDecimalBit)
    temperatureDecimal = bin2dec(TemperatureDecimalBit)
    temperature = bin2dec(TemperatureBit)

    # adding all the items to list
    value.append(humidity)
    value.append(humidityDecimal)
    value.append(temperature)
    value.append(temperatureDecimal)

    # Returning the list
    return value
