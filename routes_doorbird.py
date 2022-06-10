from routes_main import *

# TODO 11.9
# @socketio.on("get_doorbird_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
# # TODO @socketio_prevent_hack
# @socketio_login_required
# @role_required("higher_controller")
# @check_browser
# # TODO chceme logovat, že si uživatel otevřel modal?
# def get_doorbird_modal(data):
#     """
#     Get Doorbird modal
#     :param data: data of socketio request
#     :return: None
#     """
#
#     tab_id = data["tab_id"]
#     mode = sun.get_mode(user_mode=current_user.mode)
#
#     image = doorbird.live_image(resolution="vga")
#     emit("get_doorbird_modal_result", {"modal": render_template("modal_doorbird.html", mode=mode, image=image)})
#
#     refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
#                              browser=request.user_agent.browser, modal_type="doorbird",
#                              username=current_user.username)
#
#     terminal.debug("Opening Doorbird modal")
#
#
# @socketio.on("doorbird_open_door", namespace=app.config["SOCKETIO_NAMESPACE"])
# # TODO @socketio_prevent_hack
# @socketio_login_required
# # @role_required("manager")
# @check_browser
# def doorbird_open_door():
#     doorbird.open_door()
#
#
# @socketio.on("doorbird_light_on", namespace=app.config["SOCKETIO_NAMESPACE"])
# # TODO @socketio_prevent_hack
# @socketio_login_required
# # @role_required("manager")
# @check_browser
# def doorbird_open_door():
#     doorbird.light_on()
#
#
# @socketio.on("doorbird_take_photo", namespace=app.config["SOCKETIO_NAMESPACE"])
# # TODO @socketio_prevent_hack
# @socketio_login_required
# # @role_required("manager")
# @check_browser
# def doorbird_take_photo():
#     doorbird.take_photo()

