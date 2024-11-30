from flask import request, render_template, flash, url_for, redirect, session
from app.database import create_connection, close_connection
from flask_bcrypt import Bcrypt
from app.controllers.user import User
from app.controllers.team import Team
from functools import wraps

#! Instanciando Modulo que vai criptografar as senhas
cripto = Bcrypt()


#! tela inicial
def index():
    return render_template("index.html")


#! Tela de Cadastro
def register():

    if request.method == "POST":

        nome = request.form["nome"]
        username = request.form["username"]
        email = request.form["email"]
        senha = request.form["password"]
        senhaConfirmacao = request.form["confirmPassword"]

        #! Verificando se as senhas são iguais
        if senha != senhaConfirmacao:
            flash("As senhas não coincidem", "error")
            return render_template("register.html")
        senha_hash = cripto.generate_password_hash(senha).decode("utf-8")

        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()
            #! Verificando se o usuario já esta cadastrado no sistema
            cursor.execute("SELECT * FROM usuarios WHERE username =%s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("O nome de usuário já esta sendo utilizado", "error")
                return render_template("register.html")
            #! Verificando se o email já esta cadastrado no sistema
            cursor.execute("SELECT * FROM usuarios WHERE email =%s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Este Email já esta sendo utilizado", "error")
                return render_template("register.html")

        #! Salvando os dados do usuario no banco de dados
        usuario = User(nome, username, email, senha_hash)
        usuario.salvar_dados()

        close_connection(conexao)
        return render_template("login.html")

    return render_template("register.html")


#! Tela login
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["password"]

        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()

            #! Verificando se o email existe no BD
            cursor.execute("SELECT * FROM usuarios WHERE email =%s", (email,))
            user = cursor.fetchone()

            if user:
                if cripto.check_password_hash(user[4], senha):
                    session["user_id"] = user[0]
                    session["user_nome"] = user[1]
                    session["user_username"] = user[2]
                    session["user_email"] = user[3]
                    close_connection(conexao)
                    return redirect(url_for("main.dashboard_route"))
                else:
                    flash("Senha incorreta", "error")

            else:
                flash("E-mail não encontrado", "error")

    return render_template("login.html")


#! Logout
def logout():
    session.clear()
    flash("Desconectado com sucesso", "success")
    return redirect(url_for("main.login_route"))


#! Controle de sessão
def controller_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Você precisa estar logado para acessar essa pagina", "error")
            return redirect(url_for("main.login_route"))
        return f(*args, **kwargs)

    return decorated_function


@controller_session
def dashboard():
    conexao = create_connection()

    convites = []
    quantidade = 0

    if conexao:
        try:
            cursor = conexao.cursor()

            # Consulta para buscar os convites e os detalhes do time e do remetente
            cursor.execute(
                """
                SELECT 
                    convite_equipe.invite_id,
                    convite_equipe.mensagem,
                    convite_equipe.criado,
                    equipes.nome AS equipe_nome,
                    usuarios.nome AS remetente_nome,
                    usuarios.username AS remetente_username
                FROM convite_equipe
                JOIN equipes ON convite_equipe.equipe_id = equipes.id
                JOIN usuarios ON convite_equipe.sender_id = usuarios.id
                WHERE convite_equipe.receiver_id = %s
                AND convite_equipe.status = 'pendente'
                """,
                (session["user_id"],),
            )

            convites = cursor.fetchall()

            # Contando a quantidade de convites pendentes
            quantidade = len(convites)
        except Exception as e:
            print(f"Erro ao processar: {e}")
        finally:
            close_connection(conexao)

    return render_template("dashboard.html", convites=convites, quantidade=quantidade)


#! Tela Equipes
@controller_session
def teams():

    user_id = session["user_id"]
    equipes = Team.listar_equipes(user_id)
    projects = None
    return render_template("team/teams.html", equipes=equipes, projetos=projects)


#! Tela de Criação de Nova Equipe
@controller_session
def create_team():

    if request.method == "POST":

        equipe = request.form["equipe"]
        descricao = request.form["descricao"]
        criador_id = session["user_id"]

        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT nome FROM equipes WHERE nome=%s AND criador_id =%s",
                (equipe, session["user_id"]),
            )
            team = cursor.fetchone()

            if team:
                flash("Você já criou uma equipe com esse nome.", "error")
            else:
                nova_equipe = Team(equipe, descricao, criador_id)
                nova_equipe.criar_equipe()
                flash("Equipe Criada com Sucesso", "success")
                return redirect(url_for("main.teams_route"))

    return render_template("team/create_team.html")


