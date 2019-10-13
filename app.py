from flask import Flask, render_template, request
from library.file_manager import FileManager
from library.template_manager import TemplateManager
import socket

fmng = FileManager()
tmng = TemplateManager(fmng)

app = Flask(__name__)

print(socket.gethostbyname(socket.gethostname()))


@app.route("/")
def index():
    tmng.reload_files() # TODO only for now
    return tmng.index()


@app.route("/get_modal", methods=["POST"])
def get_modal():
    return tmng.complete_modal(id=request.form["id"])


@app.route("/io", methods=["POST"])
def io():
    d = request.form["data"]
    return "ok"


if __name__ == "__main__" and bool(fmng.config(overwrite=False)["run"]) is True:
    app.run(host=str(fmng.config(overwrite=False)["host"]), debug=bool(fmng.config(overwrite=False)["debug"]))

else:
    print("Stopped - see config")

