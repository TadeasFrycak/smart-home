import time
from threading import Thread
from config.protocols.default import Protocol
from flask_babel import gettext
from datetime import datetime, timedelta


class AlarmThread(Thread):
    FORMAT = "%H:%M"

    def __init__(self, terminal, general):
        super().__init__()
        self.__general = general
        self.times = []

    def run(self):
        while True:
            now = datetime.now()
            current_time = now.strftime(self.FORMAT)
            for i in self.times:
                current_object = datetime.strptime(current_time, self.FORMAT)
                list_object = datetime.strptime(i, self.FORMAT)

                if current_object == list_object:
                    self.__general.update("alarm", True, {"time": i})

                elif current_object == list_object + timedelta(minutes=1):
                    self.__general.update("alarm", False, {"time": i, "auto_off": True})

            time.sleep(3)


class Alarm(Protocol):
    TYPE = "alarm"
    VISIBLE = True
    NAME = gettext("Alarm")

    def __init__(self, terminal, update):
        super().__init__(terminal, update)

        if not self.thread.is_alive():
            self.thread = AlarmThread(terminal=self._terminal, general=self._general)
            self.thread.start()

    def config(self):
        return {
            self._TIME: (datetime.now() + timedelta(minutes=10)).strftime(self.thread.FORMAT),
            self._ON_VALUE: 1,
            self._REPEAT: []
        }

    def edit_config(self):
        from config.items.clock_picker import ClockPicker
        from config.items.button_group import ButtonGroup
        from config.items.input import Input

        return {
            self._TIME: ClockPicker().make_object(value=self.config()[self._TIME], label=gettext("Time")),
            # TODO repeat
            self._REPEAT: ButtonGroup().make_object(value=self.config()[self._REPEAT], label=gettext("Repeat"), checkbox=True,
                                                    options=[["monday", gettext("Monday")[0]],
                                                             ["tuesday", gettext("Tuesday")[0]],
                                                             ["wednesday", gettext("Wednesday")[0]],
                                                             ["thursday", gettext("Thursday")[0]],
                                                             ["friday", gettext("Friday")[0]],
                                                             ["saturday", gettext("Saturday")[0]],
                                                             ["sunday", gettext("Sunday")[0]]]),
            self._ON_VALUE: Input().make_object(value=self.config()[self._ON_VALUE], label=gettext("On value"))
        }

    def add_listener_inner(self, config):
        self.thread.times.append(config[self._TIME])

    def remove_listener_inner(self, config):
        self.thread.times.remove(config[self._TIME])
