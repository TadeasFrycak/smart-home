from logging.handlers import TimedRotatingFileHandler
import logging
import os

# TODO do configu (location dir) možná?
LOG_DIR = "logs/"
PRIORITY = [logging.DEBUG, logging.WARNING, logging.ERROR]

# TODO RAMLogger class - každý logger (authlogger, changeslogger, ...) bude mít odkaz na RAMLOGGER, který bude
#      log ukládat pouze na RAM a po určitě době až do logu (samozřejmě podle priority - error, warning, remove, atd.
#      musí logovat hned, ale debugy logovat až po určité době nebo před ukončením serveru/vypnutí, aby se nezničila
#      karta na RPi hned


class AuthLogger:
    """
    AuthLogger class
    """

    def __init__(self, priority=0):
        """
        Init of AuthLogger class
        """

        assert isinstance(priority, int), "auth priority should be int"

        self.__priority = PRIORITY[priority]

        self.__log = logging.getLogger("auth")
        self.__log.setLevel(self.__priority)

        formatter = logging.Formatter("%(asctime)s - %(type)s - %(user)s: %(message)s")
        
        os.makedirs(LOG_DIR, exist_ok=True)
        
        fh = TimedRotatingFileHandler(LOG_DIR + "auth.log", when="midnight", backupCount=365)
        fh.setLevel(self.__priority)
        fh.setFormatter(formatter)
        self.__log.addHandler(fh)

    def login(self, username, message):
        """
        Log debug message
        :param message: message to print
        :param username: user
        :return:
        """

        self.__log.debug(str(message).strip(), extra={"user": username, "type": "login"})

    def logout(self, username, message):
        self.__log.debug(str(message).strip(), extra={"user": username, "type": "logout"})

    def wrong_login(self, username, message):
        self.__log.warning(str(message).strip(), extra={"user": username, "type": "wrong login"})

    # def register(self, username, message):
    #     self.__log.warning(str(message).strip(), extra={"user": username, "type": "register"})


class ChangesLogger:
    """
    ChangesLogger class
    """

    def __init__(self, priority=0):
        """
        Init of AuthLogger class
        """
        assert isinstance(priority, int), "changes priority should be int"

        self.__priority = PRIORITY[priority]

        self.__log = logging.getLogger("changes")
        self.__log.setLevel(self.__priority)

        formatter = logging.Formatter("%(asctime)s - %(user)s - %(type)s - %(func)s: %(message)s")
        
        os.makedirs(LOG_DIR, exist_ok=True)

        fh = TimedRotatingFileHandler(LOG_DIR + "changes.log", when="midnight", backupCount=31)
        fh.setLevel(self.__priority)
        fh.setFormatter(formatter)
        self.__log.addHandler(fh)

    def change(self, username, func_name, message):
        self.__log.debug(str(message).strip(), extra={"user": username, "func": func_name, "type": "change"})

    def server(self, username, func_name, message):
        self.__log.warning(str(message).strip(), extra={"user": username, "func": func_name, "type": "server"})


class ChangesEditLogger:
    """
    ChangesEditLogger class
    """

    def __init__(self, priority=0):
        """
        Init of AuthLogger class
        """
        assert isinstance(priority, int), "changes priority should be int"

        self.__priority = PRIORITY[priority]

        self.__log = logging.getLogger("changes_edit")
        self.__log.setLevel(self.__priority)

        formatter = logging.Formatter("%(asctime)s - %(user)s - %(type)s - %(func)s: %(message)s")
        
        os.makedirs(LOG_DIR, exist_ok=True)

        fh = TimedRotatingFileHandler(LOG_DIR + "changes_edit.log", when="midnight", backupCount=365)
        fh.setLevel(self.__priority)
        fh.setFormatter(formatter)
        self.__log.addHandler(fh)

    def change(self, username, func_name, message):
        self.__log.debug(str(message).strip(), extra={"user": username, "func": func_name, "type": "change"})

    def add(self, username, func_name, message):
        self.__log.warning(str(message).strip(), extra={"user": username, "func": func_name, "type": "add"})

    def remove(self, username, func_name, message):
        self.__log.warning(str(message).strip(), extra={"user": username, "func": func_name, "type": "remove"})


class TerminalLogger:
    """
    TerminalLogger class
    """

    def __init__(self, priority=0):
        """
        Init of TerminalLogger class
        """

        assert isinstance(priority, int), "terminal priority should be int"
        self.__priority = PRIORITY[priority]

        self.__log = logging.getLogger("terminal")
        self.__log.setLevel(self.__priority)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        
        os.makedirs(LOG_DIR, exist_ok=True)
        
        fh = TimedRotatingFileHandler(LOG_DIR + "terminal.log", when="midnight", backupCount=31)
        fh.setLevel(self.__priority)
        fh.setFormatter(formatter)
        self.__log.addHandler(fh)

    def debug(self, message):
        """
        Log debug message
        :param message: message to print
        :return:
        """

        self.__log.debug(str(message).strip())

    def warning(self, message):
        """
        Log warning message
        :param message: message to print
        :return:
        """

        self.__log.warning(str(message).strip())

    def error(self, message):
        """
        Log error message
        :param message: message to print
        :return:
        """

        self.__log.error(str(message).strip())
