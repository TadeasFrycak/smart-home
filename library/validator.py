import json
import re


class Validator:
    """
    Validator class
    """

    def __init__(self, fmng, tmng_r, refactoring, terminal):
        """
        Init of Validator
        :param fmng: file_manager
        :param tmng_r: template_manager
        """

        self.__fmng = fmng
        self.__tmng_r = tmng_r
        self.__refactoring = refactoring
        self.__terminal = terminal

    def validate_jsons(self):
        """
        Validate JSONs
        :return: True/exception
        """

        # with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.DEVICES_FILE), "r") as f:
        #     json.load(f)
        # TODO kontroly všech ini a JSON souborů (mac_list.json, ...)
        # with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.APP_CONFIG_DIR,
        #                                 self.__fmng.WHITELIST_FILE), "r") as f:
        #     json.load(f)
        #
        # with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.APP_CONFIG_DIR,
        #                                 self.__fmng.BLACKLIST_FILE), "r") as f:
        #     json.load(f)

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
                if device[self.__tmng_r.ID] not in IDs:
                    IDs.append(device[self.__tmng_r.ID])

                else:
                    return device

        # Check duplicity for items in modals
        for page, page_content in enumerate(self.__fmng.devices):
            for device in page_content[self.__tmng_r.CHILDREN]:
                try:
                    IDs = []
                    for modal_item in device[self.__tmng_r.MODAL]:
                        if modal_item[self.__tmng_r.ID] not in IDs:
                            IDs.append(modal_item[self.__tmng_r.ID])

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
                    return tile_content

        self.__terminal.prevent_hack("Tile ID '{}' is NOT OK".format(tile), False)

    def tile_new_id(self, new_id):
        if isinstance(new_id, str) and 40 >= len(new_id) >= 6:
            if re.match("^[a-zA-Z0-9-_]+$", new_id):
                return True

        self.__terminal.prevent_hack("New tile ID '{}' is NOT OK".format(new_id), False)

    def tile_value(self, value):
        if isinstance(value, int) or isinstance(value, dict):
            return True

        self.__terminal.prevent_hack("Value '{}' is NOT OK".format(value), False)

    def label(self, label):
        if isinstance(label, str):
            if 40 >= len(label):
                return True
        else:
            return True

        self.__terminal.prevent_hack("Label '{}' is NOT OK".format(label), False)

    def tile_type(self, tile_type):
        if isinstance(tile_type, str) and 40 >= len(tile_type) >= 1:
            tile_type = self.__refactoring.refactor_reverse(tile_type)

            if tile_type in self.__tmng_r.get_tile_templates():
                return True

        self.__terminal.prevent_hack("Tile type '{}' is NOT OK".format(tile_type), False)

    def tile_icon(self, icon):
        if isinstance(icon, str) and 40 >= len(icon) >= 3:
            if icon in self.__fmng.list_file_names(path="static/img/icons"):
                return True

        self.__terminal.prevent_hack("Tile type '{}' is NOT OK".format(icon), False)

    def tile_index(self, slide_index, old_index, new_index):
        if self.slide_index(slide_index=slide_index):
            if isinstance(old_index, int) and old_index >= 0:
                if isinstance(new_index, int) and new_index >= 0:
                    if old_index != new_index:
                        if len(self.__fmng.devices[slide_index][self.__tmng_r.CHILDREN]) > old_index:
                            if len(self.__fmng.devices[slide_index][self.__tmng_r.CHILDREN]) > new_index:
                                return True
        self.__terminal.prevent_hack("Tile indexes 'slide_index: {}; old_index: {}; new_index: {}' are NOT OK".format(slide_index, old_index, new_index), False)

    # Slide
    def slide_index(self, slide_index):
        if isinstance(slide_index, int) and slide_index >= 0:
            if len(self.__fmng.devices) > slide_index:
                return True

        if not self.__fmng.devices:
            return True

        self.__terminal.prevent_hack("Slide index '{}' is NOT OK".format(slide_index), False)

    def slide_index_change(self, old_index, new_index):
        if self.slide_index(old_index):
            if self.slide_index(new_index):
                if old_index != new_index:
                    return True

        self.__terminal.prevent_hack("Index 'old_index: {}; new_index: {}' are NOT OK".format(old_index, new_index), False)

    # Modal
    def modal_item_type(self, modal_type):
        if isinstance(modal_type, str) and 40 >= len(modal_type) >= 1:
            if modal_type in self.__tmng_r.get_items_config():
                return True

        self.__terminal.prevent_hack("Modal type '{}' is NOT OK".format(modal_type), False)

    def modal_item_id(self, modal_id):
        if isinstance(modal_id, str) and 40 >= len(modal_id) >= 6:
            if re.match("^[a-zA-Z0-9-_]+$", modal_id):
                # Check duplicity for items in modals
                for page, page_content in enumerate(self.__fmng.devices):
                    for tile in page_content[self.__tmng_r.CHILDREN]:
                        try:
                            for modal_item in tile[self.__tmng_r.MODAL]:
                                try:
                                    if modal_item[self.__tmng_r.ID] == modal_id:
                                        return modal_item
                                except KeyError:  # Item without data
                                    pass

                        except KeyError:  # Tile without modal
                            pass

        self.__terminal.prevent_hack("Modal ID '{}' is NOT OK".format(modal_id), False)

    def modal_item_index_change(self, tile_id, old_index, new_index):
        if self.tile_id(tile_id):
            if isinstance(old_index, int) and old_index >= 0:
                if isinstance(new_index, int) and new_index >= 0:
                    if old_index != new_index:
                        for page, page_content in enumerate(self.__fmng.devices):
                            for tile in page_content[self.__tmng_r.CHILDREN]:
                                if tile[self.__tmng_r.ID] == tile_id:
                                    if len(tile["modal"]) > old_index:
                                        if len(tile["modal"]) > new_index:
                                            return True
                                    break
                            else:
                                continue
                            break

        self.__terminal.prevent_hack("Modal index 'tile_id: {}; old_index: {}; new_index: {}' is NOT OK".format(tile_id, old_index, new_index), False)

    def modal_item_index(self, tile_id, item_index):
        tile_content = self.tile_id(tile_id)
        if tile_content:
            if isinstance(item_index, int) and item_index >= 0:
                for page, page_content in enumerate(self.__fmng.devices):
                    for tile in page_content[self.__tmng_r.CHILDREN]:
                        if tile[self.__tmng_r.ID] == tile_id:
                            if len(tile["modal"]) > item_index:
                                return tile_content
                            break
                    else:
                        continue
                    break

        self.__terminal.prevent_hack("Modal index 'tile_id: {}; modal_index: {}' is NOT OK".format(tile_id, item_index), False)

    def modal_item_value_name(self, tile_id, value_name, item_id):
        tile = self.tile_id(tile_id)
        if tile:
            modal = self.modal_item_id(item_id)
            if modal:
                if isinstance(value_name, str) and 40 >= len(value_name) >= 1:
                    modal_item_value_name = self.__refactoring.refactor_reverse(value_name)
                    if modal_item_value_name in self.__tmng_r.get_modal_template_values(item_type=modal["type"])[1]:
                        return True

        self.__terminal.prevent_hack("Modal value name '{}' is NOT OK".format(value_name), False)

    # Before refresh
    def tab_id(self, tab_id):
        if isinstance(tab_id, str):
            try:
                tab_id_float = float(tab_id)
                if 0 <= tab_id_float <= 1:
                    return True
            except Exception:
                pass
        self.__terminal.prevent_hack("Tab ID '{}' is NOT OK".format(tab_id), False)

    def edit_change(self, edit):
        if isinstance(edit, bool) and edit is not None:
            return True
        self.__terminal.prevent_hack("Edit change '{}' is NOT OK".format(edit), False)

    # Other
    def user_mode(self, mode):
        if isinstance(mode, str) and 6 >= len(mode) >= 4:
            return True
        self.__terminal.prevent_hack("User mode '{}' is NOT OK".format(mode), False)
