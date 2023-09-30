from flask import render_template,request,session,redirect,flash
from app_attendward.modelos.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt
from app_attendward import app

bcrypt=Bcrypt(app)

@app.route('/', methods = ['GET'])
def desplegar_login():
    return render_template('login.html')