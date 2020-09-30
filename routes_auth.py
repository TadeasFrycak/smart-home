# Auth routes
from flask_login import login_user, logout_user
from getmac import get_mac_address
from flask import abort, redirect
from routes_errors import *


# Unauthorized
@lmng.unauthorized_handler
def unauthorized_handler():
    """
    Unauthorized access to @login_required pages
    :return: login/register page
    """

    ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

    if server_ip == ip:
        mac = get_mac_address(hostname="localhost")
    else:
        mac = get_mac_address(ip=ip)

    mac_list = fmng.mac_list
    mode = sun.day_or_night_now()

    if mac not in mac_list:
        mac_list.append(mac)
        fmng.mac_list = mac_list

        return render_template("auth/register.html", background_image=imng.random_background(bg_type=mode),
                               mode=mode, introduction=fmng.config["default"].getboolean("introduction"),
                               redirect=request.url_rule)

    else:
        return render_template("auth/login.html", background_image=imng.random_background(bg_type=mode), mode=mode,
                               redirect=request.url_rule, registration=fmng.config["default"].getboolean("registrations"),
                               browser=request.user_agent.browser)


# Login
@app.route("/login", methods=["POST"])
def login():
    """
    Login all unlogined users
    :return: ok
    """

    # TODO remove this in the future --> look for better solution
    for user in users:
        print(login_user(user["user"], user["remember"]))

    return OK


@socketio.on("login", namespace=app.config["SOCKETIO_NAMESPACE"])
def login_socketio(data):
    """
    Login user
    :param data: data of socketio request
    :return: None
    """

    ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

    if server_ip == ip:
        mac = get_mac_address(hostname="localhost")
    else:
        mac = get_mac_address(ip=ip)

    username = data["username"].strip().lower()
    password = data["password"]
    remember = data["remember"]

    user = User.query.filter_by(username=username).first()
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not user.check_password(password):
        auth_logger.warning(
            "Wrong login! User '{0}' from IP '{1}' with MAC '{2}' and header '{3}'".format(username, ip, mac,
                                                                                           request.user_agent))
        emit("login_result", {"status": False})

    else:
        auth_logger.debug("Login on user '{0}' on IP '{1}' with MAC '{2}' and header '{3}'".format(username, ip, mac,
                                                                                                   request.user_agent))
        users.append({"user": user, "remember": remember})
        login_user(user=user, remember=remember)
        emit("login_result", {"status": True})


# Logout
@app.route("/logout")
def logout():
    """
    Logout current user
    :return: None
    """
    if current_user.is_authenticated:
        user = {"first_name": current_user.first_name, "last_name": current_user.last_name,
                "username": current_user.username}

        mode = sun.get_mode(current_user.mode)

        logout_user()
        return render_template("auth/logout.html", user=user, background_image=imng.random_background(bg_type=mode),
                               mode=mode)
    else:
        abort(404)


# Register
@app.route("/register")
def register():
    """
    Register page
    :return: register/404
    """

    if current_user.is_authenticated or fmng.config["default"].getboolean("registrations") is False:
        abort(404)

    else:
        mode = sun.day_or_night_now()
        return render_template("auth/register.html", background_image=imng.random_background(bg_type=mode), mode=mode,
                               redirect="/")


@socketio.on("register", namespace=app.config["SOCKETIO_NAMESPACE"])
def register_socketio(data):
    """
    Register user
    :param data: data of socketio request
    :return: None
    """

    if fmng.config["default"].getboolean("registrations"):
        first_name = data["first_name"].strip().capitalize()
        last_name = data["last_name"].strip().capitalize()
        username = data["username"].strip().lower()
        password = data["password"]

        # TODO ochrany jako username != heslo apodobně
        # print(prevent_hack.check(first_name=first_name, last_name=last_name, username=username, password=password,
        #                         password_repeat=password_repeat, sex=sex))
        user = User.query.filter_by(username=username).first()  # if returns user, then username already exists in database

        if user:
            emit("register_result", {"status": False})

        else:
            new_user = User(first_name=first_name, last_name=last_name, username=username)
            new_user.set_password(password)

            database.session.add(new_user)  # Add the new user to the database
            database.session.commit()

            emit("register_result", {"status": True})
    else:
        pass  # TODO tady je to hacker


@socketio.on("user_mode", namespace=app.config["SOCKETIO_NAMESPACE"])
# TODO prevent
def user_mode(data):
    """
    Change current user mode
    :param data: data of socketio request
    :return: None
    """

    mode = data["mode"]

    user = User.query.filter_by(username=current_user.username).first()
    user.mode = mode
    database.session.commit()

    emit("user_mode_result", {"mode": sun.get_mode(user_mode=mode)}, room=current_user.username)


@app.route("/role/<role>")
def change_role(role):
    user = User.query.filter_by(username=current_user.username).first()
    user.role = role
    database.session.commit()
    return redirect("/")
