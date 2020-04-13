# -*- coding: utf-8 -*-

from library.logger import WerkzeugLogger, AuthLogger, ConsoleLogger
from library.tmng_rewrite import TemplateManagerRewrite
from library.default_values import DefaultValues
from library.tmng import TemplateManager
from library.html_json import HTML_JSON
from library.validator import Validator
from library.fmng import FileManager
from library.console import Console
from library.arduino import Arduino
from library.acom import Acom
from library.auth import Auth

from flask import Flask, request, render_template, abort
from flask_socketio import SocketIO
from threading import Thread, Event
from subprocess import Popen

import paho.mqtt.client as mqtt
import subprocess
import datetime
import socket
import random
import json
import time
import sys
import os

try:
    from library.raspberry import Raspberry

except Exception as e:
    pass

# Define constants
OK = "ok"

# Initialise Flask
app = Flask(__name__)
socket_io = SocketIO(app)

# Initialise own modules
fmng = FileManager()
werkzeug_logger = WerkzeugLogger(priority=fmng.config()["werkzeug_priority"])
auth_logger = AuthLogger(priority=fmng.config()["auth_priority"])
console_logger = ConsoleLogger(priority=fmng.config()["console_priority"])
console = Console(logger=console_logger, priority=fmng.config()["console_priority"], socket_io=socket_io)
default_values = DefaultValues()
tmng = TemplateManager(fmng=fmng, console=console, default_values=default_values)
tmng_rwr = TemplateManagerRewrite(fmng=fmng, tmng=tmng, default_values=default_values)
arduino = Arduino(console=console)
html_json = HTML_JSON()
auth = Auth(fmng=fmng, logger=auth_logger)
validator = Validator(fmng=fmng, tmng=tmng)
acom = Acom(console=console, socket_io=socket_io, arduino=arduino)

try:
    raspberry = Raspberry()

except Exception as e:
    console.print("This device is not a Raspberry! Some\nfunctions may not work correctly!", 1)


# Validate files
validate = validator.validate_jsons()
if validate is not True:
    console.print("Error in JSON due: {0}".format(validate), 2)
    exit()

# Check duplicities
check_duplicity = validator.check_duplicity_ids()
if check_duplicity is not True:
    console.print("Duplicity detected in: {0}".format(check_duplicity), 1)


# Add meta header
@app.after_request
def add_meta(response):
    """
    Add meta to HTMLs - it doesn't cache in Chrome, Safari, ...
    :param response: header
    :return: response
    """

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"

    return response


# Error pages
@app.errorhandler(401)
def access_denied(event):
    """
    401 error
    :param event: event
    :return: error page
    """

    return render_template("error.html", header="401", message=str(event))


@app.errorhandler(403)
def access_denied(event):
    """
    403 error
    :param event: event
    :return: error page
    """

    return render_template("error.html", header="403", message=str(event))


@app.errorhandler(404)
def page_not_found(event):
    """
    404 error
    :param event: event
    :return: error page
    """

    return render_template("error.html", header="404", message=str(event))


@app.errorhandler(410)
def gone(event):
    """
    410 error
    :param event: event
    :return: error page
    """

    return render_template("error.html", header="410", message=str(event))


@app.errorhandler(500)
def internal_server_error(event):
    """
    500 error
    :param event: event
    :return: error page
    """

    return render_template("error.html", header="500", message=str(event))


# Index page
@app.route("/")
def index():
    """
    Render index page
    :return: index page
    """

    slides = tmng.index_content()

    # If whitelist is on
    if bool(fmng.config()["whitelist"]) is True:
        if auth.auth(ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr), browser=request.user_agent.browser,
                     system=request.user_agent.platform, header=request.user_agent):

            return render_template("index.html", content=render_template("slide.html", slides=slides),
                                   background_image=tmng.random_background())

        else:
            abort(403)

    else:
        return render_template("index.html", content=render_template("slide.html", slides=slides),
                               background_image=tmng.random_background())


# Tile
@app.route("/tile", methods=["POST"])
def tile():
    """
    Tile click event
    :return:
    """

    json_data = request.form.to_dict(flat=True)

    element_id = request.form[tmng.ID]
    state = request.form[tmng.VALUE]

    socket_io.emit("tile", {tmng.ID: element_id, tmng.VALUE: state}, namespace="/acom")

    tmng_rwr.tile_status(state=state, element_id=element_id)

    arduino.write(html_json.to_html(json_data=json_data))

    return OK


