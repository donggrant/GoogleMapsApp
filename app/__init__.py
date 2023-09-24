from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from . import views
    app.register_blueprint(views.bp)

    return app