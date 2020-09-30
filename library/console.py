import subprocess
import inspect


class Console:
    """
    Console class
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

    def __init__(self, socket_io, priority, logger):
        """
        Init of console class
        :param socket_io: declare of socket_io
        :param priority: priority of logger
        :param logger: Logger class
        """

        assert isinstance(priority, int), "console priority should be int"

        self.__logger = logger
        self.__priority = priority
        self.__socket_io = socket_io

        try:
            subprocess.run(["clear"])
        except Exception:
            try:
                subprocess.run(["cls"])
            except Exception:
                pass

        # self.print(data="{bd}+-------------------------+{end}".format(bd=self.FG_COLORS["cyan"] + self.SPECIAL["bold"], fg=self.FG_COLORS["white"], end=self.END), priority=-1)
        # self.print(data="{bd}|                         {bd}|{end}".format(bd=self.FG_COLORS["cyan"] + self.SPECIAL["bold"], fg=self.FG_COLORS["white"], end=self.END), priority=-1)
        # self.print(data="{bd}|     {fg}Smart home 11.4     {bd}|{end}".format(bd=self.FG_COLORS["cyan"] + self.SPECIAL["bold"], fg=self.FG_COLORS["white"], end=self.END), priority=-1)
        # self.print(data="{bd}|    {fg}Fryčák, Szkandera    {bd}|{end}".format(bd=self.FG_COLORS["cyan"] + self.SPECIAL["bold"], fg=self.FG_COLORS["white"], end=self.END), priority=-1)
        # self.print(data="{bd}|                         {bd}|{end}".format(bd=self.FG_COLORS["cyan"] + self.SPECIAL["bold"], fg=self.FG_COLORS["white"], end=self.END), priority=-1)
        # self.print(data="{bd}|      {fg}© 2019 - 2020      {bd}|{end}".format(bd=self.FG_COLORS["cyan"] + self.SPECIAL["bold"], fg=self.FG_COLORS["white"], end=self.END), priority=-1)
        # self.print(data="{bd}|                         {bd}|{end}".format(bd=self.FG_COLORS["cyan"] + self.SPECIAL["bold"], fg=self.FG_COLORS["white"], end=self.END), priority=-1)
        # self.print(data="{bd}+-------------------------+{end}".format(bd=self.FG_COLORS["cyan"] + self.SPECIAL["bold"], fg=self.FG_COLORS["white"], end=self.END), priority=-1)
        # print()
        self.print(data="{}   _____                      _     _                          \n".format(self.FG_COLORS["cyan"] + self.SPECIAL["bold"]) +
                        "  / ____|                    | |   | |                         \n" +
                        " | (___  _ __ ___   __ _ _ __| |_  | |__   ___  _ __ ___   ___ \n" +
                        "  \\___ \\| '_ ` _ \\ / _` | '__| __| | '_ \\ / _ \\| '_ ` _ \\ / _ \\\n" +
                        "  ____) | | | | | | (_| | |  | |_  | | | | (_) | | | | | |  __/\n" +
                        " |_____/|_| |_| |_|\\__,_|_|   \\__| |_| |_|\\___/|_| |_| |_|\\___|\n{}".format(self.END), priority=-1)

    def print(self, data=None, priority=0):
        """
        Print to console
        :param data: data to print
        :param priority: priority of print
        :return:
        """

        data = str(data)

        # Get source of message
        cur_frame = inspect.currentframe()
        cal_frame = inspect.getouterframes(cur_frame, 2)
        source = cal_frame[1][1].split("/")
        source = source[len(source) - 1]

        if priority == -1 and self.__priority == 0:
            self.__logger.debug(data)
            print(data + self.END)

        elif priority == 0 and self.__priority == 0:
            self.__logger.debug(data)
            print(self.FG_COLORS["cyan"] + self.SPECIAL["bold"] + "Debug:\t" + self.END + self.FG_COLORS["white"] + data + self.END)

        elif priority == 0.1 and self.__priority == 0:
            self.__logger.debug(data)
            print(self.FG_COLORS["blue"] + self.SPECIAL["bold"] + "MQTT:\t" + self.END + self.FG_COLORS["white"] + data + self.END)

        elif priority == 0.2:
            if "arg" in data.lower():
                data = "(A) " + data

            elif "method" in data.lower():
                data = "(M) " + data

            if " not " in data.lower() and self.__priority <= 2:
                self.__logger.debug(data)
                print(self.BG_COLORS["red"] + self.SPECIAL["bold"] + "PHack:\t" + self.END + self.FG_COLORS["white"] + data + self.END)

            # elif self.__priority == 0:
            #     self.__logger.debug(data)
            #     print(self.FG_COLORS["green"] + self.SPECIAL["bold"] + "PHack:\t" + self.END + self.FG_COLORS["white"] + data + self.END)

        elif priority == 0.3 and self.__priority == 0:
            self.__logger.debug(data)
            print(self.FG_COLORS["purple"] + self.SPECIAL["bold"] + "Client:\t" + self.END + self.FG_COLORS["white"] + data + self.END)

        elif priority == 1 and self.__priority <= 1:
            self.__logger.warning(data)
            self.__socket_io.emit("notify", {"title": "WARNING", "message": data, "type": "warning"}, namespace="/com")

            print("{bg}{white}{bold}WARNING{end}\t{data} ({white}{bold}{source}:{line}{end})".format(
                bg=self.BG_COLORS["yellow"], white=self.FG_COLORS["white"], bold=self.SPECIAL["bold"], end=self.END,
                source=str(source), line=str(cal_frame[1][2]), data=data))

        elif priority == 2 and self.__priority <= 2:
            self.__logger.error(data)
            self.__socket_io.emit("notify", {"title": "ERROR", "message": data, "type": "danger"}, namespace="/com")
            print("{bg}{white}{bold}ERROR{end}\t{data} ({white}{bold}{source}:{line}{end})".format(
                bg=self.BG_COLORS["red"], white=self.FG_COLORS["white"], bold=self.SPECIAL["bold"], end=self.END,
                source=str(source), line=str(cal_frame[1][2]), data=data))
