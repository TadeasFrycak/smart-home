# Server routes
from routes_client import *


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