#! Tela da equipe
@controller_session
def team_vision(team_id):

    conexao = create_connection()

    equipe = None
    projetos = None

    if conexao:
        cursor = conexao.cursor()
        # ? Buscando informações da equipe
        cursor.execute("SELECT * FROM equipes WHERE id =%s", (team_id,))
        equipe = cursor.fetchone()

        close_connection(conexao)

    if not equipe:
        flash("Equipe não encontrada", "error")
        return redirect(url_for("main.teams_route"))

    return render_template("team/team_vision.html", equipe=equipe)


#! Convidar Membros para o time
def invite_to_team(team_id):
    if request.method == "POST":
        convidado = request.form["usernameOrEmail"]
        mensagem = request.form.get("mensagem", "")
        equipe_id = team_id

        conexao = create_connection()

        if conexao:
            try:
                cursor = conexao.cursor()
                # ? Buscando informações da equipe
                cursor.execute("SELECT * FROM equipes WHERE id =%s", (team_id,))
                equipe = cursor.fetchone()
                if not equipe:
                    flash("Equipe não encontrada.", "error")
                    return redirect(url_for("main.team_vision_route", team_id=team_id))

                # *Procurando pelo username
                cursor.execute(
                    "SELECT * FROM usuarios WHERE username =%s", (convidado,)
                )
                invited_user = cursor.fetchone()

                if not invited_user:
                    # *Procurando pelo email
                    cursor.execute(
                        "SELECT * FROM usuarios WHERE email =%s", (convidado,)
                    )
                    invited_user = cursor.fetchone()

                if not invited_user:
                    flash("Usuario não encontrado.", "error")
                    return render_template("team/team_vision.html", equipe_id)

                if invited_user[0] == session["user_id"]:
                    flash("Voce nao pode enviar convite para si mesmo.", "error")
                    return render_template("team/team_vision.html", equipe_id)

                # *Verificando se o convite já foi enviado
                cursor.execute(
                    """
                    SELECT * FROM convite_equipe
                    WHERE sender_id = %s AND receiver_id = %s AND equipe_id = %s AND status = 'pendente'
                    """,
                    (session["user_id"], invited_user[0], equipe_id),
                )
                existing_invite = cursor.fetchone()

                if existing_invite:
                    flash("Convite já enviado e está pendente.", "info")
                    return redirect(url_for("main.team_vision_route", team_id=team_id))

                # Criando o convite
                cursor.execute(
                    """
                    INSERT INTO convite_equipe (sender_id, receiver_id, equipe_id, mensagem)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (session["user_id"], invited_user[0], equipe_id, mensagem),
                )
                conexao.commit()
                flash(f"Convite enviado para {convidado}.", "success")
                return redirect(url_for("main.team_vision_route", team_id=team_id))
            except Exception as e:
                flash(f"Erro ao enviar convite {e}", "error")
                return redirect(url_for("main.team_vision_route", team_id=team_id))
            finally:
                conexao.close()


#!Aceitar o convite
def accept_invite(): ...


#!Recusar o convite
def decline_invite():
    if request.method == "POST":
        convite_id = request.form["invite_id"]
        print(f"{convite_id}")
        
    
        if convite_id:
            try:
                conexao = create_connection()
                if conexao:
                    cursor = conexao.cursor()
                    cursor.execute("UPDATE convite_equipe SET status ='recusado' WHERE invite_id=%s",
                                    (convite_id,),
                                )
                    
                    conexao.commit()
                    flash("Convite Recusado", "info")
            except Exception as e:
                flash("Erro ao tentar recusar convite: {e}", "error")
                ...
        else:
            flash("Convite não encontrado ou status invalido", "error")
        ...
    return  render_template("dashboard.html")