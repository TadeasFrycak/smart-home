from routes_doorbird import *

acom.run()

socketio.run(app=app, host=app.config["HOST"], port=app.config["PORT"], log_output=app.config["LOGGING"])
# Development mode
# if __name__ == "__main__" and fmng.config["default"].getboolean("run"):
#     try:
#         socketio.run(app=app, host=app.config["HOST"], port=app.config["PORT"], log_output=app.config["LOGGING"])
#     except OSError:
#         terminal.error("Please stop the script and wait a while before running it again")

# Production mode
# TODO
# else:
#     terminal.error("Stopped - see server_config")
