import random


class DefaultValues:
    def __init__(self):
        pass

    @staticmethod
    def random_id():
        """
        Make random ID
        :return: random ID
        """

        return "id-" + str(random.randrange(1000, 9999))

    @staticmethod
    def modal_item_value(type_of_item):
        """
        Get default modal item value - it's not dynamic
        :param type_of_item: type of item
        :return: default value
        """

        if type_of_item == "slider" or type_of_item == "progress_bar":
            return 50

        elif type_of_item == "toggle":
            return 0

        elif type_of_item == "daterangepicker":
            return {"start": "2000-01-01 00:00:00", "end": "2200-01-01 00:00:00"}

        elif type_of_item == "graph":
            return {"x": [], "y": []}

        else:
            return None

    @staticmethod
    def tile_value(value_name, tile_type):
        """
        Get default tile value - it's not dynamic
        :param value_name: value name
        :param tile_type: tile type
        :return: value
        """

        if value_name == "value" and tile_type == "toggle":
            return 0

        elif value_name == "suffix":
            return "%"

        elif value_name == "value" and tile_type == "percentage":
            return "Null"

        elif value_name == "icon":
            return "none.png"

        else:
            return False

    @staticmethod
    def tile_type():
        return "blank"
