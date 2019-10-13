
class TemplateManager:
    ITEMS = "items"
    TYPE = "type"
    DATA = "data"
    CONTENT = "content"
    MODAL = "modal"
    ID = "id"

    SEPARATOR = "::"

    PAGE_TEMPLATE = ["<div class='swiper-slide'><div class='swipe-header'>AHDFHASJHDLFKJHASLDKFHSLDKJFHDJH</div><div class='swipe-content'>", "</div></div>"]
    MODAL_TEMPLATE = ["<div id='tile-Modal' class='tile-modal'><div class='tile-modal-content'> <span class='close'>&times;</span><div class='modalContent'><div class='modalHeader'>UNDEFINED</div>", "</div></div></div>"]
    
    def __init__(self, fmng):
        self.__fmng = fmng
        self.__template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "index.html"), False)
        self.__devices = self.__fmng.devices(overwrite=False)
        self.__items = self.__fmng.items(overwrite=False)
        
    def reload_files(self):
        self.__template = self.__fmng.load_file(self.__fmng.path_join(self.__fmng.TEMPLATES_DIR, "index.html"), False)
        self.__devices = self.__fmng.devices(overwrite=True)
        self.__items = self.__fmng.items(overwrite=True)
        
    def index(self):
        """
        Complete index.html template by devices config and items config
        :return: completed index.html template
        """

        # Define arrays
        pages_and_items = []
        to_render = []

        # Get pages (number and content)
        for page, page_content in enumerate(self.__devices[self.ITEMS]):
            pages_and_items.append([])

            # Get item for current device
            for device in self.__devices[self.ITEMS][page]:
                item = self.__items[self.ITEMS][device[self.TYPE]]

                # Replace variables in item
                for value in device[self.DATA].keys():
                    item = item.replace(self.SEPARATOR + value + self.SEPARATOR, device[self.DATA][value])
                    
                pages_and_items[page].append(item)

        # Put devices into pages
        for num, i in enumerate(pages_and_items):
            to_render.append(self.PAGE_TEMPLATE[0] + "".join(pages_and_items[num]) + self.PAGE_TEMPLATE[1])

        # Return completed template
        return self.__template.replace(self.SEPARATOR + self.CONTENT + self.SEPARATOR, "".join(to_render))

    def complete_modal(self, id):
        to_render = []
        
        # Get pages (number and content)
        for page, page_content in enumerate(self.__devices[self.ITEMS]):
            # Get item for current device
            for device in self.__devices[self.ITEMS][page]:
                # If device have current id
                if device[self.DATA][self.ID] == id:
                    # Get modal items
                    for modal_item in device[self.MODAL]:
                        item = self.__items[self.MODAL][modal_item[self.TYPE]]

                        # Get value to overwrite
                        for value in modal_item[self.DATA].keys():
                            item = item.replace(self.SEPARATOR + value + self.SEPARATOR, modal_item[self.DATA][value])

                        to_render.append(item)

        return self.MODAL_TEMPLATE[0] + "".join(to_render) + self.MODAL_TEMPLATE[1]
