import serial
import serial.tools.list_ports
import sys


PORT = ""
ports = list(serial.tools.list_ports.comports())
for port in ports:
    if "Arduino" in port.description:
        PORT = port.device

if not PORT:
    print("Can't find port")
    sys.exit()

SERIAL_PORT = serial.Serial(port=PORT, baudrate=115200, timeout=0.1)

SERVER_ROOT = {"start": "<server>", "end": "</server>"}


def get_serial_data(start, end, prev_data):
    serial_data = SERIAL_PORT.readline().decode("UTF-8").strip()
    if prev_data == "":
        data_list = []
        status = False
        while True:
            serial_data = SERIAL_PORT.readline().decode("UTF-8")
            if start in serial_data:
                data_list.append(serial_data)
                status = True

            if status == True and end in serial_data:
                data_list.append(serial_data)
                data_str = "".join(data_list)
                return data_str[data_str.index(start) : data_str.index(end) + len(end)]

            if status == True:
                data_list.append(serial_data)
    elif serial_data == "":
        return prev_data
    else:
        return serial_data


def send_serial_data(data):
    SERIAL_PORT.write(data.encode("UTF-8"))
