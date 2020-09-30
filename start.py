from routes_main import *


# Run whole application
if __name__ == "__main__" and fmng.config["default"].getboolean("run"):
    acom.run()
    socketio.run(app=app, host=app.config["HOST"], port=app.config["PORT"], log_output=app.config["LOGGING"])

else:
    console.print("Stopped - see server_config", 2)
