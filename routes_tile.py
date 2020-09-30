# Tile routes
from routes_auth import *
import json


# Tile rewrites
@socketio.on("tile_value", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def tile_value_rwr(data):
    """
    Rewrite tile value (real value)
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    value = data[tmng_r.VALUE]

    emit("tile_value_result", {tmng_r.TILE_ID: tile_id, tmng_r.VALUE: value}, broadcast=True)
    acom.mqtt_thread.publish(tile_id=tile_id, value=json.dumps(value))
    tmng_rwr.tile_value(new_value=value, tile_id=tile_id)
    console.print("Change tile (ID: {0}) value to {1}".format(tile_id, str(value)))


@socketio.on("tile_id", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def tile_id_rwr(data):
    """
    Rewrite tile ID
    :param data: data of socketio request
    :return: None
    """

    tile_id = data["tile_id"]
    new_id = data["new_id"]

    emit("tile_id_result", {"tile_id": tile_id, "new_id": new_id}, broadcast=True)
    tmng_rwr.tile_id(tile_id=tile_id, new_id=new_id)
    console.print("Change tile ID from {0} to {1}".format(tile_id, str(new_id)))


@socketio.on("tile_index", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def tile_index_rwr(data):
    """
    Rewrite tile index (change index of two tiles)
    :param data: data of socketio request
    :return: None
    """

    old_index = data["old_index"]
    new_index = data["new_index"]
    slide_index = data["slide_index"]

    emit("tile_index_result", {"old_index": old_index, "new_index": new_index, "slide_index": slide_index},
         broadcast=True, include_self=False)
    tmng_rwr.tile_index(old_index=old_index, new_index=new_index, slide_index=slide_index)
    console.print("Change tile index from {0} to {1} on slide {2}".format(str(old_index), str(new_index),
                                                                          str(slide_index)))


@socketio.on("tile_label", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def tile_label_rwr(data):
    """
    Rewrite tile label (name)
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    new_label = data["new_label"]

    emit("tile_label_result", {"tile_id": tile_id, "new_label": new_label}, broadcast=True)
    tmng_rwr.tile_label(tile_id=tile_id, new_label=new_label)
    console.print("Change tile (ID: {0}) label to {1}".format(tile_id, str(new_label)))


@socketio.on("tile_dynamic_value", namespace=app.config["SOCKETIO_NAMESPACE"])  # TODO v nové verzi odstranit
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def tile_dynamic_value_rwr(data):
    """
    Rewrite dynamic value of tile (in the past for example suffix, in the future 3D printer, ...)
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    new_value = data["new_value"]
    value_name = refactoring.refactor_reverse(data["value_name"])

    # TODO refresh celého HTML
    # tmng_rwr.tile_dynamic_value(tile_id=tile_id, new_value=new_value, value_name=value_name)
    console.print("Change tile (ID: {0}) dynamic value {1} to {2}".format(tile_id, value_name, new_value))


@socketio.on("tile_type", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def tile_type_rwr(data):
    """
    Rewrite tile type (value, toggle, ...)
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    old_type = tmng_r.get_tile_type(tile_id=tile_id)
    new_type = refactoring.refactor_reverse(data["new_type"])

    if old_type != new_type:  # Prevent icon blinking (when clicking too times)
        tile = tmng_r.get_tile(tile_id)
        old_tile_values = render_template(fmng.path_join("modal_edit", "tile_values.html"),
                                          tile_values=tmng_r.get_tile_template_values(tile_type=old_type,
                                                                                      tile_id=tile_id))
        new_tile_values = render_template(fmng.path_join("modal_edit", "tile_values.html"),
                                          tile_values=tmng_r.get_tile_template_values(tile_type=new_type,
                                                                                      tile_id=tile_id))

        if old_tile_values == new_tile_values:
            tile_values = None
        else:
            tile_values = new_tile_values

        tmng_rwr.tile_type(new_type=new_type, tile_id=tile_id)
        emit("tile_type_result", {"tile_values": tile_values, "tile_id": tile_id,
                                  "tile_html": render_template(
                                      fmng.path_join("tiles", tmng_r.get_tile_type(tile_id) + ".html"), tile=tile)},
             broadcast=True)
        console.print("Change tile (ID: {0}) type to {1}".format(tile_id, new_type))


@socketio.on("tile_icon", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def tile_icon_rwr(data):
    """
    Rewrite tile icon
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    new_icon = data["new_icon"]

    if tmng_rwr.tile_icon(new_icon=new_icon, tile_id=tile_id):  # Prevent icon blinking (when clicking too times)
        emit("tile_icon_result", {"tile_id": tile_id, "new_icon": "/img/icons/" + new_icon}, broadcast=True)
        console.print("Change tile (ID: {0}) icon to {1}".format(tile_id, new_icon))


# Tile deletes
@socketio.on("tile_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def tile_delete(data):
    """
    Delete tile
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]

    emit("tile_delete_result", {"tile_id": tile_id}, broadcast=True)
    tmng_w.tile_delete(tile_id=tile_id)
    console.print("Delete tile (ID: {0})".format(tile_id))
