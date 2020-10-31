import subprocess
import inspect
import os


class Terminal:
    """
    Terminal class
    """

    FG_COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m"
    }

    BG_COLORS = {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "purple": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m"
    }

    SPECIAL = {
        "bold": "\033[1m",
        "disable": "\033[02m",
        "underline": "\033[04m",
        "reverse": "\033[07m",
        "strikethrough": "\033[09m",
        "invisible": "\033[08m"
    }

    END = "\033[0m"

    def __init__(self, logger, priority=0, socket_io=None, log_lines=True):
        """
        Init of terminal class
        :param socket_io: declare of socket_io
        :param priority: priority of logger
        :param logger: Logger class
        """

        assert isinstance(priority, int), "terminal priority should be int"

        self.__logger = logger
        self.__priority = priority
        self.__socket_io = socket_io
        self.__log_lines = log_lines
        os.system("cls")
        try:
            subprocess.run(["clear"])
        except Exception:
            try:
                subprocess.run(["cls"])
            except Exception:
                pass
        self.print(data="{}   _____                      _     _                          \n".format(self.FG_COLORS["cyan"] + self.SPECIAL["bold"]) +
                        "  / ____|                    | |   | |                         \n" +
                        " | (___  _ __ ___   __ _ _ __| |_  | |__   ___  _ __ ___   ___ \n" +
                        "  \\___ \\| '_ ` _ \\ / _` | '__| __| | '_ \\ / _ \\| '_ ` _ \\ / _ \\\n" +
                        "  ____) | | | | | | (_| | |  | |_  | | | | (_) | | | | | |  __/\n" +
                        " |_____/|_| |_| |_|\\__,_|_|   \\__| |_| |_|\\___/|_| |_| |_|\\___|\n{}".format(self.END))

    # def question(self, question):
    #     quest = input(self.FG_COLORS["blue"] + self.SPECIAL["bold"] + "Q -> ?\t" + self.END + self.FG_COLORS["white"] + question + self.END).lower()
    #     if quest == "y" or quest == "":
    #         return True
    #
    #     elif quest == "n":
    #         return False
    #
    #     else:
    #         return self.question(question="Wrong input [Y/n] ")

    def status(self, data, value=True):
        if value:
            self.print(self.FG_COLORS["green"] + self.SPECIAL["bold"] + "Ok\t" + self.END + str(data))

        else:
            self.print(self.FG_COLORS["red"] + self.SPECIAL["bold"] + "Err\t" + self.END + str(data))

    def debug(self, data):
        if self.__priority == 0:
            self.__logger.debug(data)
            self.print(self.FG_COLORS["cyan"] + self.SPECIAL["bold"] + "Debug\t" + self.END + self.FG_COLORS[
                "white"] + data + self.END)

    def prevent_hack(self, data, status=True):
        if "arg" in data.lower():
            data = "(A) " + data

        elif "method" in data.lower():
            data = "(M) " + data

        if not status and self.__priority <= 2:
            self.__logger.debug(data)
            self.print(self.BG_COLORS["red"] + self.SPECIAL["bold"] + "PHack\t" + self.END + self.FG_COLORS[
                "white"] + data)

        elif self.__priority == 0:
            self.__logger.debug(data)
        #     self.print(self.FG_COLORS["green"] + self.SPECIAL["bold"] + "PHack:\t" + self.END + self.FG_COLORS["white"] + data)

    def mqtt(self, data):
        if self.__priority == 0:
            self.__logger.debug(data)
            self.print(self.FG_COLORS["blue"] + self.SPECIAL["bold"] + "MQTT\t" + self.END + self.FG_COLORS[
                "white"] + data)

    def client(self, data):
        if self.__priority == 0:
            self.__logger.debug(data)
            self.print(self.FG_COLORS["purple"] + self.SPECIAL["bold"] + "Client\t" + self.END + self.FG_COLORS[
                "white"] + data)

    def warning(self, data):
        if self.__priority <= 1:
            # Get source of message
            cur_frame = inspect.currentframe()
            cal_frame = inspect.getouterframes(cur_frame, 2)
            source = cal_frame[1][1]
            source = os.path.basename(source)

            self.__logger.warning(data)

            if self.__socket_io:
                self.__socket_io.emit("notify", {"title": "WARNING", "message": data, "type": "warning", "delay": 5000},
                                      namespace="/com")

            if self.__log_lines:
                # TODO WARN text do konstanty
                self.print("{bg}{white}{bold}WARNING{end}\t{data} ({white}{bold}{source}:{line}{end})".format(
                    bg=self.BG_COLORS["yellow"], white=self.FG_COLORS["white"], bold=self.SPECIAL["bold"], end=self.END,
                    source=str(source), line=str(cal_frame[1][2]), data=data))
            else:
                self.print("{bg}{white}{bold}WARNING{end}\t{data}{end}".format(
                    bg=self.BG_COLORS["yellow"], white=self.FG_COLORS["white"], bold=self.SPECIAL["bold"], end=self.END,
                    data=data))

    def error(self, data):
        if self.__priority <= 2:
            # Get source of message
            cur_frame = inspect.currentframe()
            cal_frame = inspect.getouterframes(cur_frame, 2)
            source = cal_frame[1][1]
            source = os.path.basename(source)

            self.__logger.error(data)

            if self.__socket_io:
                self.__socket_io.emit("notify", {"title": "ERROR", "message": data, "type": "danger", "delay": 5000},
                                      namespace="/com")

            if self.__log_lines:
                self.print("{bg}{white}{bold}ERROR{end}\t{data} ({white}{bold}{source}:{line}{end})".format(
                    bg=self.BG_COLORS["red"], white=self.FG_COLORS["white"], bold=self.SPECIAL["bold"], end=self.END,
                    source=str(source), line=str(cal_frame[1][2]), data=data))
            else:
                self.print("{bg}{white}{bold}ERROR{end}\t{data}{end}".format(
                    bg=self.BG_COLORS["red"], white=self.FG_COLORS["white"], bold=self.SPECIAL["bold"], end=self.END,
                    data=data))

    def print(self, data=None):
        """
        Print to terminal
        :param data: data to print
        :return:
        """

        data = str(data)

        if self.__priority == 0:
            print(data + self.END)
