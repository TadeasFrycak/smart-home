from flask_babel import Babel, _, gettext, ngettext, lazy_gettext
from jinja2 import Environment, PackageLoader, meta, FileSystemLoader
import jinja2schema
import datetime


class TemplateManagerRead:
    """
    Template Manager Read class
    """

    # Main, system
    ICON_PATH = "static/img/icons"
    BACK = "../"

    # App.py
    TILE_ID = "tile_id"

    # devices.json
    TYPE = "type"
    DATA = "data"
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

    UNNAMED = gettext("Unnamed")

    CHILDREN = "children"

    X = "x"
    Y = "y"

    def __init__(self, fmng, console, default_values, refactoring):
        """
        Init of class TemplateManagerRead
        :param fmng: FileManager
        """

        self.__fmng = fmng
        self.__console = console
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
                if tile["data"]["id"] == tile_id:
                    return tile

    def get_tile_type(self, tile_id):
        """
        Get tile type by tile ID
        :param tile_id: tile ID
        :return: tily type
        """
        return self.get_tile(tile_id=tile_id)[self.TYPE]

    def get_tile_templates(self):
        """
        Get tile templates
        :return: tile templates
        """

        return self.__fmng.list_file_names(path="templates/tiles", name="*.html", extension=False)

    def get_modal_templates(self):
        """
        Get modal templates
        :return: modal templates
        """

        return self.__fmng.list_file_names(path="templates/modal", name="*.html", extension=False)

    def get_tile_template_values(self, tile_type=None, tile_id=None):
        """
        Get tile template values
        :param tile_type: tile type
        :param tile_id: tile ID
        :return:
        """
        # TODO Refactor všeho (if icon in data, ...)
        # env = Environment(loader=FileSystemLoader('templates'))
        # template_source = env.loader.get_source(env, "tiles/" + tile_type + ".html")[0]
        # parsed_content = env.parse(template_source)
        # print(parsed_content)
        # print(meta.find_undeclared_variables(parsed_content))

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
                        data[value] = tile[self.DATA][value]

                    except Exception as e:
                        data[value] = self.UNNAMED

            if "icon" in data:
                if data["icon"] != self.UNNAMED:
                    current_icon = data["icon"]

                else:
                    current_icon = self.__default_values.tile_value("icon")

                data["icon"] = []

                # Browse directory and load backgrounds
                for file in self.__fmng.list_file_names(path=self.ICON_PATH):
                    if file == current_icon:
                        current = True

                    else:
                        current = False

                    data["icon"].append({"name": file, "current": current})

        except Exception as e:  # Tile without data
            pass

        return data

    def get_modal_template_values(self, item_type):
        """
        Get modal template values
        :param item_type: modal item type
        :return:
        """
        template = str(self.__fmng.load_file("templates/modal/" + item_type + ".html"))
        variables = jinja2schema.infer(template)

        data = {}

        try:
            for value in dict(variables["item"]["data"]):
                if value == "id":
                    data[value] = self.__default_values.random_id()

                elif value == "value":
                    data[value] = self.__default_values.modal_item_value(item_type)

                else:
                    data[value] = self.UNNAMED

            if "value" not in data:
                value = self.__default_values.modal_item_value(item_type)

                if value is not None:
                    data["value"] = value

        except Exception as e:  # Modal item without data
            pass

        return data

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
                if tile["data"]["id"] == tile_id:
                    return page_num

    def get_modal_daterangepickers(self, tile_id):
        """
        Return all toggles in modal by id_tile
        :param tile_id: id of tile
        :return: toggles in modal
        """

        daterangepickers = {}

        # Get modal items
        for modal_item in self.get_tile(tile_id=tile_id)[self.MODAL]:
            # If that item is toggle, append
            if modal_item[self.TYPE] == "daterangepicker":
                daterangepickers[modal_item[self.DATA][self.ID]] = modal_item[self.DATA][self.VALUE]

        return daterangepickers

    def get_modal_graphs(self, tile_id=None, item_id=None):
        """
        Return all toggles in modal by id_tile
        :param tile_id: id of tile
        :return: toggles in modal
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for tile_num, tile_content in enumerate(page_content[self.CHILDREN]):
                # If that tile is current opened tile
                if tile_content[self.DATA][self.ID] == tile_id:
                    graphs = {}

                    # Get modal items
                    for modal_item in tile_content[self.MODAL]:
                        # If that item is toggle, append
                        if modal_item[self.TYPE] == self.GRAPH:
                            data_x = modal_item[self.DATA][self.VALUE][self.X]
                            data_y = modal_item[self.DATA][self.VALUE][self.Y]
                            minimized_x = []
                            minimized_y = []
                            for modal_item2 in tile_content[self.MODAL]:
                                if modal_item2[self.TYPE] == "daterangepicker" and modal_item2[self.DATA]["pair"] == modal_item[self.DATA][self.ID]:
                                    start = datetime.datetime.strptime(modal_item2[self.DATA][self.VALUE]["start"], "%Y-%m-%d %H:%M:%S")  # TODO to constant
                                    end = datetime.datetime.strptime(modal_item2[self.DATA][self.VALUE]["end"], "%Y-%m-%d %H:%M:%S")

                                    for num, i in enumerate(data_x):
                                        if datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") >= start and datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") <= end:
                                            minimized_x.append(i)
                                            minimized_y.append(data_y[num])

                                    break

                            if item_id is not None and modal_item[self.DATA][self.ID] == item_id:
                                return {self.DATA_X: minimized_x, self.DATA_Y: minimized_y}

                            if not minimized_x:
                                minimized_x = data_x
                                minimized_y = data_y

                            graphs[modal_item[self.DATA][self.ID]] = {self.DATA_X: minimized_x,
                                                                      self.DATA_Y: minimized_y}

                    return graphs
