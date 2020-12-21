from flask_babel import Babel, _, gettext, ngettext, lazy_gettext
import library.jinja2schema as jinja2schema
import datetime


class TemplateManagerRead:
    """
    Template manager read class
    """

    # Main, system
    ICON_PATH = "static/img/icons"
    BACK = "../"

    # App.py
    TILE_ID = "tile_id"

    # devices.json
    TYPE = "type"
    CONFIG = "config"
    MODAL = "modal"
    ID = "id"
    NAME = "name"
    VALUE = "value"
    VALUES = "values"
    LABEL = "label"

    SLIDER = "slider"
    TOGGLE = "toggle"
    GRAPH = "graph"

    DATA_X = "data_x"
    DATA_Y = "data_y"

    UNNAMED = lazy_gettext("Unnamed")
    MODAL_ITEM_UNNAMED = ""

    CHILDREN = "children"

    X = "x"
    Y = "y"

    def __init__(self, fmng, terminal, default_values, refactoring, default_items):
        """
        Init of class TemplateManagerRead
        :param fmng: FileManager
        """

        self.__default_items = default_items
        self.__fmng = fmng
        self.__terminal = terminal
        self.__refactoring = refactoring
        self.__default_values = default_values

    def get_tile(self, tile_id):
        """
        Get tile by tile ID
        :param tile_id: tile ID
        :return: tile
        """
        # Get pages (number and content)
        for page_content in self.__fmng.devices:
            # Get item for current device
            for tile in page_content[self.CHILDREN]:
                # If device have current id
                if tile[self.ID] == tile_id:
                    return tile

    def get_display_tile(self, tile_id):
        tile = self.get_tile(tile_id)
        for num, item in enumerate(tile["modal"]):
            tile["modal"][num]["value"] = self.__default_items.get_object(item["type"]).on_display_value(item["value"])
        return tile

    def get_tile_type(self, tile_id):
        """
        Get tile type by tile ID
        :param tile_id: tile ID
        :return: tile type
        """

        return self.get_tile(tile_id=tile_id)[self.TYPE]

    def get_tile_templates(self):
        """
        Get tile templates
        :return: tile templates
        """

        return self.__fmng.list_file_names(path="templates/tiles", name="*.html", extension=False)

    # def get_modal_templates(self):
    #     """
    #     Get modal templates
    #     :return: modal templates
    #     """
    #
    #     return self.__default_items.get_item_names()

    def get_tile_template_values(self, tile_type=None, tile_id=None):
        """
        Get tile template values
        :param tile_type: tile type
        :param tile_id: tile ID
        :return:
        """

        template = str(self.__fmng.load_file("templates/tiles/" + tile_type + ".html"))
        variables = jinja2schema.infer(template)

        tile = None
        data = {}

        if tile_id:
            tile = self.get_tile(tile_id=tile_id)

        try:
            for value in dict(variables["tile"]["data"]):
                if value != "id" and value != "value" and value != "label":
                    try:
                        data[value] = tile[self.CONFIG][value]

                    except KeyError:
                        data[value] = self.MODAL_ITEM_UNNAMED

            if "icon" in data:
                if data["icon"] != self.MODAL_ITEM_UNNAMED:
                    current_icon = data["icon"]

                else:
                    current_icon = self.__default_values.tile_value(value_name="icon")

                data["icon"] = []

                # Browse directory and load backgrounds
                for file in self.__fmng.list_file_names(path=self.ICON_PATH):
                    if file == current_icon:
                        current = True

                    else:
                        current = False

                    data["icon"].append({"name": file, "current": current})

        except KeyError:  # Tile without data
            pass

        return data

    def get_items_config(self):
        # configs = self.__fmng.load_files_from_dir(dir_path=self.__fmng.CONFIG_ITEMS_DIR)
        #
        # for item in configs:
        #     for value in configs[item][self.CONFIG]:
        #         try:
        #             configs[item][self.CONFIG][value][self.CONFIG][self.LABEL] = self.__refactoring.translate(configs[item][self.CONFIG][value][self.CONFIG][self.LABEL])
        #         except KeyError:  # Item config value hasn't label
        #             pass
        # return configs
        # TODO optimalizace - + přejmenovat class Items()
        return self.__default_items.get_item_types()

    def get_modal_template_values(self, item_type):
        """
        Get modal template values
        :param item_type: modal item type
        :return:
        """

        values = self.get_items_config()
        config = {}

        for value in values[item_type][self.CONFIG]:
            config[value] = values[item_type][self.CONFIG][value]["value"]

        return values[item_type]["value"], config

    def get_slide_index(self, tile_id):
        """
        Get slide index
        :param tile_id:
        :return:
        """

        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get item for current device
            for tile in page_content[self.CHILDREN]:
                # If device have current id
                if tile[self.ID] == tile_id:
                    return page_num

    def get_modal_date_range_pickers(self, tile_id):
        """
        Return all toggles in modal by id_tile
        :param tile_id: id of tile
        :return: toggles in modal
        """

        date_range_pickers = {}

        # Get modal items
        for modal_item in self.get_tile(tile_id=tile_id)[self.MODAL]:
            # If that item is toggle, append
            if modal_item[self.TYPE] == "daterangepicker":
                date_range_pickers[modal_item[self.ID]] = modal_item[self.VALUE]

        return date_range_pickers

    def get_modal_graphs(self, tile_id=None, item_id=None):
        """
        Return all toggles in modal by id_tile
        :param item_id: ID of item
        :param tile_id: ID of tile
        :return: toggles in modal
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for tile_num, tile_content in enumerate(page_content[self.CHILDREN]):
                # If that tile is current opened tile
                if tile_content[self.ID] == tile_id:
                    graphs = {}

                    # Get modal items
                    for modal_item in tile_content[self.MODAL]:
                        # If that item is toggle, append
                        if modal_item[self.TYPE] == self.GRAPH:
                            data_x = modal_item[self.VALUE][self.X]
                            data_y = modal_item[self.VALUE][self.Y]
                            minimized_x = []
                            minimized_y = []
                            for modal_item2 in tile_content[self.MODAL]:
                                if modal_item2[self.TYPE] == "daterangepicker" and modal_item2[self.CONFIG]["pair"] == modal_item[self.ID]:
                                    start = datetime.datetime.strptime(modal_item2[self.VALUE]["start"], "%Y-%m-%d %H:%M:%S")  # TODO to constant
                                    end = datetime.datetime.strptime(modal_item2[self.VALUE]["end"], "%Y-%m-%d %H:%M:%S")

                                    for num, i in enumerate(data_x):
                                        if datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") >= start and datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") <= end:
                                            minimized_x.append(i)
                                            minimized_y.append(data_y[num])

                                    break

                            if item_id is not None and modal_item[self.ID] == item_id:
                                return {self.DATA_X: minimized_x, self.DATA_Y: minimized_y}

                            if not minimized_x:
                                minimized_x = data_x
                                minimized_y = data_y

                            graphs[modal_item[self.ID]] = {self.DATA_X: minimized_x, self.DATA_Y: minimized_y}

                    return graphs
