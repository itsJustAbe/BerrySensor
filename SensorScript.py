
# assembler for all the script data
def assembler(dt, my_list,USER_ID):
    # converting them to float
    humidity = float(my_list[0])
    temperature = float(my_list[1])
    humidity_decimal = float(my_list[2])
    temperature_decimal = float(my_list[3])

    # adding the decimal bits
    humidity = humidity + humidity_decimal
    temperature = temperature + temperature_decimal

    # formatting data to be sent to the bluetooth device
    format_string = '{}-{}-{} {}:{}:{}.{} User ID: {} temperature = {} humidity = {} \n'.format(dt.year, dt.month,
                                                                                                dt.day,
                                                                                                dt.hour, dt.minute,
                                                                                                dt.second,
                                                                                                dt.microsecond, USER_ID,
                                                                                                humidity, temperature)

    return format_string
