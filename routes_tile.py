# Tile routes
from routes_auth import *


# Tile rewrites
@socketio.on("tile_value", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
@check_browser
def tile_value_rwr(data):
    """
    Rewrite tile value (real value)
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    value = data[tmng_r.VALUE]
    tile_publish(tile_id=tile_id, value=value)

    changes_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                          message="tile '{}'s value set to '{}'".format(tile_id, value))
    terminal.debug("Change tile (ID: {0}) value to {1}".format(tile_id, str(value)))


@socketio.on("tile_index", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
@check_browser
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

    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="tile's index on slide '{}' changed from '{}' to '{}'".format(slide_index, old_index, new_index))
    terminal.debug("Change tile index from {0} to {1} on slide {2}".format(str(old_index), str(new_index),
                                                                          str(slide_index)))


@socketio.on("tile_label", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
@check_browser
def tile_label_rwr(data):
    """
    Rewrite tile label (name)
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    new_label = data["new_label"]

    emit("tile_label_result", {"tile_id": tile_id, "new_label": new_label, "tile_only": False}, broadcast=True, include_self=False)
    emit("tile_label_result", {"tile_id": tile_id, "new_label": new_label, "tile_only": True})
    tmng_rwr.tile_label(tile_id=tile_id, new_label=new_label)

    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="tile '{}'s label set to '{}'".format(tile_id, new_label))
    terminal.debug("Change tile (ID: {0}) label to {1}".format(tile_id, str(new_label)))


@socketio.on("tile_type", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
@check_browser
def tile_type_rwr(data):
    """
    Rewrite tile type (value, toggle, ...)
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    old_type = tmng_r.get_tile_type(tile_id=tile_id)
    new_type = data["new_type"]

    old_tile = tmng_r.get_tile(tile_id)

    tiles_config = tmng_r.get_tiles_config()

    old_tile_values = render_template(fmng.path_join("modal_edit", "tile_values.html"),
                                      tile=old_tile,
                                      tile_config=tiles_config,
                                      group="tile-dynamic")

    if old_type != new_type:  # Prevent from icon blinking (when clicking too times)
        tmng_rwr.tile_type(new_type=new_type, tile_id=tile_id)

        tile = tmng_r.get_tile(tile_id)
        tile_values = render_template(fmng.path_join("modal_edit", "tile_values.html"),
                                      tile=tile,
                                      tile_config=tiles_config,
                                      group="tile-dynamic")

        if old_tile_values == tile_values:  # Prevent from sliding up and back down with same content
            tile_values = False

        if tiles_config[new_type]["protocols_able"]:
            tile_protocol_btns = render_template("modal_edit/tile_protocol_btns.html", tile=tile, tile_config=tiles_config, group="tile", protocol_config=get_protocols_config())

        else:
            tile_protocol_btns = False

        # Delete protocols that cannot be in new tile type
        for i in tile["protocols"].copy():
            if i["type"] not in tiles_config[new_type]["protocols_able"]:
                protocols = []
                for j in tile["protocols"]:
                    if i["type"] != j["type"]:
                        protocols.append(j["type"])

                state, new_protocol = tmng_rwr.tile_protocols_check(tile_id=tile_id, protocols=protocols)
                result = tmng_rwr.tile_protocol(tile_id=tile_id, protocol=new_protocol, state=state,
                                                protocol_object=default_protocols.get_object(new_protocol))

                emit("tile_protocol_result",
                     {"tile_id": tile_id, "protocols": protocols, "new_protocol": new_protocol, "state": state,
                      "html": None}, broadcast=True)
                default_protocols.get_object(new_protocol).remove_listener(config=result)

        emit("tile_type_result", {"tile_values": tile_values, "tile_id": tile_id, "type": new_type,
                                  "tile_protocol_btns": tile_protocol_btns,
                                  "tile_html": render_template("tiles/tile.html", tile=tile)},
             broadcast=True)

        changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                                   message="tile '{}' type changed from '{}' to '{}'".format(tile_id, old_type, new_type))
        terminal.debug("Change tile (ID: {0}) type to {1}".format(tile_id, new_type))


@socketio.on("tile_config", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
# TODO @socketio_prevent_hack a odebrat z prevent hacku tile_icon
@role_required("manager")
@check_browser
def tile_config_rwr(data):
    """
    Rewrite tile icon
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    value_name = data["value_name"]
    value = data["value"]

    if tmng_rwr.tile_config(tile_id=tile_id, value_name=value_name, value=value):
        emit("tile_config_result", {"tile_id": tile_id, "value_name": value_name, "value": value}, broadcast=True)

        changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                                   message="tile '{}''s '{}' changed to '{}'".format(tile_id, value_name, value))
        terminal.debug("Change tile (ID: {0}) {2} to {1}".format(tile_id, value, value_name))


