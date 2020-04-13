import random
import glob
import os


class TemplateManager:
    """
    Template Manager class
    """

    # Main, system
    IMG_PATH = "static/images/backgrounds"
    ICON_PATH = "static/images/icons"
    SEPARATOR = "::"
    BACK = "../"

    # App.py
    EDIT = "edit"
    INDEX = "index"
    OLD_INDEX = "old_index"
    NEW_INDEX = "new_index"
    OLD_VALUE = "old_value"
    NEW_VALUE = "new_value"
    NEW_TYPE = "new_type"
    TILE_ID = "tile_id"
    TILE = "tile"

    # Replacement
    ITEMS = "items"
    TYPE = "type"
    DATA = "data"
    CONTENT = "content"
    BACKGROUND = "background_image"
    MODAL = "modal"
    ID = "id"
    NAME = "name"
    STATUS = "status"
    VALUE = "value"
    VALUES = "values"
    LABEL = "label"

    MODAL_ITEMS = "modal_items"
    TILE_ITEMS = "tile_items"
    TILE_NAME = "tile_name"

    MAX = "max"
    MIN = "min"
    MAX_MIN = "max_min"

    HEADER = "header"
    ERROR = "error"

    SLIDER = "slider"
    SLIDERS = "sliders"
    TOGGLE = "toggle"
    TOGGLES = "toggles"
    GRAPH = "graph"
    GRAPHS = "graphs"

    DATA_X = "data_x"
    DATA_Y = "data_y"

    # Items - modal_edit
    MODAL_EDIT = "modal_edit"
    ADD_ITEM = "add_item"
    TILE_TYPE = "tile_type"
    ITEM_VALUE = "item_value"
    ITEM_CLOSE_BUTTON = "item_delete_button"
    ITEMS_SORT = "items_sort"

    # Replacement - modal_edit
    TEXT = "text"
    CLOSE_BUTTON = "close_button"
    ACTIVE = "active"
    CHECKED = "checked"
    ID_VALUE = "id_value"
    PREVIEW = "preview"

    UNNAMED = "Bez názvu"

    X = "x"
    Y = "y"

    OPTIONS = "options"

    ICON_ITEM = "icon_item"
    ICON_CHOOSER = "icon_chooser"
    TILE_VALUE = "tile_value"

    ADD = "add"
    BLANK = "blank"
    PAGE_INDEX = "page_index"

    def __init__(self, fmng, console, default_values):
        """
        Init of class TemplateManager
        :param fmng: FileManager
        """

        self.__fmng = fmng
        self.__console = console
        self.__default_values = default_values


    def random_background(self):
        """
        Load backgrounds and choose one of them (randomly)
        :return:
        """

        backgrounds = []

        os.chdir(self.IMG_PATH)

        # Browse directory and load backgrounds
        for file in glob.glob("*.*"):
            backgrounds.append("/" + self.IMG_PATH + "/" + file)

        if "/" in self.IMG_PATH:
            os.chdir(self.BACK*len(self.IMG_PATH.split("/")))

        elif "\\" in self.IMG_PATH:
            os.chdir(self.BACK*len(self.IMG_PATH.split("\\")))

        else:
            self.__console.print("TMNG - fatal error in part background", 2)

        return random.choice(backgrounds)

    @staticmethod
    def __random_id():
        """
        Make random ID
        :return: random ID
        """

        return "id-" + str(random.randrange(1000, 9999))

    def __value(self, data):
        """
        Complete separators to data value
        :param data: value to complete
        :return:
        """

        return self.SEPARATOR + data + self.SEPARATOR

    @staticmethod
    def __refactor(data):
        """
        Refactor data
        :param data: data to refactor
        :return:
        """

        if len(str(data)) <= 2:
            return str(data).upper()

        else:
            return str(data).lower().capitalize().replace("-", " ").replace("_", " ")

    @staticmethod
    def refactor_reverse(data):
        """
        Derefactor refactored data
        :param data: refactored data
        :return:
        """

        return str(data).strip().lower().replace(" ", "_")

    # Index page preparing
    def index_content(self):
        """
        Complete index.html template by devices config and items config
        :return: completed index.html template
        """

        # Define array to render
        to_render = []

        # Get pages (number and content)
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            items = []

            # Get item for current device
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                item = self.__fmng.items[self.ITEMS][device[self.TYPE]]

                # Replace variables in item
                for value in device[self.DATA].keys():
                    item = item.replace(self.__value(value), device[self.DATA][value])

                items.append(item)

            to_render.append({"content": "".join(items), "name": page_content[self.NAME]})

        # Return completed template
        return to_render

    def get_tile_values(self, element_id):
        type = ""
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get item for current device
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                # If device have current id
                if device[self.DATA][self.ID] == element_id:
                    type += str(device[self.TYPE])

                    # Tile item values
        value_names = []
        for num, value in enumerate(self.__fmng.items[self.ITEMS][type].split(self.SEPARATOR)):
            # If it is not remaining HTML
            if num % 2 and value not in value_names:
                if value != "id" and value != "label" and value != "status" and value != "percentage":  # TODO not dynamic
                    value_names.append(value)

        to_render_tile_types = []
        # Get pages (number and content)
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get item for current device
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                # If device have current id
                if device[self.DATA][self.ID] == element_id:
                    # Icons
                    if "img_src" in value_names:
                        to_render_icons = []

                        icons = []

                        os.chdir(self.ICON_PATH)

                        # Browse directory and load backgrounds
                        for file in glob.glob("*.*"):
                            icons.append({"path": "/" + self.ICON_PATH + "/" + file, "name": file})

                        if "/" in self.ICON_PATH:
                            os.chdir(self.BACK * len(self.ICON_PATH.split("/")))

                        elif "\\" in self.ICON_PATH:
                            os.chdir(self.BACK * len(self.ICON_PATH.split("\\")))

                        for i in icons:
                            if i["name"] in device[self.DATA]["img_src"]:
                                to_render_icons.append(
                                    self.__fmng.items[self.MODAL_EDIT][self.ICON_ITEM].replace(self.__value("path"),
                                                                                               i["path"]).replace(
                                        self.__value("name"), i["name"]).replace(self.__value(self.CHECKED),
                                                                                 self.CHECKED))

                            else:
                                to_render_icons.append(
                                    self.__fmng.items[self.MODAL_EDIT][self.ICON_ITEM].replace(self.__value("path"),
                                                                                               i["path"]).replace(
                                        self.__value("name"), i["name"]).replace(self.__value(self.CHECKED), ""))

                        to_render_tile_types.append(
                            self.__fmng.items[self.MODAL_EDIT][self.ICON_CHOOSER].replace(self.__value(self.CONTENT),
                                                                                          "".join(to_render_icons)))

                    for i in value_names:
                        if i != "img_src":
                            to_render_tile_types.append(
                                self.__fmng.items[self.MODAL_EDIT][self.TILE_VALUE].replace(self.__value(self.NAME),
                                                                                            self.__refactor(i)).replace(
                                    self.__value(self.VALUE), device[self.DATA][i]))
                    break  # If there is more than one ID

            else:
                continue

            break
        return "".join(to_render_tile_types)
    # Tile
    def get_tile(self, tile_id):
        """
        Get content of page, where is current edited tile
        :param tile_id: id of edited tile
        :return:
        """

        # Define array to render
        to_render = []

        # Get pages (number and content)
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get item for current device
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                if device[self.DATA][self.ID] == tile_id:
                    item = self.__fmng.items[self.ITEMS][device[self.TYPE]]

                    # Replace variables in item
                    for value in device[self.DATA].keys():
                        item = item.replace(self.__value(value), device[self.DATA][value])

                    to_render.append(item)
                    break
            else:
                continue

            break

        # Return completed page content
        return "".join(to_render)

    # Modal
    def modal_content(self, element_id=None, edit=None, add=None, page_index=None):
        """
        Complete modal
        :param element_id: ID of tile
        :param edit: is current mode edit?
        :param add: is edit add mode?
        :param page_index: index of current page
        :return:
        """

        # Edit mode is not active
        if add is not True:
            if edit is False:
                to_render = []

                # Get pages (number and content)
                for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
                    # Get item for current device
                    for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                        # If device have current id
                        if device[self.DATA][self.ID] == element_id:
                            # Get modal items
                            for modal_item in device[self.MODAL]:
                                try:
                                    item = self.__fmng.items[self.MODAL][modal_item[self.TYPE]]
                                except Exception as e:
                                    self.__console.print(
                                        "{0} item is not created in items.json. Probably wrong configuration of"
                                        "devices.json".format(e), 2)

                                # Get value to overwrite
                                try:
                                    for value in modal_item[self.DATA].keys():
                                        item = item.replace(self.__value(value), modal_item[self.DATA][value])

                                except Exception as e:  # When there is item without data
                                    pass

                                to_render.append(item)
                            break  # When there are more than one same ID
                    else:
                        continue

                    break

                return "".join(to_render)

            # Edit mode is active
            elif edit is True:
                to_render = []
                type = ""  # TODO global variables

                # Get pages (number and content)
                for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
                    # Get item for current device
                    for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                        # If device have current id
                        if device[self.DATA][self.ID] == element_id:
                            type += str(device[self.TYPE])  # TODO global +=
                            # Get modal items
                            for modal_item in device[self.MODAL]:
                                item = self.__fmng.items[self.MODAL_EDIT][self.ITEMS_SORT]

                                try:
                                    modal_item[self.DATA]

                                except Exception as e:  # If item is without data
                                    item = item.replace(
                                        self.__value(self.TYPE), self.__refactor(modal_item[self.TYPE])).replace(
                                        self.__value(self.NAME), self.UNNAMED).replace(
                                        self.__value(self.CLOSE_BUTTON),
                                        self.__fmng.items[self.MODAL_EDIT][self.ITEM_CLOSE_BUTTON]).replace(
                                        # self.__value(self.PREVIEW),
                                        # self.__fmng.items[self.MODAL][modal_item[self.TYPE]]).replace(
                                            self.__value(self.ITEMS), "")

                                else:
                                    values = []

                                    for value in modal_item[self.DATA]:
                                        values.append(self.__fmng.items[self.MODAL_EDIT][self.ITEM_VALUE].replace(
                                            self.__value(self.LABEL), self.__refactor(value)).replace(
                                            self.__value(self.VALUE), modal_item[self.DATA][value]))

                                    try:
                                        item = item.replace(
                                            self.__value(self.TYPE), self.__refactor(modal_item[self.TYPE])).replace(
                                            self.__value(self.NAME), modal_item[self.DATA][self.LABEL]).replace(
                                            self.__value(self.ITEMS), "".join(values)).replace(
                                            self.__value(self.CLOSE_BUTTON),
                                            self.__fmng.items[self.MODAL_EDIT][self.ITEM_CLOSE_BUTTON])

                                    except Exception as e:  # If there isn't label of item item
                                        item = item.replace(
                                            self.__value(self.TYPE), self.__refactor(modal_item[self.TYPE])).replace(
                                            self.__value(self.NAME), self.UNNAMED).replace(
                                            self.__value(self.ITEMS), "".join(values)).replace(
                                            self.__value(self.CLOSE_BUTTON),
                                            self.__fmng.items[self.MODAL_EDIT][self.ITEM_CLOSE_BUTTON])

                                to_render.append(item)

                            break  # When there are more than one same ID
                    else:
                        continue

                    break

                # Modal item buttons
                to_render_modal_items = []
                for i in self.__fmng.items[self.MODAL]:
                    to_render_modal_items.append(
                        self.__fmng.items[self.MODAL_EDIT][self.ADD_ITEM].replace(self.__value(self.TEXT),
                                                                                  self.__refactor(i)))

                # Edit tile buttons
                to_render_tile_items = []
                for i in self.__fmng.items[self.ITEMS]:
                    if i == type:
                        to_render_tile_items.append(
                            self.__fmng.items[self.MODAL_EDIT][self.TILE_TYPE].replace(self.__value(self.TEXT),
                                                                                       self.__refactor(i)).replace(
                                self.__value(self.CHECKED), self.CHECKED).replace(self.__value(self.ACTIVE),
                                                                                  self.ACTIVE))

                    else:
                        to_render_tile_items.append(
                            self.__fmng.items[self.MODAL_EDIT][self.TILE_TYPE].replace(self.__value(self.TEXT),
                                                                                       self.__refactor(i)).replace(
                                self.__value(self.CHECKED), "").replace(self.__value(self.ACTIVE), ""))

                # Tile item values
                value_names = []
                for num, value in enumerate(self.__fmng.items[self.ITEMS][type].split(self.SEPARATOR)):
                    # If it is not remaining HTML
                    if num % 2 and value not in value_names:
                        if value != "id" and value != "label" and value != "status" and value != "percentage":  # TODO not dynamic
                            value_names.append(value)

                to_render_tile_types = []
                # Get pages (number and content)
                for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
                    # Get item for current device
                    for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                        # If device have current id
                        if device[self.DATA][self.ID] == element_id:
                            # Icons
                            if "img_src" in value_names:
                                to_render_icons = []

                                icons = []

                                os.chdir(self.ICON_PATH)

                                # Browse directory and load backgrounds
                                for file in glob.glob("*.*"):
                                    icons.append({"path": "/" + self.ICON_PATH + "/" + file, "name": file})

                                if "/" in self.ICON_PATH:
                                    os.chdir(self.BACK * len(self.ICON_PATH.split("/")))

                                elif "\\" in self.ICON_PATH:
                                    os.chdir(self.BACK * len(self.ICON_PATH.split("\\")))

                                for i in icons:
                                    if i["name"] in device[self.DATA]["img_src"]:
                                        to_render_icons.append(self.__fmng.items[self.MODAL_EDIT][self.ICON_ITEM].replace(self.__value("path"), i["path"]).replace(self.__value("name"), i["name"]).replace(self.__value(self.CHECKED), self.CHECKED))

                                    else:
                                        to_render_icons.append(self.__fmng.items[self.MODAL_EDIT][self.ICON_ITEM].replace(self.__value("path"), i["path"]).replace(self.__value("name"), i["name"]).replace(self.__value(self.CHECKED), ""))

                                to_render_tile_types.append(self.__fmng.items[self.MODAL_EDIT][self.ICON_CHOOSER].replace(self.__value(self.CONTENT), "".join(to_render_icons)))

                            for i in value_names:
                                if i != "img_src":
                                    to_render_tile_types.append(self.__fmng.items[self.MODAL_EDIT][self.TILE_VALUE].replace(self.__value(self.NAME), self.__refactor(i)).replace(self.__value(self.VALUE), device[self.DATA][i]).replace(self.__value(self.ID), i))
                            break  # If there is more than one ID

                    else:
                        continue

                    break

                # Get pages (number and content)
                for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
                    # Get item for current device
                    for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                        if device[self.DATA][self.ID] == element_id:
                            return {"modal_items": "".join(to_render_modal_items),
                                    "tile_types": "".join(to_render_tile_items),
                                    "tile_name": device[self.DATA][self.LABEL],
                                    "tile_values": "".join(to_render_tile_types),
                                    "id_value": element_id,
                                    "content": "".join(to_render)}
            else:
                print("UNEXPECTED ERROR TEMPLATE MANAGER")
                # TODO unexpected error

        else:
            # Modal item buttons
            to_render_modal_items = []
            for i in self.__fmng.items[self.MODAL]:
                to_render_modal_items.append(
                    self.__fmng.items[self.MODAL_EDIT][self.ADD_ITEM].replace(self.__value(self.TEXT),
                                                                              self.__refactor(i)))

            # Edit tile buttons
            to_render_tile_items = []
            for i in self.__fmng.items[self.ITEMS]:
                if i == self.BLANK:
                    to_render_tile_items.append(
                        self.__fmng.items[self.MODAL_EDIT][self.TILE_TYPE].replace(self.__value(self.TEXT),
                                                                                   self.__refactor(i)).replace(
                            self.__value(self.CHECKED), self.CHECKED).replace(self.__value(self.ACTIVE),
                                                                              self.ACTIVE))
                else:
                    to_render_tile_items.append(
                        self.__fmng.items[self.MODAL_EDIT][self.TILE_TYPE].replace(self.__value(self.TEXT),
                                                                                   self.__refactor(i)).replace(
                            self.__value(self.CHECKED), "").replace(self.__value(self.ACTIVE), ""))

            new_id = self.__random_id()
            self.__fmng.devices()[self.ITEMS][page_index][self.DATA].append({self.TYPE: self.BLANK,
                                                                             self.DATA: {self.ID: new_id,
                                                                                         self.LABEL: self.UNNAMED},
                                                                             self.MODAL: []})

            return {"modal_items": "".join(to_render_modal_items), "tile_types": "".join(to_render_tile_items), "tile_name": self.UNNAMED, "id_value": new_id, "content": "", "tile_values": ""}

    def add_modal_edit_item(self, type_of_item, tile_id):
        """
        Get new SortableJS item in edit modal adn send it to JS to show it
        :param type_of_item: typ of item in modal - for example slider, toggle
        :param tile_id: tile ID
        :return:
        """

        # Get all items in items.json (MODAL)
        for i in self.__fmng.items[self.MODAL]:
            # If current item is sent item
            if i == self.refactor_reverse(type_of_item):
                values = []
                value_names = []

                new_id = self.__random_id()

                # Split item template by separator and get values
                # TODO je to společný s jednou další funkci - spojit dohromady
                for num, value in enumerate(self.__fmng.items[self.MODAL][i].split(self.SEPARATOR)):
                    # If it is not remaining HTML
                    if num % 2 and value not in value_names:
                        value_names.append(value)

                        # Add random number to ID, not other
                        if value == self.ID:
                            values.append(
                                self.__fmng.items[self.MODAL_EDIT][self.ITEM_VALUE].replace(self.__value(self.LABEL),
                                                                                            self.__refactor(
                                                                                                  value)).replace(
                                    self.__value(self.VALUE), new_id))
                        else:
                            values.append(
                                self.__fmng.items[self.MODAL_EDIT][self.ITEM_VALUE].replace(self.__value(self.LABEL),
                                                                                            self.__refactor(
                                                                                                value)).replace(
                                    self.__value(self.VALUE), self.UNNAMED))

                # Get pages (number and content)
                for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
                    # Get item for current device
                    for num, device in enumerate(self.__fmng.devices()[self.ITEMS][page][self.DATA]):
                        if device[self.DATA][self.ID] == tile_id:
                            reversed_type = self.refactor_reverse(type_of_item)

                            value = self.__default_values.default_modal_item_value(reversed_type)

                            # If is for current type default value, replace it
                            if value is not False:
                                to_save = {self.TYPE: reversed_type, self.VALUE: value}

                            else:
                                to_save = {self.TYPE: reversed_type}

                            # If it has values
                            if value_names is not []:
                                to_save[self.DATA] = {}

                                for j in value_names:
                                    # Add random number to ID, not other
                                    if j == self.ID:
                                        to_save[self.DATA][j] = new_id

                                    else:
                                        to_save[self.DATA][j] = self.UNNAMED

                            self.__fmng.devices()[self.ITEMS][page][self.DATA][num][self.MODAL].insert(0, to_save)

                            return self.__fmng.items[self.MODAL_EDIT][self.ITEMS_SORT].replace(self.__value(self.TYPE),
                                                                                               self.__refactor(
                                                                                                   i)).replace(
                                self.__value(self.NAME), self.UNNAMED).replace(self.__value(self.ITEMS),
                                                                               "".join(values)).replace(
                                self.__value(self.CLOSE_BUTTON),
                                self.__fmng.items[self.MODAL_EDIT][self.ITEM_CLOSE_BUTTON]).replace(
                                self.__value(self.PREVIEW), self.__fmng.items[self.MODAL][i])  # TODO ""

    def get_modal_sliders(self, id_tile):
        """
        Return all sliders in modal by id_tile
        :param id_tile: id of tile
        :return: sliders in modal
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == id_tile:
                    sliders = {}

                    # Get modal items
                    for modal_item in item_content[self.MODAL]:
                        # If that item is slider, append
                        if modal_item[self.TYPE] == self.SLIDER:
                            sliders[modal_item[self.DATA][self.ID]] = modal_item[self.VALUE]

                    return sliders

    def get_modal_toggles(self, id_tile):
        """
        Return all toggles in modal by id_tile
        :param id_tile: id of tile
        :return: toggles in modal
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == id_tile:
                    toggles = {}

                    # Get modal items
                    for modal_item in item_content[self.MODAL]:
                        # If that item is toggle, append
                        if modal_item[self.TYPE] == self.TOGGLE:
                            toggles[modal_item[self.DATA][self.ID]] = modal_item[self.VALUE]

                    return toggles

    def get_modal_graphs(self, id_tile):
        """
        Return all toggles in modal by id_tile
        :param id_tile: id of tile
        :return: toggles in modal
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == id_tile:
                    graphs = {}

                    # Get modal items
                    for modal_item in item_content[self.MODAL]:
                        # If that item is toggle, append
                        if modal_item[self.TYPE] == self.GRAPH:
                            data_x = modal_item[self.DATA_X]
                            data_y = modal_item[self.DATA_Y]

                            data = []
                            for i in range(len(data_x)):
                                data.append({self.X: data_x[i], self.Y: data_y[i]})

                            graphs[modal_item[self.DATA][self.ID]] = {}
                            graphs[modal_item[self.DATA][self.ID]][self.VALUES] = data
                            graphs[modal_item[self.DATA][self.ID]][self.LABEL] = modal_item[self.LABEL]
                            graphs[modal_item[self.DATA][self.ID]][self.MAX_MIN] = {self.X: {self.MAX: max(data_x),
                                                                                             self.MIN: min(data_x)},
                                                                                    self.Y: {self.MAX: max(data_y),
                                                                                             self.MIN: min(data_y)}}
                    return graphs
