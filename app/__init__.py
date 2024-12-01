from flask import Flask



def create_app():
    app = Flask(__name__)

    # Configurações da aplicação
    app.secret_key = "GR3VZ3M0D3"
    app.config["SECRET_KEY"] = "73556088"


    # Inicializar o banco de dados com a aplicaçã

    # Registrar blueprints
    from app.routes.routes import bp
    app.register_blueprint(bp)

    return app