@socketio.on("tile_protocol_values", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
# TODO @socketio_prevent_hack a odebrat z prevent hacku tile_icon
@role_required("manager")
@check_browser
def tile_config_rwr(data):
    tile_id = data[tmng_r.TILE_ID]
    protocol = data["protocol"]
    value_name = data["value_name"]
    value = data["value"]

    old_config, new_config = tmng_rwr.tile_protocol_values(tile_id=tile_id, value_name=value_name, value=value, protocol=protocol)
    if new_config:
        emit("tile_protocol_values_result", {"tile_id": tile_id, "value_name": value_name, "value": value, "protocol": protocol}, broadcast=True, include_self=False)

        default_protocols.get_object(protocol).edit_listener(old_config=old_config, new_config=new_config)

        changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                                   message="tile '{}''s protocol 's '{}' changed to '{}'".format(tile_id, value_name, value))
        terminal.debug("Change tile (ID: {0}) {2} to {1}".format(tile_id, value, value_name))


@socketio.on("tile_protocol", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
# TODO @socketio_prevent_hack
@role_required("manager")
@check_browser
def tile_protocol(data):
    tile_id = data[tmng_r.TILE_ID]
    protocols = data["protocols"]

    state, new_protocol = tmng_rwr.tile_protocols_check(tile_id=tile_id, protocols=protocols)
    result = tmng_rwr.tile_protocol(tile_id=tile_id, protocol=new_protocol, state=state, protocol_object=default_protocols.get_object(new_protocol))
    html = None
    if state == "add":
        html = render_template("modal_edit/protocol_values.html",
                               id=tile_id, protocol_config=get_protocols_config(),
                               protocols=tmng_r.get_tile(tile_id)["protocols"],
                               group="protocol-tile",
                               protocol=new_protocol, mode=sun.get_mode(user_mode=current_user.mode))

    emit("tile_protocol_result", {"tile_id": tile_id, "protocols": protocols, "new_protocol": new_protocol, "state": state,
                                  "html": html}, broadcast=True)

    if state == "add":
        default_protocols.get_object(new_protocol).add_listener()

    elif state == "remove":
        default_protocols.get_object(new_protocol).remove_listener(config=result)

    changes_edit_logger.remove(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="tile '{}' protocol '{}' to '{}'".format(tile_id, state, new_protocol))
    terminal.debug("'{1}' protocol of tile (ID: {0}) '{2}'".format(tile_id, state, new_protocol))


# Tile deletes
@socketio.on("tile_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
@check_browser
def tile_delete(data):
    """
    Delete tile
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]

    emit("tile_delete_result", {"tile_id": tile_id}, broadcast=True)

    for protocol in tmng_r.get_protocol(tile_id):
        default_protocols.get_object(protocol["type"]).remove_listener(config=protocol["config"])

    tmng_w.tile_delete(tile_id=tile_id)
    changes_edit_logger.remove(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="tile '{}'".format(tile_id))
    terminal.debug("Delete tile (ID: {0})".format(tile_id))
