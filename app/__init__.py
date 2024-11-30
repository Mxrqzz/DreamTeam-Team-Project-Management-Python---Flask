from flask import Flask
from app.routes.routes import bp


def create_app():
    app = Flask(__name__)

    # Configurações da aplicação
    app.secret_key = "GR3VZ3M0D3"
    app.config["SECRET_KEY"] = "73556088"

    # Registra o blueprint
    app.register_blueprint(bp)

    return app
