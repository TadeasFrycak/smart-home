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
        self.__devices = self.__fmng.devices(overwrite=False)
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
        self.__devices = self.__fmng.devices(overwrite=True)
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
        for page, page_content in enumerate(self.__devices[self.ITEMS]):
            items = []

            # Get item for current device
            for device in self.__devices[self.ITEMS][page][self.DATA]:
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

    def complete_modal(self, id):
        """
        Complete modal from config by ID
        :param id: ID of current modal
        :return:
        """

        to_render = []

        # Get pages (number and content)
        for page, page_content in enumerate(self.__devices[self.ITEMS]):
            # Get item for current device
            for device in self.__devices[self.ITEMS][page][self.DATA]:
                # If device have current id
                if device[self.DATA][self.ID] == id:
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
