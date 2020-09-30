import json
import re


class Validator:
    """
    Validator class
    """

    def __init__(self, fmng, tmng_r, refactoring, console):
        """
        Init of Validator
        :param fmng: file_manager
        :param tmng_r: template_manager
        """

        self.__fmng = fmng
        self.__tmng_r = tmng_r
        self.__refactoring = refactoring
        self.__console = console

    def validate_jsons(self):
        """
        Validate JSONs
        :return: True/exception
        """

        try:
            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.APP_CONFIG_DIR,
                                            self.__fmng.DEVICES_FILE), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.APP_CONFIG_DIR,
                                            self.__fmng.WHITELIST_FILE), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.APP_CONFIG_DIR,
                                            self.__fmng.BLACKLIST_FILE), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.MAC_LIST_FILE), "r") as f:
                json.load(f)

        except Exception as e:
            return e

        else:
            return True

    def check_duplicity_ids(self):
        """
        Check duplicity IDs of modal and tiles
        :return:
        """

        # Check duplicity for tiles
        IDs = []
        for page, page_content in enumerate(self.__fmng.devices):
            for device in page_content[self.__tmng_r.CHILDREN]:
                # Check duplicity for current device
                if device[self.__tmng_r.DATA][self.__tmng_r.ID] not in IDs:
                    IDs.append(device[self.__tmng_r.DATA][self.__tmng_r.ID])

                else:
                    return device

        # Check duplicity for items in modals
        for page, page_content in enumerate(self.__fmng.devices):
            for device in page_content[self.__tmng_r.CHILDREN]:
                try:
                    IDs = []
                    for modal_item in device[self.__tmng_r.MODAL]:
                        if modal_item[self.__tmng_r.DATA][self.__tmng_r.ID] not in IDs:
                            IDs.append(modal_item[self.__tmng_r.DATA][self.__tmng_r.ID])

                        else:
                            return device

                except Exception:
                    pass

        return True

    def tile_id(self, tile):
        if isinstance(tile, str) and 40 >= len(tile) >= 6:
            if re.match("^[a-zA-Z0-9-_]+$", tile):
                tile_content = self.__tmng_r.get_tile(tile_id=tile)
                if tile_content:
                    self.__console.print("Tile ID '{}' is OK".format(tile), 0.2)
                    return tile_content

        self.__console.print("Tile ID '{}' is NOT OK".format(tile), 0.2)

    def tile_new_id(self, new_id):
        if isinstance(new_id, str) and 40 >= len(new_id) >= 6:
            if re.match("^[a-zA-Z0-9-_]+$", new_id):
                self.__console.print("New tile ID '{}' is OK".format(new_id), 0.2)
                return True

        self.__console.print("New tile ID '{}' is NOT OK".format(new_id), 0.2)

    def tile_value(self, value):
        if isinstance(value, int) or isinstance(value, dict):
            self.__console.print("Value '{}' is OK".format(value), 0.2)
            return True

        self.__console.print("Value '{}' is NOT OK".format(value), 0.2)

    def label(self, label):
        if isinstance(label, str) and 40 >= len(label):
            self.__console.print("Label '{}' is OK".format(label), 0.2)
            return True

        self.__console.print("Label '{}' is NOT OK".format(label), 0.2)

    def tile_type(self, tile_type):
        if isinstance(tile_type, str) and 40 >= len(tile_type) >= 1:
            tile_type = self.__refactoring.refactor_reverse(tile_type)

            if tile_type in self.__tmng_r.get_tile_templates():
                self.__console.print("Tile type '{}' is OK".format(tile_type), 0.2)
                return True

        self.__console.print("Tile type '{}' is NOT OK".format(tile_type), 0.2)

    def tile_icon(self, icon):
        if isinstance(icon, str) and 40 >= len(icon) >= 3:
            if icon in self.__fmng.list_file_names(path="static/img/icons"):
                self.__console.print("Tile icon '{}' is OK".format(icon), 0.2)
                return True

        self.__console.print("Tile type '{}' is NOT OK".format(icon), 0.2)

    def tile_index(self, slide_index, old_index, new_index):
        if self.slide_index(slide_index=slide_index):
            if isinstance(old_index, int) and old_index >= 0:
                if isinstance(new_index, int) and new_index >= 0:
                    if old_index != new_index:
                        if len(self.__fmng.devices[slide_index][self.__tmng_r.CHILDREN]) > old_index:
                            if len(self.__fmng.devices[slide_index][self.__tmng_r.CHILDREN]) > new_index:
                                self.__console.print(
                                    "Tile indexes 'slide_index: {}; old_index: {}; new_index: {}' are OK".format(
                                        slide_index, old_index, new_index), 0.2)
                                return True
        self.__console.print("Tile indexes 'slide_index: {}; old_index: {}; new_index: {}' are NOT OK".format(slide_index, old_index, new_index), 0.2)

    # Slide
    def slide_index(self, slide_index):
        if isinstance(slide_index, int) and slide_index >= 0:
            if len(self.__fmng.devices) > slide_index:
                self.__console.print("Slide index '{}' is OK".format(slide_index), 0.2)
                return True

        self.__console.print("Slide index '{}' is NOT OK".format(slide_index), 0.2)

    def slide_index_change(self, old_index, new_index):
        if self.slide_index(old_index):
            if self.slide_index(new_index):
                if old_index != new_index:
                    self.__console.print("Index 'old_index: {}; new_index: {}' are OK".format(old_index, new_index), 0.2)
                    return True

        self.__console.print("Index 'old_index: {}; new_index: {}' are NOT OK".format(old_index, new_index), 0.2)

    # Modal
    def modal_item_type(self, modal_type):
        if isinstance(modal_type, str) and 40 >= len(modal_type) >= 1:
            item_type = self.__refactoring.refactor_reverse(modal_type)
            if item_type in self.__tmng_r.get_modal_templates():
                self.__console.print("Modal type '{}' is OK".format(modal_type), 0.2)
                return True

        self.__console.print("Modal type '{}' is NOT OK".format(modal_type), 0.2)

    def modal_item_id(self, modal_id):
        if isinstance(modal_id, str) and 40 >= len(modal_id) >= 6:
            if re.match("^[a-zA-Z0-9-_]+$", modal_id):
                # Check duplicity for items in modals
                for page, page_content in enumerate(self.__fmng.devices):
                    for tile in page_content[self.__tmng_r.CHILDREN]:
                        try:
                            for modal_item in tile[self.__tmng_r.MODAL]:
                                try:
                                    if modal_item[self.__tmng_r.DATA][self.__tmng_r.ID] == modal_id:
                                        self.__console.print("Modal ID '{}' is OK".format(modal_id), 0.2)
                                        return True
                                except Exception:  # Item without data
                                    pass

                        except Exception:  # Tile without modal
                            pass

        self.__console.print("Modal ID '{}' is NOT OK".format(modal_id), 0.2)

    def modal_item_index_change(self, tile_id, old_index, new_index):
        if self.tile_id(tile_id):
            if isinstance(old_index, int) and old_index >= 0:
                if isinstance(new_index, int) and new_index >= 0:
                    if old_index != new_index:
                        for page, page_content in enumerate(self.__fmng.devices):
                            for tile in page_content[self.__tmng_r.CHILDREN]:
                                if tile["data"]["id"] == tile_id:
                                    if len(tile["modal"]) > old_index:
                                        if len(tile["modal"]) > new_index:
                                            self.__console.print("Modal index 'tile_id: {}; old_index: {}; new_index: {}' is OK".format(tile_id, old_index, new_index), 0.2)
                                            return True
                                    break
                            else:
                                continue
                            break

        self.__console.print("Modal index 'tile_id: {}; old_index: {}; new_index: {}' is NOT OK".format(tile_id, old_index, new_index), 0.2)

    def modal_item_index(self, tile_id, item_index):
        tile_content = self.tile_id(tile_id)
        if tile_content:
            if isinstance(item_index, int) and item_index >= 0:
                for page, page_content in enumerate(self.__fmng.devices):
                    for tile in page_content[self.__tmng_r.CHILDREN]:
                        if tile["data"]["id"] == tile_id:
                            if len(tile["modal"]) > item_index:
                                self.__console.print("Modal index 'tile_id: {}; modal_index: {}' is OK".format(tile_id, item_index), 0.2)
                                return tile_content
                            break
                    else:
                        continue
                    break

        self.__console.print("Modal index 'tile_id: {}; modal_index: {}' is NOT OK".format(tile_id, item_index), 0.2)

    def modal_item_value_name(self, tile_id, value_name, item_index):
        tile = self.modal_item_index(tile_id=tile_id, item_index=item_index)
        if tile:
            if isinstance(value_name, str) and 40 >= len(value_name) >= 1:
                modal_value_name = self.__refactoring.refactor_reverse(value_name)

                if modal_value_name in self.__tmng_r.get_modal_template_values(item_type=tile["modal"][item_index]["type"]):
                    self.__console.print("Modal value name '{}' is OK".format(modal_value_name), 0.2)
                    return True

        self.__console.print("Modal value name '{}' is NOT OK".format(value_name), 0.2)
