from datetime import timedelta
import os


class DevelopmentConfig:
    """
    Flask configuration class - set Flask configuration vars
    """
    HOST = "0.0.0.0"
    PORT = 5000
    LOGGING = False

    ENV = "development"
    DEVELOPMENT = True
    TESTING = True
    DEBUG = False

    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0

    SECRET_KEY = "R`xk^U+234>a3P&ef5{kagBFk\g,DE`;/g<NwS#,`'K}gfk5p5\&XD.ce;*8_56x"

    LANGUAGES = ["cs", "en"]
    BABEL_DEFAULT_LOCALE = "en"

    SQLALCHEMY_DATABASE_URI = "sqlite:///data/database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_NAME = "home-session"
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_HTTPONLY = True

    REMEMBER_COOKIE_NAME = "home-remember"
    REMEMBER_COOKIE_DURATION = timedelta(weeks=20)
    REMEMBER_COOKIE_HTTPONLY = True

    SOCKETIO_COOKIE_NAME = "home-socketio"
    SOCKETIO_NAMESPACE = "/com"


class ProductionConfig:
    """
    Flask configuration class - set Flask configuration vars
    """

    ENV = "production"
    DEVELOPMENT = False
    TESTING = False
    DEBUG = False

    TEMPLATES_AUTO_RELOAD = False
    SECRET_KEY = "vzt=<XK74SbPA-vVVhL7Y>98+<L:-92Tc665Qu3</n=brP`[uw*swGgBeKQr\c6&"

