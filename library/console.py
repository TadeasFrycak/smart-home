import inspect


class Console:
    NEWLINE = ""
    SEPARATOR = "------------------------------------------------------------"
    SEPARATOR_START = "/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ "
    WARNING = "-->>------------------->> WARNING <<-------------------<<--"
    ERROR = "-->>-------------------->> ERROR <<--------------------<<--"

    FG_COLORS = {
        "light_red": "\033[91m",
        "red": "\033[31m",
        "fail": "\033[91m",
        "orange": "\033[33m",
        "yellow": "\033[93m",
        "pink": "\033[95m",
        "purple": "\033[35m",
        "light_blue": "\033[94m",
        "blue": "\033[34m",
        "light_cyan": "\033[96m",
        "cyan": "\033[36m",
        "light_green": "\033[92m",
        "green": "\033[32m",
        "light_grey": "\033[37m",
        "dark_grey": "\033[90m",
        "black": "\033[30m"
        }

    BG_COLORS = {
        "orange": "\033[43m",
        "red": "\033[41m",
        "purple": "\033[45m",
        "blue": "\033[44m",
        "cyan": "\033[46m",
        "green": "\033[42m",
        "light_grey": "\033[47m",
        "black": "\033[40m",
    }

    SPECIAL = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "disable": "\033[02m",
        "underline": "\033[04m",
        "reverse": "\033[07m",
        "strikethrsough": "\033[09m",
        "invisible": "\033[08m"
    }

    END = "\033[0m"

    def __init__(self, socket_io=None, priority_level=1):
        self.__priority_level = priority_level
        self.__socket_io = socket_io

    def print(self, data=None, priority=1):
        cur_frame = inspect.currentframe()
        cal_frame = inspect.getouterframes(cur_frame, 2)
        source = cal_frame[1][1].split("/")
        source = source[len(source) - 1]

        if priority is None:
            print(data)

        elif priority == 1 and self.__priority_level <= 1:
            print(self.FG_COLORS["light_cyan"] + self.SPECIAL["bold"] + "Debug: " + self.END + self.SPECIAL["bold"] + str(data) + self.END)

        elif priority == 2 and self.__priority_level <= 2:
            self.__socket_io.emit("notify", {"title": "WARNING", "message": data, "type": "warning"}, namespace="/acom")
            print(self.FG_COLORS["yellow"] + self.SPECIAL["bold"] + self.WARNING + self.END)
            print("{0}{1}{2} - ln {3}:\t{4}{5}{6}{7}".format(self.FG_COLORS["yellow"], self.SPECIAL["bold"],
                                                             str(source), str(cal_frame[1][2]), self.END,
                                                             self.SPECIAL["bold"], str(data), self.END))
            print(self.FG_COLORS["yellow"] + self.SPECIAL["bold"] + self.WARNING + self.END)

        elif priority == 3 and self.__priority_level <= 3:
            self.__socket_io.emit("notify", {"title": "ERROR", "message": data, "type": "danger"}, namespace="/acom")
            print(self.FG_COLORS["fail"] + self.SPECIAL["bold"] + self.ERROR + self.END)
            print("{0}{1}{2} - ln {3}:\t{4}{5}{6}{7}".format(self.FG_COLORS["fail"], self.SPECIAL["bold"], str(source), str(cal_frame[1][2]), self.END, self.SPECIAL["bold"], str(data), self.END))
            print(self.FG_COLORS["fail"] + self.SPECIAL["bold"] + self.ERROR + self.END)
