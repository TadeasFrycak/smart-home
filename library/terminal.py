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

    def __init__(self, logger, log_only=False, priority=0, socket_io=None, log_lines=True):
        """
        Init of terminal class
        :param socket_io: declare of socket_io
        :param priority: priority of logger
        :param logger: Logger class
        """

        assert isinstance(priority, int), "terminal priority should be int"

        self.__logger = logger
        self.__log_only = log_only
        self.__priority = priority
        self.__socket_io = socket_io
        self.__log_lines = log_lines

        if log_only is False:
            try:
                subprocess.run(["cls"])
            except FileNotFoundError:
                subprocess.run(["clear"])

            print()
            subprocess.call(["catimg", "-w", "80", "./static/img/static/favicon_python.png"])

            self.go_back(100)

            print()

            self.print(
                "\t\t\t\t\t  _____ _    _         \n" +
                "\t\t\t\t\t / ____| |  | |  Smart \n" +
                "\t\t\t\t\t| (___ | |__| |  Home  \n" +
                "\t\t\t\t\t \\___ \\|  __  |      \n" +
                "\t\t\t\t\t ____) | |  | |        \n" +
                "\t\t\t\t\t|_____/|_|  |_|        \n")

            self.print(self.FG_COLORS["black"] + self.BG_COLORS["white"] + self.SPECIAL[
                "bold"] + "\t\t\t\t\t ↓ About ↓ " + self.END)
            #self.print(self.FG_COLORS["white"] + self.SPECIAL[
            #    "bold"] + "\t\t\t\t\tAuthors\t" + self.END + "Fryčák, Szkandera")
            self.print(self.FG_COLORS["white"] + self.SPECIAL[
                "bold"] + "\t\t\t\t\tVersion\t" + self.END + os.path.basename(os.getcwd()))
            self.print(self.FG_COLORS["white"] + self.SPECIAL[
                "bold"] + "\t\t\t\t\tCreated\t" + self.END + "26.05.2019 17:29")
            self.go_forward(12)

    @staticmethod
    def go_forward(amount):
        for i in range(amount):
            print()

    def go_back(self, amount):
        for i in range(amount):
            self.print("\033[A", end="")

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

            cur_frame = inspect.currentframe()
            cal_frame = inspect.getouterframes(cur_frame, 2)
            source = cal_frame[1][1]
            source = os.path.basename(source)

            self.print(self.BG_COLORS["red"] + self.SPECIAL["bold"] + "PHack\t" + self.END + self.FG_COLORS[
                "white"] + data + self.SPECIAL["bold"] + " (" + source + ":" + str(cal_frame[1][2]) + ")" + self.END)

        # elif self.__priority == 0:
        #     self.__logger.debug(data)
        #     self.print(self.FG_COLORS["green"] + self.SPECIAL["bold"] + "PHack:\t" + self.END + self.FG_COLORS["white"] + data)

    def protocol(self, name, data):
        if self.__priority == 0:
            self.__logger.debug(data)
            self.print(self.FG_COLORS["blue"] + self.SPECIAL["bold"] + name + "\t" + self.END + self.FG_COLORS[
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
                self.print("{bg}{white}{bold}WARNING{end}\t{data} {white}{bold}({source}:{line}){end}".format(
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
                self.print("{bg}{white}{bold}ERROR{end}\t{data} {white}{bold}({source}:{line}){end}".format(
                    bg=self.BG_COLORS["red"], white=self.FG_COLORS["white"], bold=self.SPECIAL["bold"], end=self.END,
                    source=str(source), line=str(cal_frame[1][2]), data=data))
            else:
                self.print("{bg}{white}{bold}ERROR{end}\t{data}{end}".format(
                    bg=self.BG_COLORS["red"], white=self.FG_COLORS["white"], bold=self.SPECIAL["bold"], end=self.END,
                    data=data))

    def print(self, data=None, end="\n"):
        """
        Print to terminal
        :param end: end of print
        :param data: data to print
        :return:
        """

        if self.__log_only is False:
            data = str(data)

            if self.__priority == 0:
                print(data + self.END, end=end)
