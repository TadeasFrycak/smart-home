import os
import glob
import time
import sys
import colorama
import socket


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
        """
        Print intro to console
        :return:
        """
        
        print()
        self.print(self.SEPARATOR, color="blue")
        self.print(data="Smart Home - App", align="center", color="light_cyan")
        self.print(self.SEPARATOR, color="blue")
        self.print(self.FG_COLORS["light_cyan"] + "Version: " + self.FG_COLORS["light_blue"] + self.current_version)
        self.print(self.FG_COLORS["light_cyan"] + "Authors: " + self.FG_COLORS["light_blue"] + "Filip Szkandera, Tadeáš Fryčák")
        self.print(self.FG_COLORS["light_cyan"] + "IP: " + self.FG_COLORS["light_blue"] + socket.gethostbyname(socket.gethostname()))
        self.print(self.FG_COLORS["light_cyan"] + "Flask local IP: " + self.FG_COLORS["light_blue"] + "127.0.0.1")
        self.print(self.FG_COLORS["light_cyan"] + "Port: " + self.FG_COLORS["light_blue"] + "5000")

        startpath = "static"
        
        #for root, dirs, files in os.walk(startpath):
        #    level = root.replace(startpath, '').count(os.sep)

        #    indent = " " * 4 * (level)
        #    self.print("{}{}/".format(indent, os.path.basename(root)), color="light_cyan")
            
        #    subindent = ' ' * 4 * (level + 1)
        #    for f in files:
        #        self.print("{}{}".format(subindent, f), color="light_cyan")
        #        self.print("{}    Path: {}".format(subindent, os.path.join(root, f)), color="light_blue")
        #        self.print("{}    Created: {}".format(subindent, time.ctime(os.path.getctime(os.path.join(root, f)))), color="light_blue")
        #        self.print("{}    Last modifed: {}".format(subindent, time.ctime(os.path.getmtime(os.path.join(root, f)))), color="light_blue")

        self.print(self.SEPARATOR, color="blue")

    def print(self, data=None, align=None, color=None):
        """
        Print to Python Console
        :a
        :return:
        """
        
        if align == "center":
            if color is not None:
                print((self.FG_COLORS[color] + str(data) + self.END).center(len(self.SEPARATOR)))

            else:
                print(str(data).center(len(self.SEPARATOR)))

        else:
            if color is not None:
                print(self.FG_COLORS[color] + str(data) + self.END)

            else:
                print(str(data))


    def error(self, data):
        """
        Print error to console
        :data: Data to print
        :return:
        """
        
        self.print(self.NEWLINE)
        self.print(self.ERROR, color="fail")
        self.print(data, color="fail")
        self.print(self.ERROR, color="fail")
        self.print(self.NEWLINE)

    def warning(self, data):
        """
        Print Warning to console
        :data: Data to print
        :return:
        """
        
        self.print(self.NEWLINE)
        self.print(self.WARNING, color="yellow")
        self.print(data, color="yellow")
        self.print(self.WARNING, color="yellow")
        self.print(self.NEWLINE)
        
    def debug(self, data):
        """
        Debug print to console
        :data: Data to print
        :return:
        """
        
        self.print(data, color="light_green")
