# from html_to_json import HTML_JSON
import serial
print(serial)
# from serial import serial
import time
import re

# html_json = HTML_JSON()

# <i>R</i><a>1</a>$
# <i>W</i><a>1</a><v>100</v>$
#
#

top = 10 + 1

line = ""


def sendHeader(adress):
    command = "<i>W</i><a>" + str(adress) + "</a>$"
    ser.write(command.encode("ascii"))
    # line = ser.read()
    line = "AA"
    return line


def programData(adress, data):
    command = "<i>W</i><a>" + str(adress) + "</a><v>" + str(data) + "</v>$"
    ser.write(command.encode("ascii"))
    line = ser.readline()
    return line


def readData(adress):
    command = "<i>R</i><a>" + str(adress) + "</a>$"
    ser.write(command.encode("ascii"))
    line = ser.readline()
    return line


def erase():
    command = "<i>E</i>$"
    ser.write(command.encode("ascii"))
    line = ser.readline()
    return line


def process(buffer_in):
    buf = buffer_in.split('$')
    # start_index = buf.index(">")
    # buf = buffer_in

    # buf = buf[buf.find(">")+1,buf.find("x")]
    start_index = buf.index(">") + 1
    offset = start_index
    end_index = buf.index("x")
    items = end_index - start_index

    errors = 0

    for x in range(items):
        current_value = int(buf[x + offset])
        actual_value = int(file[x], 16)

        if (current_value == actual_value):
            print("M", x, current_value, file[x])
            pass

        if (current_value != actual_value):
            print("E", x, "Expected:", actual_value, "Got:", current_value)
            errors += 1

    # print(buf[start_index],end_index)
    # errors = 0
    # # buf[0] = buf[0].replace("F\r\n","")
    # buf.remove("x")
    # for l in range(len(buf)):
    #     separate = buf[l].split(":")
    #     adress = separate[0]
    #     value = int(separate[1])
    #     actual_value = int(file[l],16)
    #     if actual_value == value:
    #         print("M",adress,value,file[l])
    #         pass

    #     if actual_value != value:
    #         print("E",adress,value,actual_value)
    #         errors += 1

    print("Done.", errors, "errors.")


ser = serial.Serial('/dev/cu.wchusbserialfd120', baudrate=115200)  # open serial port
time.sleep(2)

file = open("MOJE CESTA K TAJNYMU PEOJWKTU ;)))) ", "r").read().split()
file.remove("v2.0")
file.remove("raw")
top = len(file)
i = 0

do_erase = False
read_ver = False

if do_erase:
    time.sleep(1)
    erase()
    time.sleep(1)
    print("Erased")

if read_ver:
    print(sendHeader(top))
    time.sleep(1)
    print("Start. ", top, "bytes expected")
    for item in file:
        ser.write((str(int(item, 16)) + "$").encode("ascii"))
        i += 1
        # print(i,item)
        if i >= top:
            time.sleep(0.05)
            ser.write("300$".encode("ascii"))
            print("End of writing.")
            break
        elif (i % 100) == 0:
            print(i)
        time.sleep(0.0009)
        # time.sleep(1)

time.sleep(0.5)

if not read_ver:
    buffer = ""
    current_line = 0
    ser.write(("<i>R</i><a>" + str(top) + "</a>$").encode("ascii"))
    while True:
        k = ser.read()
        buffer = buffer + str(k.decode("ascii"))

        current_line += 1
        if (current_line % 1000) == 0:
            print(current_line)
        if k == 'x'.encode("ascii"):
            break

    process(buffer)
    # print(buffer)

# print(html_json.to_json(readData(0).decode("utf-8")))
ser.close()