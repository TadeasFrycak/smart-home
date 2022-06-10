from flask_babel import lazy_gettext
import datetime


class TemplateManagerRead:
    """
    Template manager read class
    """

    # Main, system
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

    def __init__(self, fmng, terminal, refactoring, default_items, default_tiles):
        """
        Init of class TemplateManagerRead
        :param fmng: FileManager
        """

        self.__default_items = default_items
        self.__default_tiles = default_tiles
        self.__fmng = fmng
        self.__terminal = terminal
        self.__refactoring = refactoring

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

    def get_protocol(self, tile_id, item_id=None):
        # Get pages (number and content)
        for page_content in self.__fmng.devices:
            # Get item for current device
            for tile in page_content[self.CHILDREN]:
                # If device have current id
                if tile[self.ID] == tile_id:
                    if item_id:
                        for item in tile[self.MODAL]:
                            if item[self.ID] == item_id:
                                return item["protocols"]

                    else:
                        return tile["protocols"]

    def get_item(self, tile_id, item_id):
        tile = self.get_tile(tile_id)
        # Get pages (number and content)
        for item_content in tile["modal"]:
            # Get item for current device
            if item_content[self.ID] == item_id:
                return item_content

    def get_display_tile(self, tile_id):
        tile = self.get_tile(tile_id)
        for num, item in enumerate(tile["modal"]):
            tile["modal"][num]["value"] = self.__default_items.get_object(item["type"]).on_display_value(item["value"], item["config"])
        return tile

    def get_tile_type(self, tile_id):
        """
        Get tile type by tile ID
        :param tile_id: tile ID
        :return: tile type
        """

        return self.get_tile(tile_id=tile_id)[self.TYPE]

    def get_tiles_config(self):
        return self.__default_tiles.get_tile_edit_objects()

    def get_items_config(self):
        return self.__default_items.get_item_edit_objects()

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
