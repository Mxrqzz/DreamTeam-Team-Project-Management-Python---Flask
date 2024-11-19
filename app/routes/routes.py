from flask import Blueprint
from app.controllers.views import index

bp = Blueprint("main", __name__)

@bp.route("/")
@bp.route("/index")
def index_route():
    return index()