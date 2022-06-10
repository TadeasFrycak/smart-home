from routes_modal import *


@socketio.on("modal_item_protocol_values", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
# TODO @socketio_prevent_hack a odebrat z prevent hacku tile_icon
@role_required("manager")
@check_browser
def modal_item_protocol_values_rwr(data):
    tile_id = data[tmng_r.TILE_ID]
    item_id = data[tmng_r.ID]
    protocol = data["protocol"]
    value_name = data["value_name"]
    value = data["value"]

    old_config, new_config = tmng_rwr.modal_item_protocol_values(tile_id=tile_id, value_name=value_name, value=value, protocol=protocol, item_id=item_id)

    if new_config:
        emit("modal_item_protocol_values_result", {"tile_id": tile_id, "id": item_id, "value_name": value_name, "value": value, "protocol": protocol}, broadcast=True, include_self=False, room=tile_id)

        changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                                   message="item '{}''s protocol 's '{}' changed to '{}'".format(tile_id, value_name, value))
        terminal.debug("Change item (ID: {0}) {3} {2} to {1}".format(item_id, value, value_name, protocol))

        default_protocols.get_object(protocol).edit_listener(old_config=old_config, new_config=new_config)


@socketio.on("modal_item_protocol", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
# TODO @socketio_prevent_hack
@role_required("manager")
@check_browser
def modal_item_protocol(data):
    tile_id = data[tmng_r.TILE_ID]
    item_id = data[tmng_r.ID]
    protocols = data["protocols"]

    state, new_protocol = tmng_rwr.modal_item_protocols_check(tile_id=tile_id, item_id=item_id, protocols=protocols)
    result = tmng_rwr.modal_item_protocol(tile_id=tile_id, item_id=item_id, protocol=new_protocol, state=state, protocol_object=default_protocols.get_object(new_protocol))
    html = None
    if state == "add":
        html = render_template("modal_edit/protocol_values.html",
                               id=item_id,
                               protocols=tmng_r.get_item(tile_id=tile_id, item_id=item_id)["protocols"],
                               protocol_config=get_protocols_config(),
                               group="protocol-item-" + item_id,
                               protocol=new_protocol, mode=sun.get_mode(user_mode=current_user.mode))

    emit("modal_item_protocol_result", {"tile_id": tile_id, "id": item_id, "protocols": protocols, "new_protocol": new_protocol, "state": state,
                                        "html": html},
         broadcast=True, room=tile_id)

    if state == "add":
        print("Adding")
        print(result)
        print("==")
        # TODO auto_listener - s argumentem state, ten se pak vevnitř rozhodne, který zavolá - toto samé v tilu
        default_protocols.get_object(new_protocol).add_listener(config=result)

    elif state == "remove":
        print("REMOVING")
        print(result)
        print("==")
        # TODO auto_listener - s argumentem state, ten se pak vevnitř rozhodne, který zavolá - toto samé v tilu
        default_protocols.get_object(new_protocol).remove_listener(config=result)

    changes_edit_logger.remove(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="tile '{}' protocol '{}' to '{}'".format(tile_id, state, new_protocol))
    terminal.debug("'{1}' protocol of tile (ID: {0}) '{2}'".format(tile_id, state, new_protocol))


@socketio.on("modal_close", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("lower_controller")
@check_browser
def modal_close(data):
    """
    Get settings modal
    :return: None
    """

    tile_id = data["tile_id"]
    tab_id = data["tab_id"]

    for item in tmng_r.get_tile(tile_id)["modal"]:
        default_items.get_object(item["type"]).modal_close()

    leave_room(tile_id)

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, modal_type=False, modal_id=False,
                             username=current_user.username)

    terminal.debug("Modal close")


# Modal adds
@socketio.on("modal_item_prepend", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
def modal_item_prepend(data):
    """
    Prepend new modal item
    :param data: data of socketio request
    :return: None
    """

    item_type = data["type"]
    tile_id = data["tile_id"]

    item = tmng_w.append_modal_item(item_type=item_type, tile_id=tile_id)

    mode = sun.get_mode(user_mode=current_user.mode)
    emit("modal_item_prepend_result",
         {"fieldset": render_template("modal_edit/item_values.html",
                                      tile=tmng_r.get_display_tile(tile_id),
                                      item_config=tmng_r.get_items_config(),
                                      item=item, mode=mode,
                                      group="modal-edit-" + item["id"],
                                      protocol_config=get_protocols_config()),
          "item": render_template(f"items/item.html", item=item, group="modal-dynamic"),
          "tile_id": tile_id},
         broadcast=True, room=tile_id)

    changes_edit_logger.add(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                            message="new '{}' in tile '{}'".format(item_type, tile_id))
    terminal.debug("Prepend modal item {0} to tile {1}".format(item_type, tile_id))


# Modal events
# TODO log on end and save on end too (on slider)
@socketio.on("modal_item_value", namespace=app.config["SOCKETIO_NAMESPACE"])
# TODO @socketio_prevent_hack
@socketio_login_required
@role_required("visitor")
@check_browser
def modal_item_value(data):
    """
    Modal value event
    :param data: data of socketio request
    :return: None
    """

    # TODO sjednotit tmng_r.ID a "id", atd..
    item_id = data[tmng_r.ID]
    new_value = data[tmng_r.VALUE]
    tile_id = data[tmng_r.TILE_ID]

    emit("modal_item_value_result", {"id": item_id, "tile_id": tile_id, "value": new_value},
         broadcast=True, include_self=False, room=tile_id)

    item_publish(tile_id=tile_id, item_id=item_id, value=new_value)

    changes_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                          message="new value of '{}' from tile '{}' is '{}'".format(item_id, tile_id, new_value))
    terminal.debug("New value of '{}' from tile '{}' is '{}'".format(item_id, tile_id, str(new_value)))


# Modal rewrites
@socketio.on("modal_item_index", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
def modal_item_index(data):
    """
    Rewrite SortableJS modal item index from edit mode
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    old_index = int(data["old_index"])
    new_index = int(data["new_index"])

    emit("modal_item_index_result", {"tile_id": tile_id, "old_index": old_index, "new_index": new_index},
         broadcast=True, include_self=False, room=tile_id)
    tmng_rwr.modal_item_index(new_index=new_index, old_index=old_index, tile_id=tile_id)

    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="new item index in tile '{}' changes from '{}' to '{}'".format(tile_id, old_index, new_index))
    terminal.debug("Change modal item index in tile (ID: {0}) from {1} to {2}".format(tile_id, old_index, new_index))


@socketio.on("modal_item_config", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
def modal_item_config(data):
    """
    Rewrite one of SortableJS modal item config value (like label, colour, ...) from edit mode
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    value_name = refactoring.refactor_reverse(data["value_name"])
    new_value = data["new_value"]
    item_id = data["id"]

    emit("modal_item_config_result", {"tile_id": tile_id, "value_name": value_name, "new_value": new_value,
                                      "id": item_id, "preview_only": False}, broadcast=True, include_self=False, room=tile_id)
    emit("modal_item_config_result", {"tile_id": tile_id, "value_name": value_name, "new_value": new_value,
                                      "id": item_id, "preview_only": True})

    tmng_rwr.modal_item_config(new_value=new_value, value_name=value_name, tile_id=tile_id, item_id=item_id)

    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="new item value '{}' from item '{}' in tile '{}' is '{}'".format(value_name, item_id, tile_id, new_value))
    terminal.debug(f"Change modal item value ({value_name}) in tile (ID: {tile_id}) to {new_value} (item ID is {item_id})")


@socketio.on("modal_item_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
def modal_item_delete(data):
    """
    Delete SortableJS modal item from edit mode
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    item_id = data["id"]

    emit("modal_item_delete_result", {"tile_id": tile_id, "id": item_id}, broadcast=True, room=tile_id)

    for protocol in tmng_r.get_protocol(tile_id, item_id):
        default_protocols.get_object(protocol["type"]).remove_listener(config=protocol["config"])

    tmng_w.modal_item_delete(item_id=item_id, tile_id=tile_id)

    changes_edit_logger.remove(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="item '{}' from tile '{}'".format(item_id, tile_id))
    terminal.debug("Delete modal item in tile (ID: {0}) from index {1}".format(tile_id, item_id))
