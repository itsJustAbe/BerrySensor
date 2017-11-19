import bluetooth
import sensor
import SensorScript
import datetime

GPIO_PIN = 4
USER_ID = "Shivam"


dt = datetime.datetime.now()

# mac address of windows 10
bd_addr = "B8:27:EB:A9:C1:02"

# assembling data received from the sensor
data = SensorScript.assembler(dt,sensor.temp(4),USER_ID)

port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

sock.send(data)

sock.close()
