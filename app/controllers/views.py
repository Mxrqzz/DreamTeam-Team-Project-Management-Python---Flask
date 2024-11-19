from flask import render_template

#! tela inicial
def index():
    return render_template("index.html")