@app.route("/get_tile", methods=["POST"])
def get_tile():
    """
    Get HTML of tile by ID
    :return: HTML of tile
    """

    tile_id = request.form["tile_id"]
    return json.dumps({tmng.TILE: tmng.get_tile(tile_id=tile_id), tmng.ID: tile_id})


@app.route("/tile_id_rwr", methods=["POST"])
def tile_id_rwr():
    """
    Rewrite tile ID
    :return:
    """

    element_id = request.form["tile_id"]
    new_id = request.form["new_id"]

    tmng_rwr.tile_id(element_id=element_id, new_id=new_id)

    return OK

@app.route("/tile_index_rwr", methods=["POST"])
def tile_index_rwr():
    """
    Rewrite tile ID
    :return:
    """

    old_index = int(request.form["old_index"])
    new_index = int(request.form["new_index"])
    slide = int(request.form["slide"])

    tmng_rwr.tile_index(old_index=old_index, new_index=new_index, slide=slide)

    return OK


@app.route("/tile_name_rwr", methods=["POST"])
def tile_name_rwr():
    """
    Rewrite tile name
    :return:
    """

    element_id = request.form["tile_id"]
    new_name = request.form["new_name"]

    tmng_rwr.tile_name(element_id=element_id, new_name=new_name)

    return OK


@app.route("/tile_type_rwr", methods=["POST"])
def tile_type_rwr():
    """
    Rewrite tile type
    :return:
    """

    element_id = request.form[tmng.ID]
    new_type = request.form[tmng.NEW_TYPE]

    tmng_rwr.tile_type(new_type=new_type, element_id=element_id)

    return json.dumps({"tile_values": tmng.get_tile_values(element_id=element_id)})

@app.route("/tile_icon_rwr", methods=["POST"])
def tile_icon_rwr():
    """
    Rewrite tile type
    :return:
    """

    element_id = request.form[tmng.ID]
    new_icon = request.form["new_icon"]

    tmng_rwr.tile_icon(new_icon=new_icon, element_id=element_id)

    return OK


@app.route("/tile_delete", methods=["POST"])
def tile_delete():
    """
    Rewrite tile type
    :return:
    """

    element_id = request.form[tmng.ID]

    tmng_rwr.tile_delete(element_id=element_id)

    return OK


# Modal
@app.route("/get_modal", methods=["POST"])
def get_modal():
    """
    Get modal by ID - if not "add edit" mode
    :return: modal, slider, toggle and graph values, if "edit add" mode, then only modal
    """

    edit = bool(int(request.form[tmng.EDIT]))
    add = bool(int(request.form[tmng.ADD]))

    # If it's "edit add" mode
    if add is not True and edit is not True:
        tile_id = request.form[tmng.ID]

        return json.dumps({"modal": render_template("modal.html", content=tmng.modal_content(element_id=tile_id, edit=edit)),
                           "sliders": tmng.get_modal_sliders(id_tile=tile_id),  # TODO refactor element_id
                           "toggles": tmng.get_modal_toggles(id_tile=tile_id),
                           "graphs": tmng.get_modal_graphs(id_tile=tile_id)})

    elif add is True:
        page_index = int(request.form[tmng.PAGE_INDEX])

        values = tmng.modal_content(page_index=page_index, edit=edit, add=add)

        return json.dumps({"modal": render_template("modal_edit.html",
                                                    content=values["content"],
                                                    modal_items=values["modal_items"],
                                                    tile_types=values["tile_types"],
                                                    tile_values=values["tile_values"],
                                                    id_value=values["id_value"],
                                                    tile_name=values["tile_name"])})
    elif edit is True and add is not True:
        page_index = int(request.form[tmng.PAGE_INDEX])
        tile_id = request.form[tmng.ID]

        values = tmng.modal_content(page_index=page_index, edit=edit, add=add, element_id=tile_id)

        return json.dumps({"modal": render_template("modal_edit.html",
                                                    content=values["content"],
                                                    modal_items=values["modal_items"],
                                                    tile_types=values["tile_types"],
                                                    tile_values=values["tile_values"],
                                                    id_value=values["id_value"],
                                                    tile_name=values["tile_name"])})

    else:
        print("ERRRORRIHHFALIDSHIRHDSRFHEJKFHADJF")

