from flask import Blueprint
from app.controllers.views import *

bp = Blueprint("main", __name__)

@bp.route("/")
@bp.route("/index")
def index_route():
    return index()

@bp.route("/register", methods=["GET", "POST"])
def register_route():
    return register()

@bp.route("/login", methods= ["GET", "POST"])
def login_route():
    return login()

@bp.route("/dashboard", methods= ["GET"])
def dashboard_route():
    return dashboard()
