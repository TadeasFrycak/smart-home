# Basic routes
from init import *


# Socketio
def socketio_login_required(func):
    """
    If current user isn't authenticated, disconnect from request
    :return: wrapped
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()

        else:
            return func(*args, **kwargs)

    return wrapper


def check_args(args, data):
    for arg in args:
        if arg not in data:
            terminal.prevent_hack("Arg " + arg + " is NOT in " + str(data), False)
            return False
        else:
            terminal.prevent_hack("Arg " + arg + " is in " + str(data))

    if len(args) == len(data):
        return True

    else:
        terminal.prevent_hack("Args from SocketIO " + str(data) + " and required args " + str(args) + " are NOT same!")
        return False


BLACKLISTED_BROWSERS = ["msie"]


# Check browser
def check_browser(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        browser = request.user_agent.browser
        if browser in BLACKLISTED_BROWSERS:
            return render_template("error.html", header="Err", message=gettext("Your browser '{}' is not supported. Please download supported browser like Chromium, Firefox, Safari, ...").format(browser))

        else:

            return func(*args, **kwargs)

    return wrapper


def role_required(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            roles = ["lower_controller",    # Sees only tiles
                     "higher_controller",   # Sees modals too
                     "visitor",             # Can control
                     "manager",             # Can edit tiles, modals, ...
                     "administrator",       # Can start client list, blacklist, server settings, ...
                     "owner"]               # Can add/remove rights to users

            if current_user.is_authenticated:
                if roles.index(current_user.role) >= roles.index(role):
                    return func(*args, **kwargs)
        return wrapper
    return decorator


def socketio_prevent_hack(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = args[0]
        except IndexError:
            data = {}

        func_name = func.__name__
        terminal.prevent_hack("Method " + func_name)

        tests = []
        if func_name == "tile_value_rwr" and check_args(args=["tile_id", "value"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.tile_value(data["value"]))

        elif func_name == "tile_index_rwr" and check_args(args=["slide_index", "old_index", "new_index"], data=data):
            tests.append(validator.tile_index(slide_index=data["slide_index"], old_index=data["old_index"],
                                              new_index=data["new_index"]))

        elif func_name == "tile_label_rwr" and check_args(args=["tile_id", "new_label"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.label(data["new_label"]))

        elif func_name == "tile_type_rwr" and check_args(args=["tile_id", "new_type"], data=data):  # TODO not working
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.tile_type(data["new_type"]))

        elif func_name == "tile_icon_rwr" and check_args(args=["tile_id", "new_icon"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.tile_icon(data["new_icon"]))

        elif func_name == "tile_delete" and check_args(args=["tile_id"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))

        # Modal
        elif func_name == "get_normal_modal" and check_args(args=["tile_id", "tab_id"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.tab_id(data["tab_id"]))

        elif (func_name == "get_edit_modal" or func_name == "modal_close") and check_args(args=["tile_id", "tab_id"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.tab_id(data["tab_id"]))

        elif func_name == "get_add_modal" and check_args(args=["slide_index", "tab_id"], data=data):
            tests.append(validator.slide_index(data["slide_index"]))
            tests.append(validator.tab_id(data["tab_id"]))

        elif func_name == "get_settings_modal" and check_args(args=["tab_id"], data=data):
            tests.append(validator.tab_id(data["tab_id"]))

        elif (func_name == "get_client_list_modal" or func_name == "get_user_list_modal") and check_args(args=["tab_id"], data=data):
            tests.append(validator.tab_id(data["tab_id"]))

        elif func_name == "get_android_modal" and check_args(args=["tab_id"], data=data):
            tests.append(validator.tab_id(data["tab_id"]))

        elif func_name == "modal_item_prepend" and check_args(args=["tile_id", "type"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.modal_item_type(data["type"]))

        elif (func_name == "modal_slider" or func_name == "modal_toggle") and check_args(args=["tile_id", "id", "value"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.modal_item_id(data["id"]))
            tests.append(validator.tile_value(data["value"]))

        elif func_name == "modal_item_index" and check_args(args=["tile_id", "old_index", "new_index"], data=data):
            tests.append(validator.modal_item_index_change(tile_id=data["tile_id"], old_index=data["old_index"], new_index=data["new_index"]))

        elif func_name == "modal_item_config" and check_args(args=["tile_id", "value_name", "new_value", "id"], data=data):
            tests.append(validator.modal_item_value_name(tile_id=data["tile_id"], value_name=data["value_name"], item_id=data["id"]))
            tests.append(validator.label(data["new_value"]))

        elif func_name == "modal_item_delete" and check_args(args=["tile_id", "id"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.modal_item_id(modal_id=data["id"]))

        # Slide
        elif func_name == "slide_name_rwr" and check_args(args=["new_name", "index"], data=data):
            tests.append(validator.slide_index(data["index"]))
            tests.append(validator.label(data["new_name"]))

        elif func_name == "slide_index_rwr" and check_args(args=["old_index", "new_index"], data=data):
            tests.append(validator.slide_index_change(old_index=data["old_index"], new_index=data["new_index"]))

        elif func_name == "slide_append" and check_args(args=["slide_index"], data=data):
            tests.append(validator.slide_index(data["slide_index"]))

        elif func_name == "slide_delete" and check_args(args=["index"], data=data):
            tests.append(validator.slide_index(data["index"]))

        # Before refresh
        elif func_name == "edit_change" and check_args(args=["state", "tab_id"], data=data):
            tests.append(validator.edit_change(data["state"]))
            tests.append(validator.tab_id(data["tab_id"]))

        elif func_name == "slide_change" and check_args(args=["slide_index", "tab_id"], data=data):
            tests.append(validator.slide_index(data["slide_index"]))
            tests.append(validator.tab_id(data["tab_id"]))

        # Other
        elif func_name == "reload" and check_args(args=[], data=data):
            pass

        elif func_name == "save_devices" and check_args(args=[], data=data):
            pass

        elif func_name == "show_android_settings" and check_args(args=[], data=data):
            pass

        elif func_name == "user_mode" and check_args(args=["mode"], data=data):
            tests.append(validator.user_mode(mode=data["mode"]))

        else:  # When method isn't defined here or when check_args failed
            tests.append(False)

        # Evaluation
        if all(tests):
            return func(*args, **kwargs)

        else:
            socketio.emit("notify", {"title": gettext("Problem!"),
                                     "message": gettext("Detected wrong SocketIO request!"), "type": "danger",
                                     "delay": 5000}, namespace=app.config["SOCKETIO_NAMESPACE"], broadcast=True)
            # emit("reload")
            # disconnect()
            # TODO
            return None

    return wrapper


# Babel
@babel.localeselector
def get_locale():
    """
    Get best language
    :return: Best language for current user lang
    """
    # TODO timezone + ukládat language do databáze
    return request.accept_languages.best_match(app.config["LANGUAGES"])


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


# Login manager
@lmng.user_loader
def load_user(user_id):
    """
    Load user
    :user_id: user ID
    :return: user
    """

    # Since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# Socketio ping
@socketio.on("my-ping", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def ping():
    emit("my-pong")


# HTTP ping
@app.route("/ping")
def ping_http():
    return "my-pong"


