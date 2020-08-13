import random


class DefaultValues:
    TILE_TYPE = "blank"

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
    def tile_value(value_name=None, tile_type=None):
        """
        Get default tile value - it's not dynamic
        :param value_name: value name
        :param tile_type: tile type
        :return: value
        """

        if value_name == "value" and tile_type == "toggle":
            return 0

        elif value_name == "value" and tile_type == "value":
            return {"value": "Null", "suffix": ""}

        elif value_name == "value" and tile_type == "value_double":
            return {"left": {"value": "Null", "suffix": ""}, "right": {"value": "Null", "suffix": ""}}

        elif value_name == "icon":
            return "none.png"

        elif value_name == "value" and tile_type == "blank":
            return None

        else:
            return False

    def tile(self):
        tile_value = self.tile_value(value_name="value", tile_type=self.TILE_TYPE)

        if tile_value:
            return {"type": self.TILE_TYPE, "value": tile_value, "modal": [], "data": {"id": self.random_id()}}

        else:
            return {"type": self.TILE_TYPE, "modal": [], "data": {"id": self.random_id()}}
