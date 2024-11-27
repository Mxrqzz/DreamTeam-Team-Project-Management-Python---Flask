from flask import request, render_template, flash, url_for, redirect, session
from app.database import create_connection, close_connection
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from app.controllers.user import User

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
        senha_hash = cripto.generate_password_hash(senha)

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
            cursor.execute("SELECT & FROM usuarios WHERE email =%s", (email,))
            user = cursor.fetchone()

            if user:
                if check_password_hash(user[4], senha):
                    session["user_id"] = user[0]
                    session["user_nome"] = user[1]
                    session["user_username"] = user[2]
                    session["user_email"] = user[3]
                    return redirect(url_for("main.dashboard"))

    return render_template("login.html")

#! Tela Dashboard
def dashboard():
    return render_template("dashboard.html")
