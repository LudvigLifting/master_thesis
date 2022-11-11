import serial
import serial.tools.list_ports as port_list


# ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
full_name_port = list(port_list.comports())
port = [str(l) for l in full_name_port if str(l) == 'COM4 - Silicon Labs CP210x USB to UART Bridge (COM4)']
if(not port):
    exit()
ser = serial.Serial(port[0][:4], 9600, timeout=5) # For use when running on windows
ser.write(str.encode("AT\r"))
response =  ser.read(5)
print (response.decode('UTF-8'))
ser.close()

