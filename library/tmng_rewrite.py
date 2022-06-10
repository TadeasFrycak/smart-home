class TemplateManagerRewrite:
    """
    Template manager rewrite class
    """

    # TODO jde to sjednotit, bude dynamická jedna věc a tam bude:
    #  [data][VALUE (z argumentů funkce)] a poté is_in_data, sjednotí se tak všechno

    def __init__(self, fmng, tmng_r, default_items, default_tiles):
        """
        Init of template manager rewrite class
        :param fmng: fmng class
        :param tmng_r: tmng_r class
        """

        self.__fmng = fmng
        self.__tmng_r = tmng_r
        self.__default_items = default_items
        self.__default_tiles = default_tiles

    # Tile
    def tile(self, tile_id, tile):
        """
        Write tile by ID
        :param tile_id: tile ID
        :param tile: tile JSON
        :return: True
        """
        assert isinstance(tile_id, str), "bad type of tile_id"

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get item for current device
            for tile_num, tile_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If device have current id
                if tile_content[self.__tmng_r.ID] == tile_id:
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][tile_num] = tile
                    return True

    def tile_index(self, old_index, new_index, slide_index):
        """
        Rewrite tile index
        :param old_index: old index of tile
        :param new_index: new index of tile
        :param slide_index: current slide
        :return:
        """

        self.__fmng.devices[slide_index][self.__tmng_r.CHILDREN].insert(new_index, self.__fmng.devices[slide_index][self.__tmng_r.CHILDREN].pop(old_index))

    def tile_value(self, tile_id, new_value):
        """
        Rewrite tile value (state) - ON, OFF, 0, 50, 100, ...
        :param new_value: value of tile
        :param tile_id: id of tile
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    # if isinstance(new_value, dict) and isinstance(item_content[self.__tmng_r.VALUE], dict):
                    #     for key in new_value.keys():  # TODO není moc dobré
                    #         self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.VALUE][key] = new_value[key]
                    # else:
                    if item_content[self.__tmng_r.VALUE] == new_value:
                        return False
                    else:
                        self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.VALUE] = new_value
                        return True

    def tile_config(self, tile_id, value_name, value):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    # If current icon isn't same
                    if item_content[self.__tmng_r.CONFIG][value_name] != value:
                        self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.CONFIG][value_name] = value
                        return True
                    else:
                        return False

    def tile_protocols_check(self, tile_id, protocols):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    state = None
                    element = None

                    keys = []
                    for i in item_content["protocols"]:
                        keys.append(i["type"])

                    if len(protocols) > len(keys):
                        state = "add"
                        element = set(protocols) - set(keys)

                    elif len(protocols) < len(keys):  # TODO tady má být jen else
                        state = "remove"
                        element = set(keys) - set(protocols)

                    return state, list(element)[0]

    def tile_protocol(self, tile_id, protocol, state, protocol_object):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    if state == "add":
                        current_protocol = protocol_object
                        self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num]["protocols"].append(current_protocol.make_object())
                        return current_protocol.make_full_object()

                    elif state == "remove":
                        for num, i in enumerate(item_content["protocols"]):
                            if i["type"] == protocol:
                                self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num]["protocols"].pop(num)
                                return i["config"]
                    return None

    def tile_protocol_values(self, tile_id, value_name, value, protocol):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    # If current icon isn't same
                    for protocol_num, protocol_content in enumerate(item_content["protocols"]):
                        if protocol_content["type"] == protocol:
                            old = protocol_content["config"].copy()
                            self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num]["protocols"][protocol_num]["config"][value_name] = value
                            return old, self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num]["protocols"][protocol_num]["config"]
                    return False

    def tile_label(self, tile_id, new_label):
        """
        Rewrite tile label
        :param tile_id: ID of tile
        :param new_label: new label
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.LABEL] = new_label
                    return True

    def tile_type(self, tile_id, new_type):
        """
        Rewrite tile type
        :param tile_id: ID of tile
        :param new_type: new type
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    tile_default_instance = self.__default_tiles.get_object(new_type)

                    # Set default values
                    tile_config = tile_default_instance.config
                    tile_value = tile_default_instance.VALUE

                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num]["type"] = new_type
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num]["value"] = tile_value
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num]["config"] = tile_config

                    return True

    # Modal states
    def modal_item_value(self, tile_id, item_id, new_value):
        """
        Modal item value rewrite
        :param tile_id: ID of tile
        :param item_id: item ID
        :param new_value: new value
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    # Get modal items
                    for modal_num, modal_item in enumerate(item_content[self.__tmng_r.MODAL]):
                        # If that item is toggle, rewrite
                        if modal_item[self.__tmng_r.ID] == item_id:
                            whole, new = self.__default_items.get_object(modal_item[self.__tmng_r.TYPE]).on_new_value(modal_item[self.__tmng_r.VALUE], new_value)
                            if modal_item[self.__tmng_r.VALUE] == whole:
                                return False
                            else:
                                self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.MODAL][modal_num][self.__tmng_r.VALUE] = whole
                                return new

    def modal_item_index(self, tile_id, old_index, new_index):
        """
        Modal item index
        :param tile_id: tile ID
        :param old_index: old index
        :param new_index: new index
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    # Get modal items
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.MODAL].insert(new_index, self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.MODAL].pop(old_index))
                    return True

    def modal_item_protocols_check(self, tile_id, item_id, protocols):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for tile_num, tile_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                if tile_id == tile_content[self.__tmng_r.ID]:
                    for item_num, item_content in enumerate(tile_content[self.__tmng_r.MODAL]):
                        # If that tile is current opened tile, rewrite
                        if item_content[self.__tmng_r.ID] == item_id:
                            state = None
                            element = None

                            keys = []
                            for i in item_content["protocols"]:
                                keys.append(i["type"])

                            if len(protocols) > len(keys):
                                state = "add"
                                element = set(protocols) - set(keys)

                            elif len(protocols) < len(keys):  # TODO tady má být jen else
                                state = "remove"
                                element = set(keys) - set(protocols)

                            return state, list(element)[0]

    def modal_item_protocol(self, tile_id, item_id, protocol, state, protocol_object):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for tile_num, tile_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if tile_content[self.__tmng_r.ID] == tile_id:
                    for item_num, item_content in enumerate(tile_content[self.__tmng_r.MODAL]):
                        if item_content[self.__tmng_r.ID] == item_id:
                            if state == "add":
                                add_object = protocol_object.make_object()
                                self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][tile_num]["modal"][item_num]["protocols"].append(add_object)
                                return add_object["config"]

                            elif state == "remove":
                                for num, i in enumerate(item_content["protocols"]):
                                    if i["type"] == protocol:
                                        self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][tile_num]["modal"][item_num]["protocols"].pop(num)
                                        return i["config"]
                            return None

    def modal_item_protocol_values(self, tile_id, item_id, value_name, value, protocol):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for tile_num, tile_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if tile_content[self.__tmng_r.ID] == tile_id:
                    for item_num, item_content in enumerate(tile_content[self.__tmng_r.MODAL]):
                        if item_content[self.__tmng_r.ID] == item_id:
                            for protocol_num, protocol_content in enumerate(item_content["protocols"]):
                                if protocol_content["type"] == protocol:
                                    old = protocol_content["config"].copy()
                                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][tile_num]["modal"][item_num]["protocols"][protocol_num]["config"][value_name] = value
                                    return old, self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][tile_num]["modal"][item_num]["protocols"][protocol_num]["config"]
                            return False

    def modal_item_config(self, tile_id, new_value, value_name, item_id):
        """
        Modal item dynamic value
        :param tile_id: tile ID
        :param value_name: value name
        :param new_value: new value
        :param item_id: ID of item
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for tile_num, tile_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if tile_content[self.__tmng_r.ID] == tile_id:
                    # Get modal items
                    for item_num, item_content in enumerate(tile_content[self.__tmng_r.MODAL]):
                        if item_content[self.__tmng_r.ID] == item_id:
                            self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][tile_num][self.__tmng_r.MODAL][item_num][self.__tmng_r.CONFIG][value_name] = new_value
                            return True

    # Slide
    def slide_name(self, index, new_name):
        """
        Rewrite slide name
        :param index: index of slide
        :param new_name: new name of slide
        :return:
        """

        self.__fmng.devices[index][self.__tmng_r.NAME] = new_name

    def slide_index(self, old_index, new_index):
        """
        Rewrite slide index
        :param old_index: old index of slide
        :param new_index: new index of slide
        :return: None
        """

        self.__fmng.devices.insert(new_index, self.__fmng.devices.pop(old_index))

    def graph(self, tile_id, data_x, data_y):
        """
        Graph rewrite
        :param tile_id: tile ID
        :param data_x: data x
        :param data_y: data y
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CONFIG]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.ID] == tile_id:
                    for num, i in enumerate(item_content[self.__tmng_r.MODAL]):
                        if i["type"] == "graph":
                            self.__fmng.devices[page_num][self.__tmng_r.CONFIG][item_num][self.__tmng_r.MODAL][num]["data"]["data_x"].append(data_x)
                            self.__fmng.devices[page_num][self.__tmng_r.CONFIG][item_num][self.__tmng_r.MODAL][num]["data"]["data_y"].append(data_y)
                    return True
