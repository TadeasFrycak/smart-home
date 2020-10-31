# Modal routes
from routes_tile import *


# Modals
@socketio.on("get_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("higher_controller")
@check_browser
@log_error
# TODO chceme logovat, že si uživatel otevřel modal?
def get_normal_modal(data):
    """
    Get normal modal
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    tile = tmng_r.get_tile(tile_id)
    tab_id = data["tab_id"]

    emit("get_modal_result", {"modal": render_template("modal_normal.html", tile=tile),
                              "graphs": tmng_r.get_modal_graphs(tile_id=tile_id),
                              "daterangepickers": tmng_r.get_modal_daterangepickers(tile_id=tile_id),
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
@log_error
def get_edit_modal(data):
    """
    Get edit modal
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    tile_type = tmng_r.get_tile_type(tile_id)
    tab_id = data["tab_id"]

    emit("get_edit_modal_result",
         {"modal": render_template("modal_edit.html", modal=tmng_r.get_tile(tile_id)[tmng_r.MODAL],
                                   modal_items=tmng_r.get_modal_templates(), mode=current_user.mode,
                                   tile_values=tmng_r.get_tile_template_values(tile_type=tile_type, tile_id=tile_id),
                                   tile_types=tmng_r.get_tile_templates(), tile_type=tile_type, tile_id=tile_id),
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
@log_error
def get_add_modal(data):
    """
    Get add modal
    :param data: data of socketio request
    :return: None
    """

    slide_index = int(data["slide_index"])
    tab_id = data["tab_id"]

    new_tile = default_values.tile()
    tile_type = new_tile["type"]
    tile_html = render_template(fmng.path_join("tiles", tile_type + ".html"), tile=new_tile)
    tile_id = new_tile["data"]["id"]
    fmng.devices[slide_index]["children"].append(new_tile)

    emit("get_add_tile_result", {"tile_html": tile_html, "slide_index": slide_index}, broadcast=True)
    emit("get_add_modal_result", {"modal": render_template("modal_edit.html",
                                                           modal_items=tmng_r.get_modal_templates(),
                                                           tile_values=tmng_r.get_tile_template_values(tile_type=tile_type),
                                                           tile_types=tmng_r.get_tile_templates(), mode=current_user.mode,
                                                           tile_type=tile_type, tile_id=tile_id),
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
@log_error
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
@log_error
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
@log_error
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
@log_error
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


@socketio.on("modal_close", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("lower_controller")
@check_browser
@log_error
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
@log_error
def modal_item_prepend(data):
    """
    Prepend new modal item
    :param data: data of socketio request
    :return: None
    """

    item_type = refactoring.refactor_reverse(data["type"])
    tile_id = data["tile_id"]

    item = tmng_w.append_modal_item(item_type=item_type, tile_id=tile_id)

    emit("modal_item_prepend_result", {"item": render_template("modal_edit/item_values.html", tile_id=tile_id, item=item),
                                       "tile_id": tile_id}, broadcast=True)
    changes_edit_logger.add(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                            message="new '{}' in tile '{}'".format(item_type, tile_id))
    terminal.debug("Prepend modal item {0} to tile {1}".format(item_type, tile_id))


# Modal events
@socketio.on("modal_slider", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("visitor")
@check_browser
@log_error
def modal_slider(data):
    """
    Modal slider event
    :param data: data of socketio request
    :return: None
    """

    item_id = data[tmng_r.ID]
    new_value = data[tmng_r.VALUE]
    tile_id = data[tmng_r.TILE_ID]

    emit("modal_slider_result", {"id": item_id, "tile_id": tile_id, "value": new_value}, broadcast=True,
         include_self=False)
    acom.mqtt_thread.publish(tile_id=tile_id, item_id=item_id, value=new_value)
    tmng_rwr.modal_item_value(tile_id=tile_id, item_id=item_id, item_type="slider", new_value=new_value)
    # TODO log on end and save on end too


@socketio.on("modal_toggle", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("visitor")
@check_browser
@log_error
def modal_toggle(data):
    """
    Modal toggle event
    :param data: data of socketio request
    :return: None
    """

    item_id = data[tmng_r.ID]
    new_value = data[tmng_r.VALUE]
    tile_id = data[tmng_r.TILE_ID]

    emit("modal_toggle_result", {"id": item_id, "tile_id": tile_id, "value": new_value}, broadcast=True,
         include_self=False)
    acom.mqtt_thread.publish(tile_id=tile_id, item_id=item_id, value=new_value)
    tmng_rwr.modal_item_value(tile_id=tile_id, item_id=item_id, item_type="toggle", new_value=new_value)

    changes_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                          message="new value of '{}' from tile '{}' is '{}'".format(item_id, tile_id, new_value))
    terminal.debug("New value of modal toggle (ID: {}) in tile {} is {}".format(item_id, tile_id, str(new_value)))


# TODO zuniverzálnit na jen socketio modal_value
@socketio.on("modal_clockpicker", namespace=app.config["SOCKETIO_NAMESPACE"])
# TODO @socketio_prevent_hack
@socketio_login_required
@role_required("visitor")
@check_browser
@log_error
def modal_toggle(data):
    """
    Modal toggle event
    :param data: data of socketio request
    :return: None
    """

    item_id = data["item_id"]
    new_value = data[tmng_r.VALUE]
    tile_id = data[tmng_r.TILE_ID]
    print(item_id, new_value, tile_id)

    emit("modal_clockpicker_result", {"item_id": item_id, "tile_id": tile_id, "value": new_value}, broadcast=True,
         include_self=False)
    acom.mqtt_thread.publish(tile_id=tile_id, item_id=item_id, value=new_value)
    tmng_rwr.modal_item_value(tile_id=tile_id, item_id=item_id, item_type="clock_picker", new_value=new_value)

    # changes_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
    #                       message="new value of '{}' from tile '{}' is '{}'".format(item_id, tile_id, new_value))
    # terminal.debug("New value of modal toggle (ID: {}) in tile {} is {}".format(item_id, tile_id, str(new_value)))


@socketio.on("modal_daterangepicker", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("visitor")
@check_browser
@log_error
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
@log_error
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


@socketio.on("modal_item_dynamic_value", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
@log_error
def modal_item_value(data):
    """
    Rewrite one of SortableJS modal item dynamic value (like value, label, colour, ...) from edit mode
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    value_name = refactoring.refactor_reverse(data["value_name"])
    new_value = data["new_value"]
    item_index = int(data[INDEX])

    tmng_rwr.modal_item_dynamic_value(new_value=new_value, value_name=value_name, tile_id=tile_id, index=item_index)

    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="new item value '{}' from item '{}' in tile '{}' is '{}'".format(value_name, item_index, tile_id, new_value))
    terminal.debug(f"Change modal item value ({value_name}) in tile (ID: {tile_id}) to {new_value} (item index is {item_index})")


@socketio.on("modal_item_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
@log_error
def modal_item_delete(data):
    """
    Delete SortableJS modal item from edit mode
    :param data: data of socketio request
    :return: None
    """

    tile_id = data[tmng_r.TILE_ID]
    item_index = int(data[INDEX])

    emit("modal_item_delete_result", {"tile_id": tile_id, "index": item_index}, broadcast=True)
    tmng_w.modal_item_delete(index=item_index, tile_id=tile_id)

    changes_edit_logger.remove(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="item '{}' from tile '{}'".format(item_index, tile_id))
    terminal.debug("Delete modal item in tile (ID: {0}) from index {1}".format(tile_id, str(item_index)))
