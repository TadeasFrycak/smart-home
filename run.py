from pkg_resources import DistributionNotFound, VersionConflict
from library.logger import TerminalLogger
from library.terminal import Terminal
from packaging import version
import pkg_resources
import subprocess
import platform
import signal
import socket
import time
import sys
import os

# TODO python3.8 -m pip install --upgrade pip
# TODO sudo apt install python3-pip
# TODO zde bude validace souborů, JSONů, ...
# TODO Nebude Ok, jen pokud najde chybu, tak něco vypíše + na začátku napíše info
# TODO MQTT check
# TODO na RPi nejde nainstalovat Telegram bot, ale program píše, že nainstaloval správně, kontrolovat exit status commandu

ready = False
restarting = False

logger = TerminalLogger()
terminal = Terminal(logger=logger, log_lines=False)


def exit_program():
    print()
    exit()


def kill():
    # Not working on windows
    subprocess.run(["pkill", "-f", "start.py"])


def ctrl(signal_number, stack_frame):
    if ready:
        print()
        # TODO poslat informaci do hlavního programu, že se server killnul
        # TODO nebo udělat z run.py a start.py jeden soubor/implementovat tyhle killovací věci do start.py
        terminal.warning("Pressed Ctrl+C.. Exiting.. Please don't use this to shutdown the server")
        exit_program()


def install(to_install):
    for module in to_install:
        terminal.debug("Installing Python module '{}'...".format(module))
        # try:
        subprocess.run([sys.executable, "-m", "pip", "install", module]) #, shell=True, stderr=subprocess.STDOUT)
        # except subprocess.CalledProcessError as e:
        #     if "no module named pip" in str(e.output).lower():
        #         # Todo nainstalovat sám na MACU i na Linuxu
        #         terminal.error("Pip is not installed! Please install it.")
        #     else:
        #         terminal.error("Unexpected error: command '{}' return with error (code {}): {}".format(str(e.cmd), str(e.returncode), str(e.output)))
        # else:
        #     if "successfully" not in str(output).lower():
        #         terminal.error("Unexpected error in output: {}".format(str(output)))


if platform.system().lower() == "windows":
    terminal.error("Windows is not supported! Please run on Linux or Mac")
    exit_program()


# Not working on Windows
user_id = os.geteuid()
if user_id == 0:  # Is run as root
    # TODO nesmí vůbebc terminal načítat logy
    terminal.error("Don't run me please with sudo permission!")
    exit_program()


signal.signal(signal.SIGINT, ctrl)

kill()

with open("requirements.txt", mode="r") as f:
    dependencies = []
    for num, requirement in enumerate(f.readlines()):
        dependency = requirement.strip()
        if num == 0:
            split_dependency = dependency.split()

            if split_dependency[0] == "#" and split_dependency[1] == "python":
                # terminal.error("Python requirement is not valid")
                dependency_version = version.parse(split_dependency[3])
                try:
                    python_version = version.parse(platform.python_version())
                    if ((python_version >= dependency_version) and split_dependency[2] == ">=") or ((python_version == dependency_version) and split_dependency[2] == "==") or ((python_version <= dependency_version) and split_dependency[2] == "<="):
                        pass

                    else:
                        terminal.error("Python version '{}' is wrong. Required version is '{}'".format(python_version, dependency_version))
                        exit_program()

                except ValueError:
                    pass

            else:
                terminal.error("Python requirement is not in requirements.txt")
                exit_program()

        else:
            if "#" not in dependency:
                try:
                    pkg_resources.require(dependency)

                except DistributionNotFound:
                    dependencies.append(dependency)
                    module_name = dependency.split("=")[0].split(">")[0].split("<")[0]
                    terminal.error("Module '{}' is missing".format(module_name))

                except VersionConflict as e:
                    dependencies.append(dependency)
                    module_name = dependency.split("=")[0].split(">")[0].split("<")[0]
                    module_version = pkg_resources.get_distribution(module_name).version
                    terminal.warning("Module '{module}' is outdated. Required '{required}', current "
                                  "'{module}=={installed}'".format(module=module_name, required=dependency,
                                                                   installed=module_version))

    if dependencies:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            server_ip = s.getsockname()[0]
            s.close()

        except OSError:
            terminal.error("No internet connection to update modules")
            exit_program()

        else:
            print()
            install(to_install=dependencies)
            terminal.debug("All modules are installed")
            time.sleep(1)

    ready = True

    while True:
        subprocess.run([sys.executable, "start.py", str(os.getpid())])
        print()

        if restarting:
            restarting = False

        else:
            terminal.error("Error in code!")
            time.sleep(10)

        terminal.print(terminal.FG_COLORS["cyan"] + terminal.SPECIAL["bold"] + "Server is restarting..." + terminal.END)
