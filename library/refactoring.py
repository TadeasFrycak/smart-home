class Refactoring:
    dictionary = {
                  # Tile type
                  "3d_printer": "3d_tiskárna",
                  "blank": "prázdný",
                  "percentage": "procento",
                  "player": "přehrávač",
                  "toggle": "přepínač",
                  # Modal type
                  "button": "tlačítko",
                  "dropdown_menu": "rozbalovací_nabídka",
                  "graph": "graf",
                  "graph_picker": "volba_výběru_grafu",
                  "separator": "oddělovač",
                  "slider": "posuvník",
                  "time_picker": "volba_času",
                  "progress_bar": "ukazatel_průběhu",
                  # Modal item values
                  "label": "název",
                  "value": "hodnota",
                  "color": "barva",
                  "colour": "barva",
                  "pair": "vázaný_na"
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
        return data
        try:
            return self.dictionary[data]

        except Exception as e:
            return data

    def translate_reverse(self, data):
        return data
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
