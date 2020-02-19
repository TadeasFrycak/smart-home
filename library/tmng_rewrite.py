class TemplateManagerRewrite:
    def __init__(self, fmng, tmng):
        self.__fmng = fmng
        self.__tmng = tmng

    # Tile
    def tile_id(self, element_id, new_id):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == element_id:
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] = new_id

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
                        self.__tmng.STATUS] = self.__tmng.STATUSES[int(state)]
                    self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                         self.__fmng.CONFIG_DEVICES),
                                              data=self.__fmng.devices(), is_json=True)
                    return True

    def tile_name(self, element_id, new_name):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == element_id:
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.LABEL] = new_name

                    return True

    def tile_type(self, element_id, new_type):
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile, rewrite
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == element_id:
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.TYPE] = self.__tmng.refactor_reverse(new_type)

                    return True

    # Modal states
    def modal_toggle(self, id_tile, state, element_id):
        """
        Rewrite toggle status
        :param id_tile: id of mother tile
        :param state: state of toggle
        :param element_id: toggle id
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
                        # If that item is toggle, rewrite
                        if modal_item[self.__tmng.TYPE] == self.TOGGLE and modal_item[self.__tmng.DATA][self.__tmng.ID] == element_id:
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.MODAL][modal_num][self.VALUE] = state
                            self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                                 self.__fmng.CONFIG_DEVICES),
                                                      data=self.__fmng.devices(), is_json=True)
                            return True

    def modal_slider(self, id_tile, state, element_id):
        """
        Rewrite slider value
        :param id_tile: id of mother tile
        :param state: state of slider
        :param element_id: id of slider
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
                        # If that item is slider rewrite
                        if modal_item[self.__tmng.TYPE] == self.SLIDER and modal_item[self.__tmng.DATA][self.__tmng.ID] == element_id:
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.MODAL][modal_num][self.VALUE] = state
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
        :return:
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
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.MODAL][modal_num][self.__tmng.DATA_X].append(data_x)
                            self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.MODAL][modal_num][self.__tmng.DATA_Y].append(data_y)
                            self.__fmng.write_devices(path=self.__fmng.path_join(self.__fmng.CONFIG_DIR,
                                                                                 self.__fmng.CONFIG_DEVICES),
                                                      data=self.__fmng.devices(), is_json=True)
                            return True

    def modal_item_index(self, tile_id, old_index, new_index):  # TODO tile_id NAPSAT PŘÍRUČKU
        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA]):
                # If that tile is current opened tile
                if self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.DATA][self.__tmng.ID] == tile_id:
                    # Get modal items
                    self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.MODAL].insert(new_index, self.__fmng.devices()[self.__tmng.ITEMS][page_num][self.__tmng.DATA][item_num][self.__tmng.MODAL].pop(old_index))

    # Swiper
    def append_slide(self, index, value):
        """
        Append new slide
        :param index: to index
        :param value: name of page
        :return:
        """

        self.__fmng.devices()[self.__tmng.ITEMS].append({self.NAME: value, self.__tmng.DATA: []})

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
