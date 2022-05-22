from flask import Flask
from .prediction import prediction
from .home import home
from .rank import rank
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder="templates",
        static_folder="static"
    )
    # Using a production configuration
    # app.config.from_object('config.ProdConfig')

    # Using a development configuration
    app.config.from_object('config.DevConfig')

    # register blueprints
    app.register_blueprint(home.home_bp)
    app.register_blueprint(prediction.prediction_bp)
    app.register_blueprint(rank.rank_bp)
    # return to wsgi file, so server knows where/what the app is
    return app
