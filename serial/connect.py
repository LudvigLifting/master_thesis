import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
ser.write("AT\r")
response =  ser.readline()
ser.close()

print (response)