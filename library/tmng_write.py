class TemplateManagerWrite:
    """
    Template manager write class
    """

    def __init__(self, tmng_r, tmng_rwr, fmng):
        """
        Init of template manager write class
        :param tmng_r: tmng_r
        :param tmng_rwr: tmng_rwr
        :param fmng: fmng
        """

        self.__fmng = fmng
        self.__tmng_r = tmng_r
        self.__tmng_rwr = tmng_rwr

    # Tile
    def tile_delete(self, tile_id):
        """
        Delete tile by ID
        :param tile_id: ID of tile
        :return: None
        """

        # Get pages (number and content)
        for page_num, page_content in enumerate(self.__fmng.devices):
            # Get tiles (number and content)
            for item_num, item_content in enumerate(page_content[self.__tmng_r.CHILDREN]):
                # If that tile is current opened tile, rewrite
                if item_content[self.__tmng_r.DATA][self.__tmng_r.ID] == tile_id:
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN].pop(item_num)
                    return True

    # Modal
    def modal_item_delete(self, tile_id, index):
        """
        Modal item delete
        :param tile_id: tile ID
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
                    self.__fmng.devices[page_num][self.__tmng_r.CHILDREN][item_num][self.__tmng_r.MODAL].pop(index)
                    return True

    def append_modal_item(self, item_type, tile_id):  # TODO přejmenovat i tenhle request @app.rout(/append...
        """
        Get new SortableJS item in edit modal, send it to JS to show it and save (append) it
        :param item_type: type of item in modal - for example slider, toggle
        :param tile_id: tile ID
        :return: None
        """

        tile = self.__tmng_r.get_tile(tile_id=tile_id)
        item = {self.__tmng_r.TYPE: item_type, "data": self.__tmng_r.get_modal_template_values(item_type=item_type)}
        tile["modal"].insert(0, item)

        self.__tmng_rwr.tile(tile=tile, tile_id=tile_id)
        return item

    # Swiper
    def append_slide(self, slide_index):
        """
        Append new slide
        :return: None
        """

        self.__fmng.devices.insert(slide_index, {self.__tmng_r.NAME: str(self.__tmng_r.UNNAMED), self.__tmng_r.CHILDREN: []})

    def delete_slide(self, index):
        """
        Delete slide
        :param index: index of slide to remove
        :return: None
        """

        self.__fmng.devices.pop(index)
