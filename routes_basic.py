# Basic routes
from flask_socketio import emit, disconnect
from flask_login import current_user
from flask_babel import gettext
from flask import request
from init import *
import functools


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
            console.print("Arg " + arg + " is NOT in " + str(data), 0.2)
            return False
        else:
            console.print("Arg " + arg + " is in " + str(data), 0.2)

    if len(args) == len(data):
        return True

    else:
        console.print("Args in " + str(data) + " and in " + str(args) + " are NOT same!", 0.2)
        return False


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
        console.print("Method " + func_name, 0.2)

        tests = []
        if func_name == "tile_value_rwr" and check_args(args=["tile_id", "value"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.tile_value(data["value"]))

        elif func_name == "tile_id_rwr" and check_args(args=["tile_id", "new_id"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.tile_new_id(data["new_id"]))

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
        elif func_name == "get_normal_modal" and check_args(args=["tile_id"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))

        elif func_name == "get_edit_modal" and check_args(args=["tile_id"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))

        elif func_name == "get_add_modal" and check_args(args=["slide_index"], data=data):
            tests.append(validator.slide_index(data["slide_index"]))

        elif func_name == "get_settings_modal" and check_args(args=[], data=data):
            pass

        elif func_name == "modal_item_prepend" and check_args(args=["tile_id", "type"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.modal_item_type(data["type"]))

        elif (func_name == "modal_slider" or func_name == "modal_toggle") and check_args(args=["tile_id", "id", "value"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.modal_item_id(data["id"]))
            tests.append(validator.tile_value(data["value"]))

        elif func_name == "modal_daterangepicker" and check_args(args=["tile_id", "start_value", "end_value", "pair_id", "id"], data=data):
            tests.append(validator.tile_id(data["tile_id"]))
            tests.append(validator.modal_item_id(data["id"]))
            tests.append(validator.modal_item_id(data["pair_id"]))
            console.print("Validation is not complete! TODO", 1)
            # TODO (start_value, end_value, pair_id - je třeba vracet clientovi, zda je správná a zobrazovat, jinak err)

        elif func_name == "modal_item_index" and check_args(args=["tile_id", "old_index", "new_index"], data=data):
            tests.append(validator.modal_item_index_change(tile_id=data["tile_id"], old_index=data["old_index"], new_index=data["new_index"]))

        elif func_name == "modal_item_value" and check_args(args=["tile_id", "value_name", "new_value", "index"], data=data):
            tests.append(validator.modal_item_value_name(tile_id=data["tile_id"], value_name=data["value_name"], item_index=data["index"]))
            tests.append(validator.label(data["new_value"]))

        elif func_name == "modal_item_delete" and check_args(args=["tile_id", "index"], data=data):
            tests.append(validator.modal_item_index(tile_id=data["tile_id"], item_index=data["index"]))

        # Slide
        elif func_name == "slide_name_rwr" and check_args(args=["new_name", "index"], data=data):
            tests.append(validator.slide_index(data["index"]))
            tests.append(validator.label(data["new_name"]))

        elif func_name == "slide_index_rwr" and check_args(args=["old_index", "new_index"], data=data):
            tests.append(validator.slide_index_change(old_index=data["old_index"], new_index=data["new_index"]))

        elif (func_name == "slide_append" or func_name == "slide_prepend") and check_args(args=[], data=data):
            pass

        elif func_name == "slide_delete" and check_args(args=["index"], data=data):
            tests.append(validator.slide_index(data["index"]))

        # Other
        elif func_name == "reload" and check_args(args=[], data=data):
            pass

        elif func_name == "save" and check_args(args=[], data=data):
            pass

        else:  # When method isn't defined here or when check_args failed
            tests.append(False)

        # Evaluation
        if all(tests):
            return func(*args, **kwargs)

        else:
            socketio.emit("notify",
                          {"title": "Hacker", "message": gettext("Detected bad SocketIO request!"), "type": "danger"},
                          namespace=app.config["SOCKETIO_NAMESPACE"], broadcast=True)
            # disconnect()
            # TODO
            return None

    return wrapper


# TODO remove in new version
# def slide_index_check(func):
#     @functools.wraps(func)
#     def wrapper(slide_index):
#         try:
#             if validator.slide_index(int(slide_index)):
#                 return func(slide_index)
#             else:
#                 abort(404)
#
#         except Exception:
#             abort(404)
#
#     return wrapper


# Babel
@babel.localeselector
def get_locale():
    """
    Get best language
    :return: Best language for current user lang
    """

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
