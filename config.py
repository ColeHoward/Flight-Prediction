from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    # LESS_BIN = './venv/lib/python3.9/site-packages/lessc'
    # Flask-Assets won't bundle our static files while we're running Flask in debug mode.
    # ASSETS_DEBUG = False
    # tell Flask to build our bundles of fin_assets when Flask starts up automatically.
    # ASSETS_AUTO_BUILD = True


class DevConfig(Config):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    FLASK_ENV = 'production'
    TESTING = False
    DEBUG = False
