# Modal routes
from routes_tile import *


# Modals
@socketio.on("get_normal_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("higher_controller")
@check_browser
# TODO chceme logovat, že si uživatel otevřel modal?
def get_normal_modal(data):
    """
    Get normal modal
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    tile = tmng_r.get_display_tile(tile_id)
    tab_id = data["tab_id"]

    if tile["modal"]:
        mode = sun.get_mode(user_mode=current_user.mode)
        emit("get_normal_modal_result", {"modal": render_template("modal_normal.html", tile=tile, mode=mode),
                                  "tile_id": tile_id})

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, modal_id=tile_id, modal_type="normal",
                             username=current_user.username)

    terminal.debug("Opening modal for {0}...".format(tile_id))


@socketio.on("get_edit_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
def get_edit_modal(data):
    """
    Get edit modal
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    tile_type = tmng_r.get_tile_type(tile_id)
    tab_id = data["tab_id"]

    mode = sun.get_mode(user_mode=current_user.mode)

    emit("get_edit_modal_result",
         {"modal": render_template(
             "modal_edit.html",
             tile=tmng_r.get_display_tile(tile_id),
             mode=mode,
             item_config=tmng_r.get_items_config(),
             tile_config=tmng_r.get_tiles_config(),
             protocol_config=get_protocols_config()
         ),
          "tile_id": tile_id})

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, modal_id=tile_id, modal_type="edit",
                             username=current_user.username)

    terminal.debug("Opening edit modal for {0} - tile type is {1}...".format(tile_id, tile_type))


@socketio.on("get_add_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
def get_add_modal(data):
    """
    Get add modal
    :param data: data of socketio request
    :return: None
    """

    slide_index = int(data["slide_index"])
    tab_id = data["tab_id"]

    new_tile = default_tiles.get_default()  # TODO default_values ne! použít nový dynamický!
    tile_type = new_tile["type"]
    tile_html = render_template(fmng.path_join("tiles", tile_type + ".html"), tile=new_tile)
    tile_id = new_tile["id"]
    fmng.devices[slide_index]["children"].append(new_tile)

    mode = sun.get_mode(user_mode=current_user.mode)
    emit("get_add_tile_result", {"tile_html": tile_html, "slide_index": slide_index}, broadcast=True)
    emit("get_edit_modal_result",
         {"modal": render_template(
             "modal_edit.html",
             tile=tmng_r.get_display_tile(tile_id),
             mode=mode,
             item_config=tmng_r.get_items_config(),
             tile_config=tmng_r.get_tiles_config(),
             protocol_config=get_protocols_config()
         ),
             "tile_id": tile_id})

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, modal_id=tile_id, modal_type="edit",
                             username=current_user.username)

    changes_edit_logger.add(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                            message="new tile '{}' on slide '{}'".format(tile_id, slide_index))
    terminal.debug("Opening add modal")


@socketio.on("get_settings_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("lower_controller")
@check_browser
def get_settings_modal(data):
    """
    Get settings modal
    :return: None
    """
    tab_id = data["tab_id"]
    emit("get_settings_modal_result", {"modal": render_template("modal_settings.html", backgrounds=fmng.backgrounds_data, current_background=current_user.background)})

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, modal_type="settings", username=current_user.username)

    terminal.debug("Opening settings modal...")


@socketio.on("get_client_list_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("administrator")
@check_browser
def get_client_list_modal(data):
    tab_id = data["tab_id"]

    emit("get_client_list_modal_result", {"modal": render_template("modal_client_list.html", clients=clients.get_clients())})

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, modal_type="client_list", username=current_user.username)

    terminal.debug("Opening client list modal...")


@socketio.on("get_user_list_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("owner")
@check_browser
def get_user_list_modal(data):
    tab_id = data["tab_id"]

    all_users = User.query.all()
    prepared_users = []

    for user in all_users:
        prepared_users.append(
            {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "register_date": user.register_date,
                "role": user.role,
                "mode": user.mode
            }
        )

    emit("get_user_list_modal_result", {"modal": render_template("modal_user_list.html", users=prepared_users)})

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, modal_type="user_list", username=current_user.username)

    terminal.debug("Opening user list modal...")


@socketio.on("get_android_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("lower_controller")
@check_browser
def get_android_modal(data):
    """
    Get settings modal
    :return: None
    """
    tab_id = data["tab_id"]

    emit("get_android_modal_result", {"modal": render_template("modal_android.html")})

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, modal_type="android", username=current_user.username)

    terminal.debug("Opening Android modal...")


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
        emit("modal_item_protocol_values_result", {"tile_id": tile_id, "id": item_id, "value_name": value_name, "value": value, "protocol": protocol}, broadcast=True, include_self=False)

        changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                                   message="item '{}''s protocol 's '{}' changed to '{}'".format(tile_id, value_name, value))
        terminal.debug("Change item (ID: {0}) {2} to {1}".format(tile_id, value, value_name))

        default_protocols.get_object(protocol).edit_listener(old_config=old_config, new_config=new_config)


