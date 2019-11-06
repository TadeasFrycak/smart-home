import random
import glob
import os


class TemplateManager:
    """
    Template Manager
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

    SLIDER = "slider"
    TOGGLE = "toggle"

    STATUSES = ["OFF", "ON"]

    SEPARATOR = "::"

    BACK = "../"

    IMG_PATH = "static/images/backgrounds"
    
    def __init__(self, fmng, console):
        """
        Init of class TemplateManager
        :param fmng: FileManager
        """

        self.__fmng = fmng
        self.__console = console

        self.__template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "index.html"), False)
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
            self.__console.print("TMNG - error in part background", priority="error")
            
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

        self.__template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "index.html"), False)
        self.__items = self.__fmng.items(overwrite=True)
        self.__page_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "page.html"),
                                                     False)
        self.__modal_template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "modal.html"),
                                                      False)
        
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
        return self.__template.replace(self.__value(self.CONTENT), "".join(to_render)).replace(
            self.__value(self.BACKGROUND), self.__random_background())

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
