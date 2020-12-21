# Server routes
from threading import Timer
from routes_client import *
import signal
import sys


@app.route("/shutdown", methods=["POST"])  # TODO to socket
@login_required
@role_required("owner")
@check_browser
def shutdown():
    """
    Shutdown server
    :return: confirmation of server shutdown
    """

    socketio.emit("shutdown", broadcast=True, namespace=app.config["SOCKETIO_NAMESPACE"])

    for client in clients.get_clients_sid():
        disconnect(sid=client, namespace=app.config["SOCKETIO_NAMESPACE"])

    changes_logger.server(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                          message="now")

    def inner_kill():
        print("ok")
        os.kill(int(sys.argv[1]), signal.SIGUSR1)

    Timer(1, inner_kill).start()

    return OK


@app.route("/restart", methods=["POST"])  # TODO to socket
@login_required
@role_required("administrator")
@check_browser
def restart():
    """
    Restart server
    :return: confirmation of server restart - display only if it is GET request
    """

    socketio.emit("restart", broadcast=True, namespace=app.config["SOCKETIO_NAMESPACE"])

    changes_logger.server(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                          message="now")

    os.kill(int(sys.argv[1]), signal.SIGUSR2)
    return OK


@socketio.on("reload_all", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("administrator")
@check_browser
def reload():
    """
    Reload page in all opened browsers
    :return: confirmation of browsers reload - display only if it is GET request
    """

    emit("reload", broadcast=True)  # Send request to reload page on all browsers
    terminal.print(terminal.FG_COLORS["cyan"] + terminal.SPECIAL["bold"] + "Server is reloading all active browsers..." +
          terminal.END)