@socketio.on("modal_item_protocol", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
# TODO @socketio_prevent_hack
@role_required("manager")
@check_browser
def modal_item_protocol(data):
    tile_id = data[tmng_r.TILE_ID]
    item_id = data[tmng_r.ID]
    new_protocol = data["new_protocol"]
    state = data["state"]

    result = tmng_rwr.modal_item_protocol(tile_id=tile_id, item_id=item_id, protocol=new_protocol, state=state, protocol_object=default_protocols.get_object(new_protocol))
    html = None
    if state == "add":
        html = render_template("modal_edit/protocol_values.html",
                               id=item_id,
                               protocols=tmng_r.get_item(tile_id=tile_id, item_id=item_id)["protocols"],
                               protocol_config=get_protocols_config(),
                               group="protocol-item",
                               protocol=new_protocol)

    emit("modal_item_protocol_result", {"tile_id": tile_id, "id": item_id, "new_protocol": new_protocol, "state": state,
                                        "html": html},
         broadcast=True)

    if state == "add":
        # TODO auto_listener - s argumentem state, ten se pak vevnitř rozhodne, který zavolá - toto samé v tilu
        default_protocols.get_object(new_protocol).add_listener()

    elif state == "remove":
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

    tab_id = data["tab_id"]

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
          "item": render_template(f"items/{item_type}.html", item=item, group="modal-dynamic"),
          "tile_id": tile_id},
         broadcast=True)

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
         broadcast=True, include_self=False)

    item_publish(tile_id=tile_id, item_id=item_id, value=new_value)

    changes_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                          message="new value of '{}' from tile '{}' is '{}'".format(item_id, tile_id, new_value))
    terminal.debug("New value of '{}' from tile '{}' is '{}'".format(item_id, tile_id, str(new_value)))


@socketio.on("modal_daterangepicker", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("visitor")
@check_browser
def daterangepicker(data):
    """
    Daterangepicker event
    :param data: data of socketio request
    :return: None
    """

    # TODO
    terminal.warning("This method is probably not working, TODO")

    item_id = data["tile_id"]
    start_value = data["start_value"]
    end_value = data["end_value"]
    pair_id = data["pair_id"]
    tile_id = data["id"]

    emit("graph_rwr", {"graph_id": pair_id, "value": tmng_r.get_modal_graphs(tile_id=tile_id, item_id=pair_id)},
         broadcast=True)
    tmng_rwr.modal_daterangepicker(tile_id=tile_id, item_id=item_id, item_type="daterangepicker", value={"start": start_value, "end": end_value})

    changes_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                          message="new value of '{}' from tile '{}' is: start '{}'; end '{}'".format(item_id, tile_id, start_value, end_value))
    terminal.debug("New value of modal daterangepicker (ID: {}) in tile {} is: start value {} and end value {}".format(item_id, tile_id, start_value, end_value))


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
         broadcast=True, include_self=False)
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
                                            "id": item_id}, broadcast=True)
    tmng_rwr.modal_item_config(new_value=new_value, value_name=value_name, tile_id=tile_id, item_id=item_id)

    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="new item value '{}' from item '{}' in tile '{}' is '{}'".format(value_name, item_id, tile_id, new_value))
    terminal.debug(f"Change modal item value ({value_name}) in tile (ID: {tile_id}) to {new_value} (item ID is {item_id})")


@socketio.on("modal_item_id", namespace=app.config["SOCKETIO_NAMESPACE"])
# TODO @socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
def modal_item_id(data):
    """
    Rewrite ID of SortableJS modal item from edit mode
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    item_id = data["id"]
    new_id = data["new_id"]

    tmng_rwr.modal_item_id(new_id=new_id, tile_id=tile_id, item_id=item_id)
    emit("modal_item_id_result", {"id": item_id, "new_id": new_id, "tile_id": tile_id}, broadcast=True)
    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="new item ID of item '{}' in tile '{}' is '{}'".format(item_id, tile_id, new_id))
    terminal.debug(f"Change modal item ID in tile (ID: {tile_id}) to {new_id} (item ID is {item_id})")


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

    emit("modal_item_delete_result", {"tile_id": tile_id, "id": item_id}, broadcast=True)

    for protocol in tmng_r.get_protocol(tile_id, item_id):
        default_protocols.get_object(protocol["type"]).remove_listener(config=protocol["config"])

    tmng_w.modal_item_delete(item_id=item_id, tile_id=tile_id)

    changes_edit_logger.remove(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="item '{}' from tile '{}'".format(item_id, tile_id))
    terminal.debug("Delete modal item in tile (ID: {0}) from index {1}".format(tile_id, item_id))
