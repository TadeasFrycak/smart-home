from flask_babel import gettext, lazy_gettext


class Refactoring:
    dictionary = {
        # Tile type
        "blank": lazy_gettext("blank"),
        "alarm_clock": lazy_gettext("alarm_clock"),
        "value_double": lazy_gettext("value_double"),
        "player": lazy_gettext("player"),
        "toggle": lazy_gettext("toggle"),
        # Modal type
        "daterangepicker": lazy_gettext("daterangepicker"),
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
        "pair": lazy_gettext("pair")
    }

    def __init__(self):
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
            translated = self.translate(data.strip().lower())

            if len(str(translated)) <= 2:
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

    def translate(self, data):
        try:
            return self.dictionary[data]

        except Exception as e:
            return data

    def translate_reverse(self, data):
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
