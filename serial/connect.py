import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyUSB0'
ser.timeout = 5
#ser = serial.Serial('/Device/Silabser0', 9600, timeout=5)
ser.write("AT\r")
response =  ser.readline()
ser.close()

print (response)