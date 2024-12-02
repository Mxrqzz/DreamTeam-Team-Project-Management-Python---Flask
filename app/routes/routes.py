from flask import Blueprint
from app.controllers.views import *

bp = Blueprint("main", __name__)

#! Index
@bp.route("/")
@bp.route("/index")
def index_route():
    return index()

#! Register
@bp.route("/register", methods=["GET", "POST"])
def register_route():
    return register()

#! Login
@bp.route("/login", methods=["GET", "POST"])
def login_route():
    return login()

#! Logout
@bp.route("/logout")
def logout_route():
    return logout()

#! Dashboard
@bp.route("/dashboard", methods=["GET"])
def dashboard_route():
    return dashboard()


#! Tela da Equipe
@bp.route("/team_vision/<int:team_id>")
def team_vision_route(team_id):
    return team_vision(team_id)
# equipe
@bp.route("/teams")
def teams_route():
    return teams()

#! Team
@bp.route("/create_team", methods=["GET", "POST"])
def create_team_route():
    return create_team()

#! Convidar Membros para o time
@bp.route("/invite_to_team/<int:team_id>", methods=["POST"])
def invite_to_team_route(team_id):
    return invite_to_team(team_id)

#! Aceitar o convite para equipe
@bp.route("/accept_invite", methods=["POST"])
def accept_invite_route():
    return accept_invite()

#! Recusar o convite para equipe
@bp.route("/decline_invite", methods=["POST"])
def decline_invite_route():
    return decline_invite()

#! Recusar o convite para equipe
@bp.route("/alterar_cargo", methods=["POST"])
def alterar_cargo_route():
    return alterar_cargo()

#! Enviar Mensagem
@bp.route("/adicionar_mensagem/<int:team_id>", methods=["POST"])
def adicionar_mensagem_route(team_id):
    return adicionar_mensagem(team_id)

@bp.route("/criar_projeto/<int:team_id>", methods=["GET", "POST"])
def criar_projeto_route(team_id):
    return create_project(team_id)