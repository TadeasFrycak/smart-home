import random
import glob
import os


class TemplateManager:
    """
    Template Manager class
    """

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

    SEPARATOR = "::"

    BACK = "../"

    X = "x"
    Y = "y"

    OPTIONS = "options"

    INPUT_HTML = "<input type='text'>"
    INPUT_AND_STRING = "<div class='edit_list_item_dropdown'>{0}: {1}</div>"
    OPTION_FORMULA = "<div class='edit_list_source_item list-group-item'>{0}<div class='edit_list_dropdown'>{1}</div></div>"

    IMG_PATH = "static/images/backgrounds"
    
    def __init__(self, fmng, console):
        """
        Init of class TemplateManager
        :param fmng: FileManager
        """

        self.__fmng = fmng
        self.__console = console

        self.__index_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "index.html"),
                                                      False)
        self.__edit_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "edit.html"), False)
        self.__error = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "error.html"), False)
        self.__page_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "page.html"),
                                                     False)
        self.__modal_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "modal.html"),
                                                      False)
        self.__items = self.__fmng.items(overwrite=False)

    def __random_background(self):
        """
        Load backgrounds and choose one of them
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

    def reload_files(self):
        """
        Reload all files
        // only for debug
        :return:
        """

        self.__index_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "index.html"),
                                                      False)
        self.__edit_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "edit.html"),
                                                     False)
        self.__items = self.__fmng.items(overwrite=True)
        self.__page_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "page.html"),
                                                     False)
        self.__modal_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "modal.html"),
                                                      False)

    def error_page(self, header, error):
        """
        Generate error page
        :param header: header of page
        :param error: error
        :return: page
        """

        return self.__error.replace(self.__value(self.HEADER), header).replace(self.__value(self.ERROR), error)

    def edit(self):
        # Define arrays
        to_render_tiles = []

        # Get pages (number and content)
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            items = []

            # Get item for current device
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                item = self.__items[self.ITEMS][device[self.TYPE]]

                # Replace variables in item
                for value in device[self.DATA].keys():
                    if device[self.TYPE] == self.TOGGLE and value == self.STATUS:
                        item = item.replace(self.__value(value), self.STATUSES[0])

                    else:
                        item = item.replace(self.__value(value), device[self.DATA][value])

                items.append(item)

            to_render_tiles.append(
                self.__page_template.replace(self.__value(self.CONTENT), "".join(items)).replace(
                    self.__value(self.NAME), page_content[self.NAME]))

        to_render_modal_opt = []

        for i in self.__fmng.items()[self.MODAL]:
            to_render_modal_val = []

            for num, j in enumerate(self.__fmng.items()[self.MODAL][i].split(self.SEPARATOR)):
                if (num-1) % 2 == 0:
                    to_render_modal_val.append(self.INPUT_AND_STRING.format(str(j).lower().capitalize(), self.INPUT_HTML))

            to_render_modal_opt.append(self.OPTION_FORMULA.format(i.capitalize(), "".join(to_render_modal_val)))

        # Return completed template
        return self.__edit_template.replace(self.__value(self.CONTENT), "".join(to_render_tiles)).replace(
            self.__value(self.BACKGROUND), self.__random_background()).replace(self.__value(self.OPTIONS),
                                                                               "".join(to_render_modal_opt))

    def index(self):
        """
        Complete index.html template by devices config and items config
        :return: completed index.html template
        """

        # Define arrays
        to_render = []

        # Get pages (number and content)
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            items = []

            # Get item for current device
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                item = self.__items[self.ITEMS][device[self.TYPE]]

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

    def check_duplicity_ids(self):
        # Check duplicity for tiles
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            IDs = []

            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                # Check duplicity for current device
                if device[self.DATA][self.ID] not in IDs:
                    IDs.append(device[self.DATA][self.ID])

                else:
                    return device

        # Check duplicity for items in modals
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                try:
                    IDs = []
                    for modal_item in device[self.MODAL]:
                        if modal_item[self.DATA][self.ID] not in IDs:
                            IDs.append(modal_item[self.DATA][self.ID])

                        else:
                            return device

                except Exception as e:
                    pass

        return True

    def complete_modal(self, element_id):
        """
        Complete modal from config by ID
        :param element_id: ID of current modal
        :return:
        """

        to_render = []

        # Get pages (number and content)
        for page, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get item for current device
            for device in self.__fmng.devices()[self.ITEMS][page][self.DATA]:
                # If device have current id
                if device[self.DATA][self.ID] == element_id:
                    # Get modal items
                    for modal_item in device[self.MODAL]:
                        item = self.__items[self.MODAL][modal_item[self.TYPE]]

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

    def get_sliders(self, id_tile):
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

    def get_toggles(self, id_tile):
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

    def get_graphs(self, id_tile):
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

    def tile_rwr(self, state, element_id):
        """
        Rewrite tile status
        :param state: state of tile
        :param element_id: id of tile
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == element_id:
                    self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.STATUS] = self.STATUSES[int(state)]
                    self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                         self.__fmng.CONFIG_DEVICES),
                                              data=self.__fmng.devices(), is_json=True)
                    return True

    def toggle_rwr(self, id_tile, state, element_id):
        """
        Rewrite toggle status
        :param id_tile: id of mother tile
        :param state: state of toggle
        :param element_id: toggle id
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == id_tile:
                    # Get modal items
                    for modal_num, modal_item in enumerate(item_content[self.MODAL]):
                        # If that item is toggle, rewrite
                        if modal_item[self.TYPE] == self.TOGGLE and modal_item[self.DATA][self.ID] == element_id:
                            self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.MODAL][modal_num][self.VALUE] = state
                            self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                                 self.__fmng.CONFIG_DEVICES),
                                                      data=self.__fmng.devices(), is_json=True)
                            return True

    def slider_rwr(self, id_tile, state, element_id):
        """
        Rewrite slider value
        :param id_tile: id of mother tile
        :param state: state of slider
        :param element_id: id of slider
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == id_tile:
                    # Get modal items
                    for modal_num, modal_item in enumerate(item_content[self.MODAL]):
                        # If that item is slider rewrite
                        if modal_item[self.TYPE] == self.SLIDER and modal_item[self.DATA][self.ID] == element_id:
                            self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.MODAL][modal_num][self.VALUE] = state
                            self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                                 self.__fmng.CONFIG_DEVICES),
                                                      data=self.__fmng.devices(), is_json=True)
                            return True

    def graph_rwr(self, id_tile, data_x, data_y, element_id):
        """
        Rewrite graph data
        :param id_tile: ID of graph parent (tile)
        :param data_x: data on X
        :param data_y: data on Y
        :param element_id: ID of current graph
        :return:
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == id_tile:
                    # Get modal items
                    for modal_num, modal_item in enumerate(item_content[self.MODAL]):
                        # If that item is graph rewrite
                        if modal_item[self.TYPE] == self.GRAPH and modal_item[self.DATA][self.ID] == element_id:
                            self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.MODAL][modal_num][self.DATA_X].append(data_x)
                            self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.MODAL][modal_num][self.DATA_Y].append(data_y)
                            self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                                 self.__fmng.CONFIG_DEVICES),
                                                      data=self.__fmng.devices(), is_json=True)
                            return True

    def title_rwr(self, index, value):
        self.__fmng.devices()[self.ITEMS][index][self.NAME] = value

    def append_slide(self, index, value):
        self.__fmng.devices()[self.ITEMS].append({self.NAME: value, self.DATA: []})

    def remove_slide(self, index):
        self.__fmng.devices()[self.ITEMS].pop(index)

    def tile_title_rwr(self, element_id, name):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == element_id:
                    self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.LABEL] = name

                    return True

    def change_tile_type(self, element_id, type):
        print("Aalsdhfjksdhlfkjhd")  # TODO
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.ITEMS][page_num][self.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.DATA][self.ID] == element_id:
                    self.__fmng.devices()[self.ITEMS][page_num][self.DATA][item_num][self.TYPE] = type

                    return True
