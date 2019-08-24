import serial
import time


class Arduino:
    """
    Arduino class
    """

    BAUDRATE = 9600
    TIMEOUT = 0.1
    END_CHAR = "-"
    WRITE_READ_DELAY = 0.5
    SEPARATOR = ";"

    WINDOWS_PORT = "COM14"
    MAC_PORT = "/dev/cu.wchusbserialfd120"
    LINUX_PORT = None
    
    def __init__(self, console_log):
        """
        Init of class Arduino
        :param console_log: Python console log
        """

        self.__console_log = console_log
        
        try:
            self.arduino = serial.Serial(self.WINDOWS_PORT, self.BAUDRATE, timeout=self.TIMEOUT)

        except Exception as e:
            self.__console_log.warning("Error in opening port due {0}".format(e))

            try:
                self.arduino = serial.Serial(self.MAC_PORT, self.BAUDRATE, timeout=self.TIMEOUT)

            except Exception as e2:
                self.arduino = None
                self.__console_log.warning("Error in opening port due {0}".format(e2))

    def write(self, data):
        """
        Write data to Arduino
        :param data: data to write
        :return:
        """

        if self.arduino:
            if isinstance(data, list):
                data = self.SEPARATOR.join(data)

            data = data + self.END_CHAR
            return self.arduino.write(bytes(data, encoding='utf8'))

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
                return False

        else:
            return False

    def write_read(self, data):
        """
        Write data and read response ==> synchronous communication
        :param data: data to write
        :return:
        """

        self.write(data=data)
        time.sleep(self.WRITE_READ_DELAY)

        return self.read()

    def check_data(self, data):
        if len(data.split(self.SEPARATOR)) > 2 or len(data.split(self.SEPARATOR)) < 2:
            self.__console_log.warning("Warning! Message from Arduino isn´t correct! "+data)
