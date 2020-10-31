import random
import string


class DefaultValues:
    TILE_TYPE = "blank"

    def __init__(self, fmng):
        self.__fmng = fmng

    @staticmethod
    def create_random_id():
        return "".join(random.choices(string.ascii_lowercase, k=2)) + "".join(random.choices(string.digits.lower(), k=4))

    def random_id(self):
        """
        Make random ID
        :return: random ID
        """
        IDs = []
        for page, page_content in enumerate(self.__fmng.devices):
            for device in page_content["children"]:
                # Check duplicity for current device
                if device["data"]["id"] not in IDs:
                    IDs.append(device["data"]["id"])

        random_id = self.create_random_id()
        while random_id in IDs:
            random_id = self.create_random_id()

        return random_id

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

        if value_name == "value":
            if tile_type == "toggle":
                return 0

            elif tile_type == "value":
                return {"value": "Null", "time": None, "suffix": ""}

            elif tile_type == "value_double":
                return {"left": {"value": "Null", "suffix": ""}, "right": {"value": "Null", "suffix": ""}}

            elif tile_type == "blank":
                return None

            elif tile_type == "alarm_clock":
                return {"main": False, "monday": False, "tuesday": False, "wednesday": False, "thursday": False,
                        "friday": False, "saturday": False, "sunday": False}

        elif value_name == "icon":
            return "none.png"

        return False

    def tile(self):
        """
        Get default tile
        :return: default tile
        """

        tile_value = self.tile_value(value_name="value", tile_type=self.TILE_TYPE)

        if tile_value:
            return {"type": self.TILE_TYPE, "value": tile_value, "modal": [], "data": {"id": self.random_id()}}

        else:
            return {"type": self.TILE_TYPE, "modal": [], "data": {"id": self.random_id()}}
