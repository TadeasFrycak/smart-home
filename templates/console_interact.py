import os
import time
import sys
import colorama
colorama.init()


class PythonConsole:
    NEWLINE = ""
    SEPARATOR = "------------------------------------------------------------"
    SEPARATOR_START = "/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ "
    WARNING =   "-->>------------------->> WARNING <<-------------------<<--"
    ERROR =   "-->>-------------------->> ERROR <<--------------------<<--"

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
        "strikethrough": "\033[09m",
        "invisible": "\033[08m"
    }

    END = "\033[0m"
    
    def __init__(self):
        self.current_folder = os.getcwd()
        self.current_file = __file__
        self.current_version = self.current_folder.split("IoT")
        self.current_version = self.current_version[len(self.current_version)-1].strip()

    def introduction(self):
        self.print(self.SEPARATOR, color="blue")
        self.print(data="Smart Home - App", align="center", color="light_cyan")
        self.print(self.SEPARATOR, color="blue")
        self.print(self.FG_COLORS["light_cyan"] + "Version: " + self.FG_COLORS["light_blue"] + self.current_version)
        self.print(self.FG_COLORS["light_cyan"] + "Authors:" + self.FG_COLORS["light_blue"] + "Filip Szkandera, Tadeáš Fryčák")
        self.print(self.FG_COLORS["light_cyan"] + "IP: " + self.FG_COLORS["light_blue"] + "127.0.0.1")
        self.print(self.FG_COLORS["light_cyan"] + "Port: " + self.FG_COLORS["light_blue"] + "5000")

        # TODO: Automatically files print
        self.print("Working directory: ", color="light_cyan")
        self.print("  - Path: " + self.current_folder, color="light_blue")
        self.print("  - Created: %s" % time.ctime(os.path.getctime(self.current_folder)), color="light_blue")
        self.print("  - Last modified: %s" % time.ctime(os.path.getmtime(self.current_folder)), color="light_blue")
        self.print("Flask Python file:", color="light_cyan")
        self.print("  - Path: " + self.current_file, color="light_blue")
        self.print("  - Created: %s" % time.ctime(os.path.getctime(self.current_file)), color="light_blue")
        self.print("  - Last modified: %s" % time.ctime(os.path.getmtime(self.current_file)), color="light_blue")
        self.print(self.SEPARATOR, color="blue")

    def print(self, data=None, align=None, color=None):
        """
        Print to Python Console
        :a
        :return:
        """
        
        if align == "center":
            if color is not None:
                print((self.FG_COLORS[color] + data + self.END).center(len(self.SEPARATOR)))

            else:
                print(data.center(len(self.SEPARATOR)))

        else:
            if color is not None:
                print(self.FG_COLORS[color] + data + self.END)

            else:
                print(data)


    def error(self, data):
        self.print(self.NEWLINE)
        self.print(self.ERROR, color="fail")
        self.print(data, color="fail")
        self.print(self.ERROR, color="fail")
        self.print(self.NEWLINE)

    def warning(self, data):
        self.print(self.NEWLINE)
        self.print(self.WARNING, color="yellow")
        self.print(data, color="yellow")
        self.print(self.WARNING, color="yellow")
        self.print(self.NEWLINE)
        
    def debug(self, data):
        self.print(data, color="light_green")
