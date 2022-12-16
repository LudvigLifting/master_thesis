import serial
import serial.tools.list_ports as port_list
import time

def ver_windows():

    i = 0
    responses = ['+JOIN: Joined already', '+JOIN: Done', 'WPOWER: WAKEUP', '+MSGHEX: Done', '+LOWPOWER: WAKEUP', '♥GHEX: Done', 'GHEX: Done']
    full_name_port = list(port_list.comports())
    port = [str(l) for l in full_name_port if str(l) == 'COM4 - Silicon Labs CP210x USB to UART Bridge (COM4)']
    if(not port):
        exit()
    ser = serial.Serial(port[0][:4], 9600, timeout = 5)
    res = []

    ser.write(str.encode("AT+JOIN\n"))
    response =  ser.readline().decode('UTF-8').rstrip()
    print (response)
    while response not in responses:
        response =  ser.readline().decode('UTF-8').rstrip()
        print(response)

    time.sleep(1)

    #for i in range(10):
    while i < 10:
        ser.write(str.encode("AT+LOWPOWER=5000\n"))
        response =  ser.readline().decode('UTF-8').rstrip()
        print (response)
        while response not in responses:
            time.sleep(1)
            response =  ser.readline().decode('UTF-8').rstrip()
            print(response)

        #msg = f"AT+MSGHEX={1<<(8*i)}\n"
        msg = "AT+MSGHEX=123456789012345678901234567890\n"
        ser.write(str.encode(msg))
        response =  ser.readline().decode('UTF-8').rstrip()
        print (response)
        while response not in responses:
            time.sleep(1)
            if response[:10] == "+AT: ERROR":
                break
            #response = ser.read(50).decode('UTF-8').rstrip()
            response =  ser.readline().decode('UTF-8').rstrip()
            print(response)

        i += 1
    
    ser.write(str.encode("AT+LOWPOWER=1000\n"))
    response =  ser.readline().decode('UTF-8').rstrip()
    print (response)
    while response not in responses:
        time.sleep(2)
        response =  ser.readline().decode('UTF-8').rstrip()
        print(response)

    ser.close()
    
def main():
    ver_windows()

if __name__ == '__main__':
    main()