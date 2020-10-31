class TemplateManagerRewrite:
    """
    Template manager rewrite class
    """

    # TODO jde to sjednotit, bude dynamická jedna věc a tam bude:
    #  [data][VALUE (z argumentů funkce)] a poté is_in_data, sjednotí se tak všechno

    def __init__(self, fmng, tmng_r, default_values):
        """
        Init of template manager rewrite class
        :param fmng: fmng class
        :param tmng_r: tmng_r class
        :param default_values: default values class
        """

        self.__fmng = fmng
        self.__tmng_r = tmng_r
        self.__default_values = default_values

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
                if tile_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
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

    def tile_id(self, tile_id, new_id):
        """
        Rewrite tile ID
        :param tile_id: old ID of tile
        :param new_id: new ID of tile
        :return:
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.DATA][self.__tmng_r.ID] = new_id
                    return True

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
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    if isinstance(new_value, dict) and isinstance(item_content[self.__tmng_r.VALUE], dict):
                        for key in new_value.keys():  # TODO není moc dobré
                            self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.VALUE][key] = new_value[key]
                    else:
                        self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.VALUE] = new_value
                    return True

    def tile_icon(self, tile_id, new_icon):
        """
        Rewrite tile icon
        :param tile_id: tile ID
        :param new_icon: new icon
        :return: True/False
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    # If current icon isn't same
                    if self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.DATA]["icon"] != new_icon:
                        self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.DATA]["icon"] = new_icon
                        return True

                    else:
                        # Don't refresh tile
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
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
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
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.TYPE] = new_type
                    value_names = self.__tmng_r.get_tile_template_values(tile_id=tile_id, tile_type=new_type)
                    # Append default values
                    tile_value = self.__default_values.tile_value(value_name="value", tile_type=new_type)

                    if tile_value:
                        self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num]["value"] = tile_value

                    for j in value_names:
                        try:
                            self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.DATA][j]

                        except Exception as e:
                            value = self.__default_values.tile_value(value_name=j, tile_type=new_type)

                            if value:
                                self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.DATA][j] = value

                            else:
                                self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.DATA][j] = self.__tmng_r.UNNAMED

                    return True

    # Modal states
    def modal_item_value(self, tile_id, item_id, item_type, new_value):
        """
        Modal item value rewrite
        :param tile_id: ID of tile
        :param item_id: item ID
        :param item_type: type of modal item
        :param new_value: new value
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    # Get modal items
                    for modal_num, modal_item in enumerate(item_content[self.__tmng_r.MODAL]):
                        # If that item is toggle, rewrite
                        if modal_item[self.__tmng_r.TYPE] == item_type and modal_item[self.__tmng_r.DATA][self.__tmng_r.ID] == item_id:
                            self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.MODAL][modal_num][self.__tmng_r.VALUE] = new_value
                            return True

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
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    # Get modal items
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.MODAL].insert(new_index, self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.MODAL].pop(old_index))
                    return True

    def modal_item_dynamic_value(self, tile_id, new_value, value_name, index):
        """
        Modal item dynamic value
        :param tile_id: tile ID
        :param value_name: value name
        :param new_value: new value
        :param index: index
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    # Get modal items
                    for value in item_content[self.__tmng_r.MODAL][index][self.__tmng_r.DATA]:
                        if value == value_name:
                            self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.MODAL][index][self.__tmng_r.DATA][value] = new_value
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
            for item_num, item_content in enumerate(page_content[self.__tmng_r.DATA]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    for num, i in enumerate(item_content[self.__tmng_r.MODAL]):
                        if i["type"] == "graph":
                            self.__fmng.devices[page_num][self.__tmng_r.DATA][item_num][self.__tmng_r.MODAL][num]["data"]["data_x"].append(data_x)
                            self.__fmng.devices[page_num][self.__tmng_r.DATA][item_num][self.__tmng_r.MODAL][num]["data"]["data_y"].append(data_y)
                    return True
