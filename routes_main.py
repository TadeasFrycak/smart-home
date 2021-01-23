# Main routes
from routes_server import *


# Index page
@app.route("/")
@login_required
@role_required("lower_controller")
@check_browser
def index():
    """
    Main index page
    :return: index.html page
    """

    probably = refresh_clients.get_data(ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                        browser=request.user_agent.browser, username=current_user.username)
    mode = sun.get_mode(user_mode=current_user.mode)

    android_apk = None
    android_browser = None

    if request.user_agent.platform == "android":
        x_requested_with = request.headers.get("X-Requested-With")
        if x_requested_with:
            if x_requested_with == "cz.frycak.smarthome":
                android_apk = True
            else:  # Not my application
                return abort(403)
        else:
            android_browser = True
            
    # TODO minify není cesta
    return htmlmin.minify(render_template("index.html", slides=fmng.devices, mode=mode, probably=probably,
                                          background_image=imng.random_background(current_mode=mode, background=current_user.background),
                                          android_apk=android_apk, android_browser=android_browser, doorbird=fmng.config["doorbird"].getboolean("active")),
                          remove_empty_space=True, remove_comments=True, reduce_empty_attributes=True,
                          reduce_boolean_attributes=True, remove_optional_attribute_quotes=True,
                          remove_all_empty_space=True)


@socketio.on("edit_change", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@login_required
@role_required("lower_controller")
@check_browser
def edit_change(data):
    tab_id = data["tab_id"]
    state = data["state"]

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, edit=state, username=current_user.username)

    terminal.debug("Edit mode set to " + str(state))


# Other
@app.route("/devices")
@login_required
@role_required("administrator")
@check_browser
def devices_return():
    """
    Devices file return
    :return: devices.json file
    """

    return str(fmng.devices)


@socketio.on("save", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
def save_devices():
    """
    Save to devices.json
    :return:
    """

    fmng.devices = fmng.devices
    terminal.debug("Devices saved")


@socketio.on("show_android_settings", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@role_required("lower_controller")
@socketio_prevent_hack
@check_browser
def show_android_settings():
    ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    acom.mqtt_thread.publish_android(ip)
    terminal.debug("Showing Android settings")
