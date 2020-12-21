import math

from flask_babel import gettext, ngettext, lazy_gettext, lazy_ngettext
import time


class Refactoring:
    """
    Refactoring class
    """

    dictionary = {
        # Tile type
        "blank": lazy_gettext("blank"),
        "alarm_clock": lazy_gettext("alarm_clock"),
        "value_double": lazy_gettext("value_double"),
        "player": lazy_gettext("player"),
        "toggle": lazy_gettext("toggle"),
        # Modal type
        "date_range_picker": lazy_gettext("date_range_picker"),
        "button": lazy_gettext("button"),
        "dropdown_menu": lazy_gettext("dropdown_menu"),
        "graph": lazy_gettext("graph"),
        "separator": lazy_gettext("separator"),
        "slider": lazy_gettext("slider"),
        "time_picker": lazy_gettext("time_picker"),
        "progress_bar": lazy_gettext("progress_bar"),
        # Modal item values
        "label": lazy_gettext("label"),
        "value": lazy_gettext("value"),
        "value_min": lazy_gettext("value_min"),
        "value_max": lazy_gettext("value_max"),
        "color": lazy_gettext("color"),
        "colour": lazy_gettext("colour"),
        "pair": lazy_gettext("pair"),
        "step": lazy_gettext("step"),
    }

    UPPER_CASE = ["id"]

    def __init__(self):
        """
        Init of Refactoring class
        """

        pass

    def refactor(self, data):
        """
        Refactor string, list or dict
        :param data: data to refactor
        :return: refactored data
        """

        if isinstance(data, dict):
            refactored_data = {}
            for i in data:
                refactored_data[self.refactor(i)] = data[i]

            return refactored_data

        elif isinstance(data, list):
            refactored_data = []
            for i in data:
                refactored_data.append(self.refactor(i))

            return refactored_data

        else:
            edited = data.strip().lower()
            translated = self.translate(edited)

            if edited in self.UPPER_CASE:
                return str(translated).upper()

            else:
                pre_refactored_data = str(translated).capitalize().replace("-", " ").replace("_", " ")
                if len(pre_refactored_data.split(" ")) == 1:
                    return pre_refactored_data

                else:
                    split = pre_refactored_data.split(" ")
                    refactored = [self.refactor(split.pop(0))]

                    for i in split:
                        refactored.append(i)

                    return " ".join(refactored)

    def refactor_remove(self, data, string):
        return self.refactor(data.replace(string, ""))

    def translate(self, data):
        """
        Translate phrase
        :param data: phrase to translate
        :return: translated data
        """

        try:
            return self.dictionary[data]

        except KeyError:
            return gettext(data)

    def translate_reverse(self, data):
        """
        Translate reverse phrase
        :param data: phrase to translate back
        :return: translated data
        """

        for num, value in enumerate(self.dictionary.values()):
            if value == data:
                return list(self.dictionary.keys())[num]

        return data

    def refactor_reverse(self, data):
        """
        Refactor back refactored data
        :param data: refactored data
        :return: reversed refactored data
        """

        return self.translate_reverse(str(data).strip().lower().replace(" ", "_"))

    @staticmethod
    def get_time_ago(data):
        time_ago = math.floor(time.time() - data)
        time_ago_minute = math.floor(time_ago / 60)
        time_ago_hour = math.floor(time_ago / 3600)
        time_ago_day = math.floor(time_ago / 86400)
        time_ago_week = math.floor(time_ago_day / 7)
        time_ago_month = math.floor(time_ago_day / 30.4375)
        time_ago_year = math.floor(time_ago_day / 365.25)

        if time_ago < 60:
            ago = gettext("now")

        elif time_ago_minute < 60:
            ago = ngettext("%(num)s minute", "%(num)s minutes", time_ago_minute)

        elif time_ago_hour < 24:
            ago = ngettext("%(num)s hour", "%(num)s hours", time_ago_hour)

        elif time_ago_day <= 7:
            ago = ngettext("%(num)s day", "%(num)s days", time_ago_day)

        elif time_ago_week < 10:
            ago = ngettext("%(num)s week", "%(num)s weeks", time_ago_week)

        elif time_ago_month < 12:
            ago = ngettext("%(num)s month", "%(num)s months", time_ago_month)

        else:
            ago = ngettext("%(num)s year", "%(num)s years", time_ago_year)

        return ago.capitalize()
