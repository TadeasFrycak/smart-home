# Slide routes
from routes_modal import *


# Slide rewrites
@socketio.on("slide_name", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
@log_error
def slide_name_rwr(data):
    """
    Rewrite slide name from edit mode
    :param data: data of socketio request
    :return: None
    """

    slide_index = int(data[INDEX])
    new_name = data["new_name"]

    emit("slide_name_result", {"slide_index": slide_index, "name": new_name}, broadcast=True, include_self=False)
    tmng_rwr.slide_name(index=slide_index, new_name=new_name)

    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="on index '{}' to '{}'".format(slide_index, new_name))
    terminal.debug("Change slide (index: {0}) name to {1}".format(str(slide_index), new_name))


@socketio.on("slide_index", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
@log_error
def slide_index_rwr(data):
    """
    Rewrite slide index (change index of two slides)
    :param data: data of socketio request
    :return: None
    """

    old_index = data["old_index"]
    new_index = data["new_index"]

    refresh_clients.slide_index_change(old_index=old_index, new_index=new_index)
    emit("slide_index_result", broadcast=True)
    emit("reload", broadcast=True)
    tmng_rwr.slide_index(old_index=old_index, new_index=new_index)

    changes_edit_logger.change(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="from '{}' to '{}'".format(old_index, new_index))
    terminal.debug("Changing slide index from {0} to {1}".format(str(old_index), str(new_index)))


# Slide adds
@socketio.on("slide_append", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
@log_error
def slide_append(data):
    """
    Append new slide to the right
    :return: None
    """

    before_fmng_devices = fmng.devices.copy()

    slide_index = data["slide_index"] + 1
    tmng_w.append_slide(slide_index=slide_index)
    if not before_fmng_devices:
        emit("reload", broadcast=True)
        terminal.debug("Creating first slide")

    else:
        mode = sun.get_mode(user_mode=current_user.mode)
        emit("slide_append_result", {"slide": render_template("slide.html", slide={"name": tmng_r.UNNAMED}, mode=mode),
                                     "slide_index": slide_index}, broadcast=True)
        emit("slide_append_animation_result", {"slide_index": slide_index})

    changes_edit_logger.add(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                            message="to index '{}'".format(slide_index))
    terminal.debug("Append new slide")


# Slide deletes
@socketio.on("slide_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("manager")
@check_browser
@log_error
def slide_delete(data):
    """
    Delete slide
    :param data: data of socketio request
    :return: None
    """

    slide_index = data[INDEX]

    emit("slide_delete_animation_result")
    emit("slide_delete_result", {"index": slide_index}, broadcast=True)  # TODO když bude na slajdě, udělat taky animaci

    terminal.debug("Delete slide (index: {0})".format(slide_index))

    changes_edit_logger.remove(username=current_user.username, func_name=inspect.currentframe().f_code.co_name,
                               message="on index '{}'".format(slide_index))
    tmng_w.delete_slide(index=slide_index)


# On slide change
@socketio.on("slide_change", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_prevent_hack
@socketio_login_required
@role_required("lower_controller")
@check_browser
@log_error
def slide_change(data):
    slide_index = data["slide_index"]
    tab_id = data["tab_id"]

    refresh_clients.set_data(tab_id=tab_id, ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                             browser=request.user_agent.browser, slide=slide_index, username=current_user.username)

    terminal.debug("Slide change")
