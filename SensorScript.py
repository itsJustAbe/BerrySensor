import time
import datetime
import RPi.GPIO as GPIO


def bin2dec(string_num):
    return str(int(string_num, 2))


# function to transfer all the output to a text file with alerts
def output_to_file(dt, a, b):
    lHumidity = "humidity is low"
    hHumidity = "humidity is high"
    hTemperature = "temperature is high"
    lTemperature = "temperature is low"

    # normal case
    if 45 < a <= 53 and 20 < b <= 25:
        out.write('{}-{}-{} {}:{}:{}.{}  humidity = {} temperature = {}'.format(dt.year, dt.month, dt.day,
                                                                                dt.hour, dt.minute, dt.second,
                                                                                dt.microsecond, a, b))
    # High humidity
    elif a > 53:
        out.write('{}-{}-{} {}:{}:{}.{} {}'.format(dt.year, dt.month, dt.day,
                                                   dt.hour, dt.minute, dt.second,
                                                   dt.microsecond, hHumidity))
    # low humidity
    elif a <= 45:
        out.write('{}-{}-{} {}:{}:{}.{} {} '.format(dt.year, dt.month, dt.day,
                                                    dt.hour, dt.minute, dt.second,
                                                    dt.microsecond, lHumidity))
    # high temperature
    elif b > 25:
        out.write('{}-{}-{} {}:{}:{}.{} {}'.format(dt.year, dt.month, dt.day,
                                                   dt.hour, dt.minute, dt.second,
                                                   dt.microsecond, hTemperature))
    # low temperature
    elif b <= 20:
        out.write('{}-{}-{} {}:{}:{}.{} {}'.format(dt.year, dt.month, dt.day,
                                                   dt.hour, dt.minute, dt.second,
                                                   dt.microsecond, lTemperature))

    out.write("\n")


# function testing the room temperature according to which table will be created for alerts
def generate_val(dt, a, b):
    print ('{}-{}-{} {}:{}:{}.{}  humidity = {} temperature = {} \n'.format(dt.year, dt.month, dt.day,
                                                                            dt.hour, dt.minute, dt.second,
                                                                            dt.microsecond, a, b))


def temp():
    values = []
    data = []

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)
    time.sleep(0.025)
    GPIO.output(4, GPIO.LOW)
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


# creating a file
out = open("output.txt", "w")

# running the program to transfer output to a file
output = []
i = 0

# running the loop 40 times to capture 15 outputs
while i < 40:
    dt = datetime.datetime.now()

    mylist = temp()

    a = float(mylist[0])
    b = float(mylist[1])

    c = float(mylist[2]) / 10
    d = float(mylist[3]) / 10
    # adding the decimal bits
    a = a + c
    b = b + d
    print('humidity decimal  = ' + str(c) + '\ntemperature decimal = ' + str(d))

    # To Define Alerts
    generate_val(dt, a, b)
    # Output to the generates file
    output_to_file(dt, a, b)

    # to iterate the loop
    i = i + 1

    # waiting 5 seconds before taking the input
    time.sleep(5)

# closing the file
out.close()