@app.route("/add_modal_edit_item", methods=["POST"])
def add_modal_edit_item():
    """
    Add new item (like slider or toggle) into modal in edit mode
    :return: HTML of item
    """

    type_of_item = request.form[tmng.TYPE]
    tile_id = request.form[tmng.TILE_ID]

    return json.dumps({"item": tmng.add_modal_edit_item(type_of_item=type_of_item, tile_id=tile_id)})


# Modal events
@app.route("/slider", methods=["POST"])
def slider():
    """
    Slider item event
    :return:
    """

    json_data = request.form.to_dict(flat=True)
    element_id = request.form[tmng.ID]
    state = request.form[tmng.VALUE]
    tile_id = request.form[tmng.TILE_ID]

    tmng_rwr.modal_slider(tile_id=tile_id, state=state, element_id=element_id)
    socket_io.emit("slider", json_data, namespace="/acom")
    arduino.write(html_json.to_html(json_data=json_data))

    return OK


@app.route("/toggle", methods=["POST"])
def toggle():
    """
    Toggle item event
    :return:
    """

    json_data = request.form.to_dict(flat=True)

    element_id = request.form[tmng.ID]
    state = request.form[tmng.VALUE]
    tile_id = request.form[tmng.TILE_ID]

    socket_io.emit("toggle", json_data, namespace="/acom")
    arduino.write(html_json.to_html(json_data=json_data))

    try:
        client = mqtt.Client()
        client.username_pw_set(USER, password=PASSWORD)
        client.connect(BROKER, port=PORT)
        client.publish("{0}/{1}/{2}".format(HOME, str(id_tile), str(element_id)), state)

    except Exception as e:
        pass  # TODO

    # TODO If current tile is Raspberry tile - Make for Raspberry static tile
    if tile_id == "raspberry-1":
        if element_id == "raspberry-cpu-fan":
            raspberry.set_fan(state=int(state))

        elif element_id == "raspberry-save":
            fmng.write_file(fmng.path_join(fmng.CONFIG_DIR, fmng.CONFIG_DEVICES), fmng.devices(), True)
            socket_io.emit("notify", {"title": "Uloženo", "message": "Hodnoty byly úspěšně uloženy",
                                      "type": "success"}, namespace="/acom")

        elif element_id == "raspberry-birds":
            subprocess.check_output(["omxplayer", "birds.mp3"]).decode("utf-8")

        elif element_id == "raspberry-alarm":
            subprocess.check_output(["omxplayer", "alarm.mp3"]).decode("utf-8")

        elif element_id == "raspberry-halt":
            fmng.write_file(fmng.path_join(fmng.CONFIG_DIR, fmng.CONFIG_DEVICES), fmng.devices(), True)
            socket_io.emit("notify", {"title": "Uloženo", "message": "Hodnoty byly úspěšně uloženy",
                                      "type": "success"}, namespace="/acom")
            socket_io.emit("notify", {"title": "Kontaktuji...", "message": "Kontaktuji všechna zařízení...",
                                      "type": "info"}, namespace="/acom")
            time.sleep(3)
            socket_io.emit("notify", {"title": "Vypínání...", "message": "Nebude již možné kontrolovat zařízení",
                                      "type": "danger"}, namespace="/acom")
            subprocess.check_output(["sudo", "halt"]).decode("utf-8")

        return OK

    tmng_rwr.modal_toggle(tile_id=tile_id, state=state, element_id=element_id)

    return OK


# Modal rewrite
@app.route("/modal_item_index_rwr", methods=["POST"])
def modal_item_index_rwr():
    """
    Change order of items in modal (from old_index to new_index)
    :return:
    """

    tile_id = request.form[tmng.ID]
    old_index = int(request.form[tmng.OLD_INDEX])
    new_index = int(request.form[tmng.NEW_INDEX])

    tmng_rwr.modal_item_index(new_index=new_index, old_index=old_index, tile_id=tile_id)

    return OK


@app.route("/modal_item_value_rwr", methods=["POST"])
def modal_item_value_rwr():
    """
    Rewrite any value of item
    :return:
    """

    tile_id = request.form[tmng.TILE_ID]
    old_value = request.form[tmng.OLD_VALUE]
    new_value = request.form[tmng.NEW_VALUE]
    item_index = int(request.form[tmng.INDEX])

    tmng_rwr.modal_item_value(new_value=new_value, old_value=old_value, tile_id=tile_id, index=item_index)

    return OK


