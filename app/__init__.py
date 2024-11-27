from flask import Flask
from app.routes.routes import bp

app = Flask(__name__)
app.config['SECRET_KEY'] = '73556088'

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(bp)
    app.secret_key = 'GR3VZ3M0D3'
    
    return app