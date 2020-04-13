class DefaultValues:
    STATUSES = ["OFF", "ON"]

    def __init__(self):
        pass

    @staticmethod
    def default_modal_item_value(type_of_item):
        """
        Get default modal item value - it's not dynamic
        :param type_of_item: type of item
        :return: default value
        """

        if type_of_item == "slider":
            return 50

        elif type_of_item == "toggle":
            return 0

        else:
            return False

    def default_tile_value(self, value_name):
        """
        Get default tile value - it's not dynamic
        :param value_name: value name
        :return: value
        """

        if value_name == "status":
            return self.STATUSES[0]

        elif value_name == "suffix":
            return "%"

        elif value_name == "percentage":
            return "Null"

        elif value_name == "img_src":
            return "/static/images/icons/none.png"
        else:
            print("TEMPLATEMANAGER - ERROR EXCEPT2")  # TODO
