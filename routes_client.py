from flask_socketio import join_room, leave_room
from routes_slide import *


# Client connect/disconnect
@socketio.on("connect", namespace=app.config["SOCKETIO_NAMESPACE"])
def client_connect():
    """
    Event on browser connect
    :return: None
    """

    if current_user.is_authenticated:
        join_room(current_user.username)

    clients.add_client()
    console.print("Connected {0} ({2}; {1})".format(request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                                    str(request.accept_languages), str(request.user_agent.browser)), 0.3)


@socketio.on("disconnect", namespace=app.config["SOCKETIO_NAMESPACE"])
def client_disconnect():
    """
    Event on browser disconnect
    :return: None
    """

    if current_user.is_authenticated:
        leave_room(current_user.username)

    clients.remove_client()
    console.print("Disconnected {0} ({2}; {1})".format(request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                                       str(request.accept_languages), str(request.user_agent.browser)), 0.3)
