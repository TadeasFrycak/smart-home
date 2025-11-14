import time


class Updater:
    def __init__(self, fmng, tmng_r, tmng_rwr, tmng_w, socketio):
        self.__fmng = fmng
        self.__tmng_r = tmng_r
        self.__tmng_rwr = tmng_rwr
        self.__tmng_w = tmng_w
        self.__socketio = socketio

    def tile_value(self, tile_id, value, save=True):
        def send():
            self.__socketio.emit("tile_value_result", {self.__tmng_r.TILE_ID: tile_id, self.__tmng_r.VALUE: value},
                                 namespace="/com")

        if self.__tmng_r.get_tile_type(tile_id=tile_id) == "value":  # TODO
            value = value.copy()
            value["time"] = time.time()

        if save:
            if self.__tmng_rwr.tile_value(new_value=value, tile_id=tile_id):
                send()
                return True
        else:
            send()

    def item_value(self, tile_id, item_id, value, save=True):
        if save:
            new = self.__tmng_rwr.modal_item_value(tile_id=tile_id, item_id=item_id, new_value=value)
            if new:
                self.__socketio.emit("modal_item_value_result", {"tile_id": tile_id, "value": new, "id": item_id},
                                     namespace="/com", room=tile_id)
                return True
        else:
            self.__socketio.emit("modal_item_value_result", {"tile_id": tile_id, "value": value, "id": item_id},
                                 namespace="/com", room=tile_id)

    def __notify(self, title, msg, color, delay=5000):
        self.__socketio.emit("notify", {"title": title,
                                        "message": msg,
                                        "type": color,
                                        "delay": delay}, namespace="/com")

    def error(self, device, msg):
        self.__notify("FAIL - {}".format(device), msg, "danger", 0)

    def warning(self, device, msg):
        self.__notify("WARNING - {}".format(device), msg, "warning", 0)

    def debug(self, device, msg):
        self.__notify("DEBUG - {}".format(device), msg, "info")

    def connection_success(self, device, msg):
        if not msg or msg == "None":
            msg = "Device {} is connected successfully!".format(device)

        self.__notify("New connection - {}".format(device), msg, "success")
