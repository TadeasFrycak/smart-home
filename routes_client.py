from routes_slide import *


# Client connect/disconnect
@socketio.on("connect", namespace=app.config["SOCKETIO_NAMESPACE"])
# @check_browser
def client_connect():
    """
    Event on browser connect
    :return: None
    """
    if current_user.is_authenticated:
        username = current_user.username
        join_room(username)

    else:
        username = None
    # TODO vlastní logger - clients.log pro logování přístupů ze zařízení na účtě atd.
    clients.add_client(ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr), sid=request.sid,
                       user_agent=request.user_agent, accept_languages=request.accept_languages,
                       package=request.headers.get("X-Requested-With", None), referrer=request.referrer,
                       username=username)

    # TODO Raspbian keyboard
    terminal.client("Connected {0} ({2}; {1})".format(request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                                    str(request.accept_languages), str(request.user_agent.browser)))


@socketio.on("disconnect", namespace=app.config["SOCKETIO_NAMESPACE"])
@check_browser
def client_disconnect():
    """
    Event on browser disconnect
    :return: None
    """

    if current_user.is_authenticated:
        leave_room(current_user.username)

    clients.remove_client(request.sid)
    terminal.client("Disconnected {0} ({2}; {1})".format(request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                                       str(request.accept_languages), str(request.user_agent.browser)))
