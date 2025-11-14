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
    else:
        emit("notify", {"title": gettext("Info"), "message": gettext("No content to show!"),
                        "type": "info", "delay": 5000})

    join_room(tile_id)

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

    join_room(tile_id)

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
    tile_html = render_template("tiles/tile.html", tile=new_tile)
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

    join_room(tile_id)

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
        all_logs = []
        all_logs.extend(auth_logger.get_user_logs(user.username))
        all_logs.extend(changes_logger.get_user_logs(user.username))
        all_logs.extend(changes_edit_logger.get_user_logs(user.username))
        all_logs.sort()

        prepared_users.append(
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "register_date": user.register_date,
                "role": user.role,
                "mode": user.mode,
                "logs": all_logs
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


