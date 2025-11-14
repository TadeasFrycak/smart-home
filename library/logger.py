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

class BaseLogger:
    def __init__(self, log_name, priority=0, when="midnight", backup_count=365):
        self.log_file = os.path.join(LOG_DIR, f"{log_name}.log")
        self.priority = PRIORITY[priority]
        self.log = logging.getLogger(log_name)
        self.log.setLevel(self.priority)
        
        os.makedirs(LOG_DIR, exist_ok=True)
        
        fh = TimedRotatingFileHandler(self.log_file, when=when, backupCount=backup_count)
        fh.setLevel(self.priority)
        self.log.addHandler(fh)

    def get_user_logs(self, username):
        user_logs = []
        if not os.path.exists(self.log_file):
            return []

        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    if "- " + username in line:
                        user_logs.append(line.strip())
        except Exception as e:
            print(f"Error reading log file {self.log_file}: {e}")
        
        return user_logs

class AuthLogger(BaseLogger):
    """
    AuthLogger class
    """

    def __init__(self, priority=0):
        """
        Init of AuthLogger class
        """
        super().__init__("auth", priority)
        formatter = logging.Formatter("%(asctime)s - %(type)s - %(user)s: %(message)s")
        self.log.handlers[0].setFormatter(formatter)


    def login(self, username, message):
        """
        Log debug message
        :param message: message to print
        :param username: user
        :return:
        """

        self.log.debug(str(message).strip(), extra={"user": username, "type": "login"})

    def logout(self, username, message):
        self.log.debug(str(message).strip(), extra={"user": username, "type": "logout"})

    def wrong_login(self, username, message):
        self.log.warning(str(message).strip(), extra={"user": username, "type": "wrong login"})

    # def register(self, username, message):
    #     self.__log.warning(str(message).strip(), extra={"user": username, "type": "register"})


class ChangesLogger(BaseLogger):
    """
    ChangesLogger class
    """

    def __init__(self, priority=0):
        """
        Init of AuthLogger class
        """
        super().__init__("changes", priority, backup_count=31)
        formatter = logging.Formatter("%(asctime)s - %(user)s - %(type)s - %(func)s: %(message)s")
        self.log.handlers[0].setFormatter(formatter)

    def change(self, username, func_name, message):
        self.log.debug(str(message).strip(), extra={"user": username, "func": func_name, "type": "change"})

    def server(self, username, func_name, message):
        self.log.warning(str(message).strip(), extra={"user": username, "func": func_name, "type": "server"})


class ChangesEditLogger(BaseLogger):
    """
    ChangesEditLogger class
    """

    def __init__(self, priority=0):
        """
        Init of AuthLogger class
        """
        super().__init__("changes_edit", priority)
        formatter = logging.Formatter("%(asctime)s - %(user)s - %(type)s - %(func)s: %(message)s")
        self.log.handlers[0].setFormatter(formatter)

    def change(self, username, func_name, message):
        self.log.debug(str(message).strip(), extra={"user": username, "func": func_name, "type": "change"})

    def add(self, username, func_name, message):
        self.log.warning(str(message).strip(), extra={"user": username, "func": func_name, "type": "add"})

    def remove(self, username, func_name, message):
        self.log.warning(str(message).strip(), extra={"user": username, "func": func_name, "type": "remove"})


class TerminalLogger(BaseLogger):
    """
    TerminalLogger class
    """

    def __init__(self, priority=0):
        """
        Init of TerminalLogger class
        """
        super().__init__("terminal", priority, backup_count=31)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        self.log.handlers[0].setFormatter(formatter)

    def debug(self, message):
        """
        Log debug message
        :param message: message to print
        :return:
        """

        self.log.debug(str(message).strip())

    def warning(self, message):
        """
        Log warning message
        :param message: message to print
        :return:
        """

        self.log.warning(str(message).strip())

    def error(self, message):
        """
        Log error message
        :param message: message to print
        :return:
        """

        self.log.error(str(message).strip())