import random
import glob
import os


class TemplateManager:
    """
    Template Manager class
    """

    # Main, system
    IMG_PATH = "static/images/backgrounds"
    SEPARATOR = "::"
    BACK = "../"

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
    TOGGLE = "toggle"
    GRAPH = "graph"

    DATA_X = "data_x"
    DATA_Y = "data_y"

    STATUSES = ["OFF", "ON"]

    # Items - modal_edit
    MODAL_EDIT = "modal_edit"
    ADD_ITEM = "add_item"
    TILE_TYPE = "tile_type"
    ITEM_VALUE = "item_value"
    ITEM_CLOSE_BUTTON = "item_close_button"
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

    def __init__(self, fmng, console):
        """
        Init of class TemplateManager
        :param fmng: FileManager
        """

        self.__fmng = fmng
        self.__console = console

        self.__index_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "index.html"),
                                                      False)
        self.__error = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "error.html"), False)
        self.__page_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "page.html"),
                                                     False)
        self.__modal_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "modal.html"),
                                                      False)
        self.__modal_edit_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR,
                                                                                 "modal_edit.html"), False)

    def __random_background(self):
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
            self.__console.print("TMNG - fatal error in part background", priority=2)

        return random.choice(backgrounds)

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

    def get_modal_edit_item(self, type_of_item):
        """
        Get new SortableJS item in edit modal adn send it to JS to show it
        :param type_of_item: typ of item in modal - for example slider, toggle
        :return:
        """

        # Get all items in items.json (MODAL)
        for i in self.__fmng.items()[self.MODAL]:
            # If current item is sent item
            if i == self.refactor_reverse(type_of_item):
                values = []
                value_names = []

                # Split item template by separator and get values
                for num, value in enumerate(self.__fmng.items()[self.MODAL][i].split(self.SEPARATOR)):  # TODO je to společný s jednou další funkci - spojit dohromady
                    # If it is not remaining HTML
                    if num % 2 and value not in value_names:
                        value_names.append(value)
                        values.append(
                            self.__fmng.items()[self.MODAL_EDIT][self.ITEM_VALUE].replace(self.__value(self.LABEL),
                                                                                          self.__refactor(
                                                                                              value)).replace(
                                self.__value(self.VALUE), self.UNNAMED))

                return self.__fmng.items()[self.MODAL_EDIT][self.ITEMS_SORT].replace(self.__value(self.TYPE),
                                                                                     self.__refactor(i)).replace(
                    self.__value(self.NAME), self.UNNAMED).replace(self.__value(self.ITEMS), "".join(values)).replace(
                    self.__value(self.CLOSE_BUTTON),
                    self.__fmng.items()[self.MODAL_EDIT][self.ITEM_CLOSE_BUTTON]).replace(self.__value(self.PREVIEW),
                                                                                          self.__fmng.items()[
                                                                                              self.MODAL][i])  # TODO ""

    def reload_files(self):
        """
        Reload all files
        IMPORTANT - it is only for debug and better testing
        :return:
        """

        # Same as from __init__
        self.__index_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "index.html"),
                                                      False)
        self.__page_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "page.html"),
                                                     False)
        self.__modal_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "modal.html"),
                                                      False)
        self.__modal_edit_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR,
                                                                                 "modal_edit.html"), False)

    # Index page preparing
    def index(self):
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
                item = self.__fmng.items()[self.ITEMS][device[self.TYPE]]

                # Replace variables in item
                for value in device[self.DATA].keys():
                    item = item.replace(self.__value(value), device[self.DATA][value])

                items.append(item)

            to_render.append(
                self.__page_template.replace(self.__value(self.CONTENT), "".join(items)).replace(
                    self.__value(self.NAME), page_content[self.NAME]))

        # Return completed template
        return self.__index_template.replace(self.__value(self.CONTENT), "".join(to_render)).replace(
            self.__value(self.BACKGROUND), self.__random_background())

    def page_content(self, element_id):
        """
        Get content of page, where is current edited tile
        :param element_id: id of edited tile
        :return:
        """

        # Define array to render
        page_index = 0  # TODO chybně napsané +=

        # Get pages (number and content)
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get item for current device
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                if device[self.DATA][self.ID] == element_id:
                    page_index += page
                    break
            else:
                continue

            break

        # Define array to render
        to_render = []

        # Get item for current device
        for device in self.__fmng.devices()[self.ITEMS][page_index][self.DATA]:
            item = self.__fmng.items()[self.ITEMS][device[self.TYPE]]

            # Replace variables in item
            for value in device[self.DATA].keys():
                item = item.replace(self.__value(value), device[self.DATA][value])

            to_render.append(item)

        # Return completed page content
        return "".join(to_render)

    # Error page preparing
    def error_page(self, header, error):
        """
        Generate error page
        :param header: header of page
        :param error: error
        :return: page
        """

        return self.__error.replace(self.__value(self.HEADER), header).replace(self.__value(self.ERROR), error)

    # Modal
    def modal(self, element_id, edit):
        """
        Complete modal
        :param element_id: ID of tile
        :param edit: is current mode edit?
        :return:
        """

        # Edit mode is not active
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
                            item = self.__fmng.items()[self.MODAL][modal_item[self.TYPE]]

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

            return self.__modal_template.replace(self.__value(self.CONTENT), "".join(to_render))

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
                            try:
                                modal_item[self.DATA]

                            except Exception as e:
                                pass

                            else:
                                values = []
                                for value in modal_item[self.DATA]:
                                    values.append(self.__fmng.items()[self.MODAL_EDIT][self.ITEM_VALUE].replace(
                                        self.__value(self.LABEL), self.__refactor(value)).replace(
                                        self.__value(self.VALUE), modal_item[self.DATA][value]))

                                try:
                                    item = self.__fmng.items()[self.MODAL_EDIT][self.ITEMS_SORT].replace(
                                        self.__value(self.TYPE), self.__refactor(modal_item[self.TYPE])).replace(
                                        self.__value(self.NAME), modal_item[self.DATA][self.LABEL]).replace(
                                        self.__value(self.ITEMS), "".join(values)).replace(
                                        self.__value(self.CLOSE_BUTTON),
                                        self.__fmng.items()[self.MODAL_EDIT][self.ITEM_CLOSE_BUTTON]).replace(
                                        self.__value(self.PREVIEW),
                                        self.__fmng.items()[self.MODAL][modal_item[self.TYPE]])  # TODO ""

                                    to_render.append(item)

                                except Exception as e:  # When there is item without data
                                    item = self.__fmng.items()[self.MODAL_EDIT][self.ITEMS_SORT].replace(
                                        self.__value(self.TYPE), self.__refactor(modal_item[self.TYPE])).replace(
                                        self.__value(self.NAME), self.UNNAMED).replace(self.__value(self.ITEMS),
                                                                                       "".join(values)).replace(
                                        self.__value(self.CLOSE_BUTTON),
                                        self.__fmng.items()[self.MODAL_EDIT][self.ITEM_CLOSE_BUTTON])  # TODO ""

                                    to_render.append(item)
                        break  # When there are more than one same ID
                else:
                    continue

                break

            to_render_modal_items = []
            for i in self.__fmng.items()[self.MODAL]:
                to_render_modal_items.append(self.__fmng.items()[self.MODAL_EDIT][self.ADD_ITEM].replace(self.__value(self.TEXT), self.__refactor(i)))

            to_render_tile_items = []
            for i in self.__fmng.items()[self.ITEMS]:
                if i == type:
                    to_render_tile_items.append(self.__fmng.items()[self.MODAL_EDIT][self.TILE_TYPE].replace(self.__value(self.TEXT), self.__refactor(i)).replace(self.__value(self.CHECKED), self.CHECKED).replace(self.__value(self.ACTIVE), self.ACTIVE))
                else:
                    to_render_tile_items.append(self.__fmng.items()[self.MODAL_EDIT][self.TILE_TYPE].replace(self.__value(self.TEXT), self.__refactor(i)).replace(self.__value(self.CHECKED), "").replace(self.__value(self.ACTIVE), ""))

            # Get pages (number and content)
            for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
                # Get item for current device
                for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                    if device[self.DATA][self.ID] == element_id:
                        return self.__modal_edit_template.replace(self.__value(self.CONTENT), "".join(to_render)).replace(self.__value(self.MODAL_ITEMS), "".join(to_render_modal_items)).replace(self.__value(self.TILE_ITEMS), "".join(to_render_tile_items)).replace(self.__value(self.TILE_NAME), device[self.DATA][self.LABEL]).replace(self.__value(self.ID_VALUE), element_id)
# TODO "".join "" na constant
        else:
            print("UNEXPECTED ERROR TEMPLATE MANAGER")
            # TODO unexpected error

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
