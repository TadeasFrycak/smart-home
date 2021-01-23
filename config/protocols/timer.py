import time
from threading import Thread
from config.protocols.default import Protocol
from flask_babel import gettext
from datetime import datetime


class TimerThread(Thread):
    def __init__(self, terminal, general):
        super().__init__()
        self.__general = general
        self.times = []

    def run(self):
        while True:
            now = datetime.now()

            current_time = now.strftime("%H:%M")
            if current_time in self.times:
                self.__general.update("timer", True, {"time": current_time})
                
            time.sleep(1)


class Timer(Protocol):
    TYPE = "timer"
    VISIBLE = True
    NAME = gettext("Timer")

    __HOME = "home"

    def __init__(self, terminal, update):
        super().__init__(terminal, update)

        if not self.thread.is_alive():
            self.thread = TimerThread(terminal=self._terminal, general=self._general)
            self.thread.start()

    def config(self):
        return {
            self._TIME: "00:00",
        }

    def edit_config(self):
        from config.items.clock_picker import ClockPicker

        return {
            self._TIME: ClockPicker().make_object(value=self.config()[self._TIME], label=gettext("Time"))
        }

    def add_listener_inner(self, config):
        self.thread.times.append(config[self._TIME])

    def remove_listener_inner(self, config):
        self.thread.times.remove(config[self._TIME])
