from flask import Flask, render_template, request
from library.file_manager import FileManager
from library.template_manager import TemplateManager
import socket

CONTENT = "::content::"

fmng = FileManager()
tmng = TemplateManager()

app = Flask(__name__)

print(socket.gethostbyname(socket.gethostname()))
@app.route("/")
def index():
    return tmng.complete_template(template=fmng.load_file(fmng.path_join(fmng.TEMPLATES_DIR, "index.html"), False), devices=fmng.devices(), items=fmng.items())


@app.route("/get_modal", methods=["POST"])
def rec():
    return tmng.complete_modal(id=request.form["id"], devices=fmng.devices(), items=fmng.items())
    #return """<div id="tile-Modal" class="tile-modal"> <!-- Modal content --> <div class="tile-modal-content"> <span class="close">&times;</span> <div class="modalContent"> <div class="modalHeader">UNDEFINED</div> <hr> <div class="sliderModule" data-id="0"> <span class="sliderModuleLabel">Slider 1</span> <div class="slider" class="hx-slider"></div> </div> <hr> <div class="buttonModule" data-id="toggle4"> <div class="toggle-slider-div">This is a Toggle switch <label class="switch"> <input type="checkbox"> <span class="toggle-slider round"></span> </label> </div> </div> <hr> <div class="graphModul modalModule" data-header="Last Week"> <canvas id="myChart"></canvas> </div> <hr> <div class="dropDownModule modalModule"> <div class="input-field col s12"> <select> <option value="" disabled selected>Choose your color</option> <option value="1">RED</option> <option value="2">GREEN</option> </select> <label>Select your color</label> </div> </div> <hr> <div class="timerModule modalModule"> <div class="modalTimer">Timer Settings Timer <input type="text" class="timepicker"> </div> </div> </div> </div></div>"""

@app.route("/io", methods=["POST"])
def receive():
    d = request.form["data"]
    print(d)
    return "ok"

if __name__ == "__main__" and bool(fmng.config()["run"]) is True:
    app.run(host=str(fmng.config()["host"]), debug=bool(fmng.config()["debug"]))

else:
    print("Stopped - see config")

