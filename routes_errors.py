# Error routes
from routes_basic import *


@app.errorhandler(401)
def access_denied(event):
    """
    401 error - access denied
    :param event: event
    :return: error.html
    """

    mode = sun.get_mode(user_mode=current_user.mode)
    return render_template("error.html", header=401, message=str(event), mode=mode,
                           background_image=imng.random_background(bg_type=mode, background=current_user.background))


@app.errorhandler(403)
def access_denied(event):
    """
    403 error - access denied
    :param event: event
    :return: error.html
    """

    mode = sun.get_mode(user_mode=current_user.mode)
    return render_template("error.html", header=403, message=str(event), mode=mode,
                           background_image=imng.random_background(bg_type=mode, background=current_user.background))


@app.errorhandler(404)
def page_not_found(event):
    """
    404 error - page not found
    :param event: event
    :return: error.html
    """

    mode = sun.get_mode(user_mode=current_user.mode)
    return render_template("error.html", header=404, message=str(event), mode=mode,
                           background_image=imng.random_background(bg_type=mode, background=current_user.background))


@app.errorhandler(410)
def gone(event):
    """
    410 error - gone
    :param event: event
    :return: error.html
    """

    mode = sun.get_mode(user_mode=current_user.mode)
    return render_template("error.html", header=410, message=str(event), mode=mode,
                           background_image=imng.random_background(bg_type=mode, background=current_user.background))


@app.errorhandler(429)
def internal_server_error(event):
    mode = sun.get_mode(user_mode=current_user.mode)
    return render_template("error.html", header=429, message=str(event), mode=mode,
                           background_image=imng.random_background(bg_type=mode, background=current_user.background))


@app.errorhandler(500)
def internal_server_error(event):
    """
    500 error - internal server error
    :param event: event
    :return: error.html
    """

    mode = sun.get_mode(user_mode=current_user.mode)
    return render_template("error.html", header=500, message=str(event), mode=mode,
                           background_image=imng.random_background(bg_type=mode, background=current_user.background))
