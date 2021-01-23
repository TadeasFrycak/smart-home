# Auth routes
from routes_errors import *


# Unauthorized
@lmng.unauthorized_handler
@check_browser
def unauthorized_handler():
    """
    Unauthorized access to @login_required pages
    :return: login/register page
    """

    mode = sun.day_or_night_now()

    return render_template("auth/login.html", background_image=imng.random_background(current_mode=mode), mode=mode,
                           redirect=request.url_rule, registration=fmng.config["default"].getboolean("registrations"))


# Login
@app.route("/login", methods=["POST"])
@check_browser
def login():
    """
    Login all unlogged users
    :return: ok
    """

    # TODO remove this in the future --> look for better solution
    for user in users:
        login_user(user["user"], user["remember"])

    return OK


@socketio.on("login", namespace=app.config["SOCKETIO_NAMESPACE"])
@check_browser
# TODO prevent heck, kontrolovat stejný regex
def login_socketio(data):
    """
    Login user
    :param data: data of socketio request
    :return: None
    """

    ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    mac = clients.get_mac_from_ip(ip=ip)

    username = data["username"].strip().lower()  # TODO v uživatelském poli půjde zadat pouze malými písmeny +PHACK
    password = data["password"]
    remember = data["remember"]

    user = User.query.filter_by(username=username).first()
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not user.check_password(password):
        auth_logger.wrong_login(username=username, message="IP {0}; MAC {1}; Agent {2}".format(ip, mac, request.user_agent))
        emit("login_result", {"status": False})
        emit("notify", {"title": "Login", "message": "Username or password is wrong!", "type": "danger", "delay": 5000})

    else:
        auth_logger.login(username=username, message="IP {0}; MAC {1}; Agent {2}".format(ip, mac, request.user_agent))
        users.append({"user": user, "remember": remember})
        login_user(user=user, remember=remember)
        emit("login_result", {"status": True})


# Logout
@app.route("/logout")
# @login_required
@check_browser
def logout():
    """
    Logout current user
    :return: None
    """

    if current_user.is_authenticated:
        user = {"first_name": current_user.first_name, "last_name": current_user.last_name,
                "username": current_user.username}

        mode = sun.get_mode(current_user.mode)
        background = current_user.background

        ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
        mac = clients.get_mac_from_ip(ip=ip)
        auth_logger.logout(username=current_user.username, message="IP {0}; MAC {1}; Agent {2}".format(ip, mac, request.user_agent))

        logout_user()
        return render_template("auth/logout.html", user=user, background_image=imng.random_background(current_mode=mode, background=background),
                               mode=mode)
    else:
        return abort(404)


@socketio.on("register", namespace=app.config["SOCKETIO_NAMESPACE"])
@check_browser
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
            emit("notify", {"title": "Error", "message": "Username is already taken!", "type": "danger", "delay": 5000})

        else:
            new_user = User(first_name=first_name, last_name=last_name, username=username)
            new_user.set_password(password)

            database.session.add(new_user)  # Add the new user to the database
            database.session.commit()

            emit("register_result", {"status": True})
    else:
        pass  # TODO tady je to hacker


@socketio.on("user_mode", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
@socketio_prevent_hack
@check_browser
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


@socketio.on("user_background", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
# TODO @socketio_prevent_hack
@check_browser
def user_background(data):
    """
    Change current user background
    :param data: data of socketio request
    :return: None
    """
    background = data["background"]

    user = User.query.filter_by(username=current_user.username).first()
    user.background = background
    database.session.commit()
    emit("user_background_result", {"background": background}, room=current_user.username)


# TODO remove this after GUI
@app.route("/role/<role>")
@check_browser
def change_role(role):
    user = User.query.filter_by(username=current_user.username).first()
    user.role = role
    database.session.commit()
    return redirect("/")
