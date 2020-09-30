# Slide routes
from routes_modal import *


# Slide rewrites
@socketio.on("slide_name", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
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
    console.print("Change slide (index: {0}) name to {1}".format(str(slide_index), new_name))


@socketio.on("slide_index", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def slide_index_rwr(data):
    """
    Rewrite slide index (change index of two slides)
    :param data: data of socketio request
    :return: None
    """

    old_index = data["old_index"]
    new_index = data["new_index"]

    slide_index_change[0] = old_index
    slide_index_change[1] = new_index

    emit("slide_index_result", broadcast=True)
    emit("reload", broadcast=True)
    tmng_rwr.slide_index(old_index=old_index, new_index=new_index)
    console.print("Changing slide index from {0} to {1}".format(str(old_index), str(new_index)))


# Slide adds
@socketio.on("slide_append", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def slide_append():
    """
    Append new slide
    :return: None
    """

    emit("slide_append_result", {"slide": render_template("slide.html", slide={"name": tmng_r.UNNAMED})},
         broadcast=True)
    emit("slide_append_animation_result")

    tmng_w.append_slide()
    console.print("Append new slide")


@socketio.on("slide_prepend", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def slide_prepend():
    """
    Prepend new slide
    :return: None
    """

    emit("slide_prepend_result", {"slide": render_template("slide.html", slide={"name": tmng_r.UNNAMED})},
         broadcast=True)
    emit("slide_prepend_animation_result")

    tmng_w.prepend_slide()
    console.print("Prepend new slide")


# Slide deletes
@socketio.on("slide_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@role_required("manager")
def slide_delete(data):
    """
    Delete slide
    :param data: data of socketio request
    :return: None
    """

    slide_index = data[INDEX]

    emit("slide_delete_animation_result")
    emit("slide_delete_result", {"index": slide_index}, broadcast=True)  # TODO když bude na slajdě, udělat taky animaci

    console.print("Delete slide (index: {0})".format(slide_index))
    tmng_w.delete_slide(index=slide_index)
