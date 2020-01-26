import logging


class WerkzeugLogger:
    """
    WerkzeugLogger class
    """

    def __init__(self):
        """
        Init of WerkzeugLogger class
        """
        priority = logging.WARNING

        self.__log = logging.getLogger("werkzeug")
        self.__log.setLevel(priority)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

        # fh = logging.FileHandler("logs/console.log")
        # fh.setLevel(priority)
        # fh.setFormatter(formatter)
        # self.__log.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(priority)
        ch.setFormatter(formatter)
        self.__log.addHandler(ch)


class AuthLogger:
    """
    AuthLogger class
    """

    def __init__(self):
        """
        Init of AuthLogger class
        """

        priority = logging.DEBUG

        self.__log = logging.getLogger("auth")
        self.__log.setLevel(priority)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

        fh = logging.FileHandler("logs/auth.log")
        fh.setLevel(priority)
        fh.setFormatter(formatter)
        self.__log.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(priority)
        ch.setFormatter(formatter)
        self.__log.addHandler(ch)

    def warning(self, message):
        """
        Log warning message
        :param message: message to print
        :return:
        """

        self.__log.warning(message)


