# Main routes
from flask import send_from_directory
from routes_server import *
import time


# TODO class for this
before_refreshes = []


# Index page
@app.route("/")
@login_required
@role_required("lower_controller")
def index():
    """
    Main index page
    :return: index.html page
    """

    probably = []

    if fmng.config["refresh"].getboolean("save"):
        current_ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
        # if server_ip == current_ip:
        #     current_mac = get_mac_address(hostname="localhost")
        # else:
        #     current_mac = get_mac_address(ip=current_ip)
        current_browser = request.user_agent.browser
        # current_browser_version = request.user_agent.version

        for refresh in before_refreshes:
            if (time.time() - refresh["time"]) > fmng.config["refresh"].getint("time"):
                before_refreshes.remove(refresh)

        # TODO nefunguje moc dobře, hlavně pokud je server refresh (obnovit všechny klienty)
        # for num, refresh in enumerate(before_refreshes):
        #     if refresh["device"]["ip"] == current_ip:
        #         if refresh["device"]["mac"] == current_mac:
        #             if refresh["device"]["browser"] == current_browser:
        #                 if refresh["device"]["browser_version"] == current_browser_version:
        #                     if before_refreshes[num]["session"] == request.cookies[app.config["SESSION_COOKIE_NAME"]] or before_refreshes[num]["session"] is None:
        #                         edit = refresh["data"]["edit"]
        #                         slide_index = refresh["data"]["slide_index"]
        #                         tile_id = refresh["data"]["tile_id"]
        #
        #                         before_refreshes[num]["session"] = request.cookies[app.config["SESSION_COOKIE_NAME"]]
        #                         break
        #
        # else:
        #     edit = "false"
        #     slide_index = 0
        #     tile_id = None

        for num, refresh in enumerate(before_refreshes):
            if refresh["device"]["ip"] == current_ip:
                if refresh["device"]["browser"] == current_browser:
                    probably.append({"data": refresh["data"], "tab_id": refresh["device"]["tab_id"]})

    mode = sun.get_mode(user_mode=current_user.mode)

    if request.user_agent.platform == "android":
        x_requested_with = request.headers.get("X-Requested-With")
        if x_requested_with:
            if x_requested_with == "cz.frycak.smarthome":
                return render_template("index.html", slides=fmng.devices, mode=mode, probably=probably,
                                       background_image=imng.random_background(bg_type=mode), android_apk=True)
            else:  # Not my application
                abort(403)
        else:
            return render_template("index.html", slides=fmng.devices, mode=mode, probably=probably,
                                   background_image=imng.random_background(bg_type=mode), android_browser=True)
    else:
        return render_template("index.html", slides=fmng.devices, background_image=imng.random_background(bg_type=mode),
                               mode=mode, probably=probably)

# TODO remove in new version
# @app.route("/android_download")
# def android_download():
#     return send_from_directory(directory="android", filename="Smart-home-v1.0-latest.apk")


# Other
@app.route("/devices")
@login_required
@role_required("administrator")
def devices_return():
    """
    Devices file return
    :return: devices.json file
    """

    return str(fmng.devices)


@socketio.on("save", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def save_devices():
    """
    Save to devices.json
    :return:
    """

    fmng.devices = fmng.devices


@socketio.on("show_android_settings", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@role_required("lower_controller")
# @socketio_prevent_hack TODO přidat do prevent hacku
def show_android_settings():
    ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    acom.mqtt_thread.publish_android(ip)


@socketio.on("before_refresh", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@role_required("lower_controller")
# @socketio_prevent_hack TODO přidat do prevent hacku
def before_refresh(data):
    # TODO screen position (scroll position) - uložit také
    if fmng.config["refresh"].getboolean("save"):
        # ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
        #
        # if server_ip == ip:
        #     mac = get_mac_address(hostname="localhost")
        # else:
        #     mac = get_mac_address(ip=ip)
        #
        # before_refreshes.append({"device": {"ip": ip,
        #                                     "mac": mac,
        #                                     "browser": request.user_agent.browser,
        #                                     "browser_version": request.user_agent.version},
        #                                     # "tab_id": data["tab_id"]},
        #                          "time": time.time(),
        #                          "data": data, "session": None})

        if data["slide_index_change"] is True:
            if int(data["data"]["slide_index"]) == slide_index_change[0]:
                data["data"]["slide_index"] = slide_index_change[1]

            elif int(data["data"]["slide_index"]) == slide_index_change[1]:
                data["data"]["slide_index"] = slide_index_change[0]

        for num, refresh in enumerate(before_refreshes):
            if refresh["device"]["tab_id"] == data["tab_id"]:
                before_refreshes[num]["data"] = data["data"]
                before_refreshes[num]["time"] = time.time()
                break
        else:
            # TODO ukládat i user - menší šance na chybu
            ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
            before_refreshes.append({"device": {"ip": ip,
                                                "browser": request.user_agent.browser,
                                                "tab_id": data["tab_id"]},
                                     "time": time.time(),
                                     "data": data["data"]})


@app.route("/esp/<data>", methods=["GET", "POST"])
def esp(data):
    """
    Cube test
    :return: ok
    """

    socketio.emit("notify", {"title": "Kostka", "message": "Nová pozice: " + data, "type": "warning"},
                  namespace=app.config["SOCKETIO_NAMESPACE"], broadcast=True)
    return OK
