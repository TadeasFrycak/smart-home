import serial
import time

class Arduino:
    def __init__(self):
        try:
            self.arduino = serial.Serial("COM14", 9600, timeout=0.1)

        except:
            self.arduino = None

    def write(self, data):
        if self.arduino:
            self.arduino.write(bytes(data,encoding='utf8'))