@app.route("/modal_item_delete", methods=["POST"])
def modal_item_delete():
    """
    Delete modal item
    :return:
    """

    tile_id = request.form[tmng.TILE_ID]
    item_index = int(request.form[tmng.INDEX])

    tmng_rwr.modal_item_delete(index=item_index, tile_id=tile_id)

    return OK


# Swiper
@app.route("/swiper_title", methods=["POST"])
def swiper_title():
    """
    Change page name
    :return:
    """

    page_index = int(request.form[tmng.INDEX])
    value = request.form[tmng.VALUE]

    tmng.title_rwr(index=page_index, value=value)

    return OK


@app.route("/append_slide", methods=["POST"])
def append_slide():
    """
    Append new slide
    :return:
    """

    tmng_rwr.append_slide()

    return json.dumps({"slide": render_template("slide.html", slides=[{"content": "", "name": "Bez názvu"}])})


@app.route("/remove_slide", methods=["POST"])
def remove_slide():
    """
    Remove current slide (by index)
    :return:
    """

    page_index = int(request.form[tmng.INDEX])

    tmng_rwr.remove_slide(index=page_index)

    return OK


# Client connect/disconnect
@socket_io.on("connect", namespace="/acom")
def client_connect():
    """
    Event on user connect
    :return:
    """

    console.print("Client connected")
    console.print("\t- Client IP: " + str(request.environ.get("HTTP_X_REAL_IP", request.remote_addr)))

    data = subprocess.check_output(["arp", request.environ.get("HTTP_X_REAL_IP", request.remote_addr)]).decode("utf-8")
    for i in data.split(" "):
        if ":" in i:
            console.print("\t- MAC adress: " + str(i))

    console.print("\t- Language: " + str(request.accept_languages))
    console.print("\t- Header: " + str(request.user_agent))
    console.print("\t\t- Browser: " + str(request.user_agent.browser))
    console.print("\t\t- Version: " + str(request.user_agent.version))


@socket_io.on("disconnect", namespace="/acom")
def client_disconnect():
    """
    Event on user discconnect
    :return:
    """

    console.print("Client disconnected")


# Server operations
@app.route("/shutdown", methods=["POST", "GET"])
def shutdown():
    """
    Shutdown server
    :return: confirmation of server shutdown
    """

    werkzeug_shutdown = request.environ.get("werkzeug.server.shutdown")

    if werkzeug_shutdown is None:
        console.print("Not running with the Werkzeug Server", 2)

    werkzeug_shutdown()  # Shutdown server

    return render_template("error.html", header="Vypnuto", message="Server byl úspěšně vypnut")


@app.route("/restart", methods=["POST", "GET"])
def restart():
    """
    Restart server
    :return: confirmation of server restart - display only if it is GET request
    """

    Popen([sys.executable, "app.py"])  # Open new app.py

    werkzeug_shutdown = request.environ.get("werkzeug.server.shutdown")

    if werkzeug_shutdown is None:
        console.print("Not running with the Werkzeug Server", 2)

    werkzeug_shutdown()  # Shutdown current server

    return render_template("error.html", header="Restart", message="Server byl úspěšně restartován")


@app.route("/reload", methods=["POST", "GET"])
def reload():
    """
    Reload page in all opened browsers
    :return: confirmation of browsers reload - display only if it is GET request
    """

    socket_io.emit("reload", {}, namespace="/acom")  # Send acom request to reload page on all browsers

    return render_template("error.html", header="Reload", message="Všechny webové prohlížeče práve obnovili svoje stránky s Chytrou domácností")


app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # TODO Turn off cashing - not working
os.environ["WERKZEUG_RUN_MAIN"] = "true"  # Turn off first Werkzeug log to console


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("\033[34m\033[1mServer IP address: \033[0m" + s.getsockname()[0] + ":5000")
    s.close()

except Exception as e:
    print("\033[32m127.0.0.1")

# Run whole application
if __name__ == "__main__" and bool(fmng.config()["run"]) is True:
    app.run(host=str(fmng.config()["host"]), debug=bool(fmng.config()["debug"]))

else:
    console.print("Stopped - see config", 2)
