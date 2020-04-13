class TemplateManagerRewrite:
    """
    Template manager rewrite class
    """

    def __init__(self, fmng, tmng, default_values):
        """
        Init of template manager rewrite class
        :param fmng: fmng class
        :param tmng: tmng class
        """

        self.__fmng = fmng
        self.__tmng = tmng
        self.__default_values = default_values

    # Tile
    def tile_index(self, old_index, new_index, slide):
        """
        Rewrite tile index
        :param old_index: old index of tile
        :param new_index: new index of tile
        :param slide: current slide
        :return:
        """

        self.__fmng.devices()[self.__tmng.ITEMS][slide][self.__tmng.DATA].insert(new_index, self.__fmng.devices()[
            self.__tmng.ITEMS][slide][self.__tmng.DATA].pop(old_index))

    def tile_id(self, element_id, new_id):
        """
        Rewrite tile ID
        :param element_id: old element ID
        :param new_id: new element ID
        :return:
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == element_id:
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][
                        self.__tmng.ID] = new_id

    def tile_status(self, state, element_id):
        """
        Rewrite tile status
        :param state: state of tile
        :param element_id: id of tile
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == element_id:
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][
                        self.__tmng.STATUS] = state
                    self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                         self.__fmng.CONFIG_DEVICES),
                                              data=self.__fmng.devices(), is_json=True)

                    return True

    def tile_icon(self, new_icon, element_id):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][
                        self.__tmng.ID] == element_id:
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][
                        "img_src"] = self.__fmng.path_join(self.__tmng.ICON_PATH, new_icon)
                    self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                         self.__fmng.CONFIG_DEVICES),
                                              data=self.__fmng.devices(), is_json=True)

                    return True

    def tile_name(self, element_id, new_name):
        """
        Rewrite tile name
        :param element_id: element ID
        :param new_name:  new name
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == element_id:
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][
                        self.__tmng.LABEL] = new_name

                    return True

    def tile_type(self, element_id, new_type):
        """
        Rewrite tile type
        :param element_id: element ID
        :param new_type: new type
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == element_id:
                    refactored_type = self.__tmng.refactor_reverse(new_type)
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][
                        self.__tmng.TYPE] = refactored_type

                    for i in self.__fmng.items[self.__tmng.ITEMS]:
                        if i == refactored_type:
                            value_names = []

                            # Get values to replace from tile item in items.json
                            for num, value in enumerate(self.__fmng.items[self.__tmng.ITEMS][i].split(self.__tmng.SEPARATOR)):
                                # If it is not remaining HTML
                                if num % 2 and value not in value_names:
                                    value_names.append(value)

                            # Append default values
                            for j in value_names:
                                try:
                                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][j]

                                except Exception as e:
                                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][j] = self.__default_values.default_tile_value(value_name=j)

                            return True

    def tile_delete(self, element_id):
        """
        Delete tile by ID
        :param element_id: ID of tile
        :return:
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][
                        self.__tmng.ID] == element_id:
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA].pop(item_num)

    # Modal states
    def modal_toggle(self, tile_id, state, element_id):
        """
        Rewrite toggle status
        :param tile_id: id of mother tile
        :param state: state of toggle
        :param element_id: toggle id
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == tile_id:
                    # Get modal items
                    for modal_num, modal_item in enumerate(item_content[self.__tmng.MODAL]):
                        # If that item is toggle, rewrite
                        if modal_item[self.__tmng.TYPE] == self.__tmng.TOGGLE and modal_item[self.__tmng.DATA][self.__tmng.ID] == element_id:
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][
                                self.__tmng.MODAL][modal_num][self.__tmng.VALUE] = state
                            self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                                 self.__fmng.CONFIG_DEVICES),
                                                      data=self.__fmng.devices(), is_json=True)

                            return True

    def modal_slider(self, tile_id, state, element_id):
        """
        Rewrite slider value
        :param tile_id: id of mother tile
        :param state: state of slider
        :param element_id: id of slider
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == tile_id:
                    # Get modal items
                    for modal_num, modal_item in enumerate(item_content[self.__tmng.MODAL]):
                        # If that item is slider rewrite
                        if modal_item[self.__tmng.TYPE] == self.__tmng.SLIDER and modal_item[self.__tmng.DATA][self.__tmng.ID] == element_id:
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][
                                self.__tmng.MODAL][modal_num][self.__tmng.VALUE] = state
                            self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                                 self.__fmng.CONFIG_DEVICES),
                                                      data=self.__fmng.devices(), is_json=True)

                            return True

    def modal_graph(self, id_tile, data_x, data_y, element_id):
        """
        Rewrite graph data
        :param id_tile: ID of graph parent (tile)
        :param data_x: data on X
        :param data_y: data on Y
        :param element_id: ID of current graph
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == id_tile:
                    # Get modal items
                    for modal_num, modal_item in enumerate(item_content[self.MODAL]):
                        # If that item is graph rewrite
                        if modal_item[self.__tmng.TYPE] == self.GRAPH and modal_item[self.__tmng.DATA][self.__tmng.ID] == element_id:
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.MODAL][
                                modal_num][self.__tmng.DATA_X].append(data_x)
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.MODAL][
                                modal_num][self.__tmng.DATA_Y].append(data_y)
                            self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                                 self.__fmng.CONFIG_DEVICES),
                                                      data=self.__fmng.devices(), is_json=True)

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
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == tile_id:
                    # Get modal items
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][
                        self.__tmng.MODAL].insert(new_index,
                                                  self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][
                                                      item_num][self.__tmng.MODAL].pop(old_index))

                    return True

    def modal_item_value(self, tile_id, old_value, new_value, index):
        """
        Modal item value
        :param tile_id: tile ID
        :param old_value: old value
        :param new_value: new value
        :param index: index
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == tile_id:
                    # Get modal items
                    for value in item_content[self.__tmng.MODAL][index][self.__tmng.DATA]:
                        if item_content[self.__tmng.MODAL][index][self.__tmng.DATA][value] == old_value:
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][
                                self.__tmng.MODAL][index][self.__tmng.DATA][value] = new_value

                            return True

    def modal_item_delete(self, tile_id, index):
        """
        Modal item delete
        :param tile_id: tile ID
        :param index: index
        :return: True
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == tile_id:
                    # Get modal items
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][
                        self.__tmng.MODAL].pop(index)
                    return True

    # Swiper
    def append_slide(self):
        """
        Append new slide
        :return:
        """

        self.__fmng.devices()[self.__tmng.ITEMS].append({self.__tmng.NAME: self.__tmng.UNNAMED, self.__tmng.DATA: []})

    def remove_slide(self, index):
        """
        Remove slide
        :param index: index of slide to remove
        :return:
        """

        self.__fmng.devices()[self.__tmng.ITEMS].pop(index)

    def page_title(self, index, value):
        """
        Rewrite tile title
        :param index: index  # TODO What is index?
        :param value: value
        :return:
        """

        self.__fmng.devices()[self.__tmng.ITEMS][index][self.NAME] = value
