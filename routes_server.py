# Server routes
from flask_login import login_required
from threading import Timer
from routes_client import *
import subprocess
import sys


@app.route("/shutdown", methods=["POST", "GET"])  # TODO to socket
@login_required
@role_required("owner")
def shutdown():
    """
    Shutdown server
    :return: confirmation of server shutdown
    """

    for client in clients.get_clients_sid():
        disconnect(sid=client, namespace=app.config["SOCKETIO_NAMESPACE"])

    # TODO (clean logs, __pycache__, ...) - create for this *.sh file
    print(console.FG_COLORS["cyan"] + console.SPECIAL["bold"] + "I must clean space after me! Wait please..." +
          console.END)
    print(console.FG_COLORS["cyan"] + console.SPECIAL["bold"] + "Server shutdown" + console.END)

    def shutdown_delay():
        subprocess.run(["pkill", "-f", "start.py"])

    timer = Timer(1, shutdown_delay)
    timer.start()

    return render_template("error.html", header=gettext("Shutdown"),
                           message=gettext("Server was successfully shutdown"))


@app.route("/restart", methods=["POST", "GET"])  # TODO to socket
@login_required
@role_required("administrator")
def restart():
    """
    Restart server
    :return: confirmation of server restart - display only if it is GET request
    """
    def restart_delay():
        print(console.FG_COLORS["cyan"] + console.SPECIAL["bold"] + "Server is restarting..." + console.END)
        subprocess.Popen([sys.executable, "run.py"])

    timer = Timer(0.5, restart_delay)
    timer.start()

    return render_template("error.html", header=gettext("Restart"),
                           message=gettext("Server was successfully restarted"))


@socketio.on("reload_all", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("administrator")
def reload():
    """
    Reload page in all opened browsers
    :return: confirmation of browsers reload - display only if it is GET request
    """

    emit("reload", broadcast=True)  # Send request to reload page on all browsers
    print(console.FG_COLORS["cyan"] + console.SPECIAL["bold"] + "Server is reloading all active browsers..." +
          console.END)
