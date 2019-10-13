
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
    
    def __init__(self):
        pass

    def complete_template(self, template, devices, items):
        pages_and_items = []
        to_render = []

        # Get pages (number and content)
        for page, page_content in enumerate(devices[self.ITEMS]):
            pages_and_items.append([])

            # Get item for current device
            for device in devices[self.ITEMS][page]:
                item = items[self.ITEMS][device[self.TYPE]]

                # Replace variables in item
                for value in device[self.DATA].keys():
                    item = item.replace(self.SEPARATOR + value + self.SEPARATOR, device[self.DATA][value])
                    
                pages_and_items[page].append(item)

        # Put devices into the pages
        for num, i in enumerate(pages_and_items):
            to_render.append(self.PAGE_TEMPLATE[0] + "".join(pages_and_items[num]) + self.PAGE_TEMPLATE[1])
        
        return template.replace(self.SEPARATOR + self.CONTENT + self.SEPARATOR, "".join(to_render))

    def complete_modal(self, id, devices, items):
        to_render = []
        
        # Get pages (number and content)
        for page, page_content in enumerate(devices[self.ITEMS]):
            # Get item for current device
            for device in devices[self.ITEMS][page]:
                if device[self.DATA][self.ID] == id:
                    for modal_item in device[self.MODAL]:
                        print(modal_item)
                        item = items[self.MODAL][modal_item[self.TYPE]]
                        for value in modal_item[self.DATA].keys():
                            print(value)
                            item = item.replace(self.SEPARATOR + value + self.SEPARATOR, modal_item[self.DATA][value])

                        to_render.append(item)
        print(to_render)   
        return self.MODAL_TEMPLATE[0] + "".join(to_render) + self.MODAL_TEMPLATE[1]
