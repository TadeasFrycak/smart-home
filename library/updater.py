import time


class Updater:
    def __init__(self, fmng, tmng_r, tmng_rwr, tmng_w, socketio):
        self.__fmng = fmng
        self.__tmng_r = tmng_r
        self.__tmng_rwr = tmng_rwr
        self.__tmng_w = tmng_w
        self.__socketio = socketio

    def tile_value(self, tile_id, value):
        if self.__tmng_r.get_tile_type(tile_id=tile_id) == "value":  # TODO
            value = value.copy()
            value["time"] = time.time()

        self.__socketio.emit("tile_value_result", {self.__tmng_r.TILE_ID: tile_id, self.__tmng_r.VALUE: value}, namespace="/com", broadcast=True)
        self.__tmng_rwr.tile_value(new_value=value, tile_id=tile_id)

    def item_value(self, tile_id, item_id, value):
        self.__tmng_rwr.modal_item_value(tile_id=tile_id, item_id=item_id, new_value=value)
        self.__socketio.emit("modal_item_value_result", {"tile_id": tile_id, "value": value, "id": item_id},
                             namespace="/com", broadcast=True)
