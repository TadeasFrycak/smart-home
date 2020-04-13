import logging


class WerkzeugLogger:
    """
    WerkzeugLogger class
    """

    PRIORITY = [logging.DEBUG, logging.WARNING, logging.ERROR]

    def __init__(self, priority):
        """
        Init of WerkzeugLogger class
        """

        self.__priority = self.PRIORITY[priority]

        self.__log = logging.getLogger("werkzeug")
        self.__log.setLevel(self.__priority)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

        fh = logging.FileHandler("logs/werkzeug.log")
        fh.setLevel(self.__priority)
        fh.setFormatter(formatter)
        self.__log.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(self.__priority)
        ch.setFormatter(formatter)
        self.__log.addHandler(ch)


class AuthLogger:
    """
    AuthLogger class
    """

    PRIORITY = [logging.DEBUG, logging.WARNING, logging.ERROR]

    def __init__(self, priority):
        """
        Init of AuthLogger class
        """

        self.__priority = self.PRIORITY[priority]

        self.__log = logging.getLogger("auth")
        self.__log.setLevel(self.__priority)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

        fh = logging.FileHandler("logs/auth.log")
        fh.setLevel(self.__priority)
        fh.setFormatter(formatter)
        self.__log.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(self.__priority)
        ch.setFormatter(formatter)
        self.__log.addHandler(ch)

    def debug(self, message):
        """
        Log debug message
        :param message: message to print
        :return:
        """

        self.__log.debug(message)

    def warning(self, message):
        """
        Log warning message
        :param message: message to print
        :return:
        """

        self.__log.warning(message)

    def error(self, message):
        """
        Log error message
        :param message: message to print
        :return:
        """

        self.__log.error(message)


class ConsoleLogger:
    """
    ConsoleLogger class
    """

    PRIORITY = [logging.DEBUG, logging.WARNING, logging.ERROR]

    def __init__(self, priority):
        """
        Init of ConsoleLogger class
        """

        self.__priority = self.PRIORITY[priority]

        self.__log = logging.getLogger("console")
        self.__log.setLevel(self.__priority)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

        fh = logging.FileHandler("logs/console.log")
        fh.setLevel(self.__priority)
        fh.setFormatter(formatter)
        self.__log.addHandler(fh)

    def debug(self, message):
        """
        Log debug message
        :param message: message to print
        :return:
        """

        self.__log.debug(message)

    def warning(self, message):
        """
        Log warning message
        :param message: message to print
        :return:
        """

        self.__log.warning(message)

    def error(self, message):
        """
        Log error message
        :param message: message to print
        :return:
        """

        self.__log.error(message)
