import serial
import time


class Arduino:
    """
    Arduino class
    """

    BAUDRATE = 9600
    TIMEOUT = 0.1
    END_CHAR = "$"

    WINDOWS_PORT = "COM3"
    MAC_PORT = "/dev/cu.usbmodemFD121"
    LINUX_PORT = "/dev/ttyACM0"
    LINUX_PORT2 = "/dev/ttyACM1"
    
    def __init__(self, console):
        self.__console = console

        try:
            self.arduino = serial.Serial(self.WINDOWS_PORT, self.BAUDRATE, timeout=self.TIMEOUT)

        except Exception as e:
            try:
                self.arduino = serial.Serial(self.MAC_PORT, self.BAUDRATE, timeout=self.TIMEOUT)

            except Exception as e2:
                try:
                    self.arduino = serial.Serial(self.LINUX_PORT, self.BAUDRATE, timeout=self.TIMEOUT)

                except Exception as e3:
                    try:
                        self.arduino = serial.Serial(self.LINUX_PORT2, self.BAUDRATE, timeout=self.TIMEOUT)

                    except Exception as e4:
                        self.arduino = None
                        self.__console.print("Error in opening port due: {0},{1},{2},{3}".format(e, e2, e3, e4),
                                             priority=2)

    def write(self, data):
        """
        Write data to Arduino
        :param data: data to write
        :return:
        """

        if self.arduino:
            data = data + self.END_CHAR
            return self.arduino.write(bytes(data, encoding="utf8"))

        else:
            # self.__console.print("Error in writing to Arduino - not defined", priority=3)
            return False

    def read(self):
        """
        Read data from Arduino
        :return: False/value
        """

        if self.arduino:
            data = self.arduino.readline()[:-2]

            if data:
                return str(data).split("'")[1]

            else:
                return None

        else:
            # self.__console.print("Error in writing to Arduino - not defined", priority=3)
            return None
