import os


class DevelopmentConfig:
    """
    Flask configuration class - set Flask configuration vars
    """

    ENV = "development"
    DEVELOPMENT = True
    TESTING = True
    DEBUG = False

    LANGUAGES = ["cs", "en", "ru", "de"]
    SEND_FILE_MAX_AGE_DEFAULT = 0
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = "R`xk^U+234>a3P&ef5{kagBFk\g,DE`;/g<NwS#,`'K}gfk5p5\&XD.ce;*8_56x"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig:
    """
    Flask configuration class - set Flask configuration vars
    """

    ENV = "production"
    DEVELOPMENT = False
    TESTING = False
    DEBUG = False

    LANGUAGES = ["cs", "en", "ru", "de"]
    SEND_FILE_MAX_AGE_DEFAULT = 0
    TEMPLATES_AUTO_RELOAD = False
    SECRET_KEY = "vzt=<XK74SbPA-vVVhL7Y>98+<L:-92Tc665Qu3</n=brP`[uw*swGgBeKQr\c6&"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
