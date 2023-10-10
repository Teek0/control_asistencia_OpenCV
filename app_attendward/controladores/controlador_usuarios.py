from flask import render_template,request,session,redirect,flash
from app_attendward.modelos.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt
from app_attendward import app

bcrypt=Bcrypt(app)

@app.route('/', methods = ['GET'])
def desplegar_login():
    return render_template('login.html')



@app.route('/crear/usuario', methods = ['POST'])
def nuevo_usuario():
    #validaciones
    data = {
        **request.form
    }
    usuario_existe=Usuario.obtener_uno_con_email(data)
    if Usuario.validar_registro(data,usuario_existe) == False:
        return redirect('/')
    else:
        password_encriptado=bcrypt.generate_password_hash(data['password'])
        data['password']=password_encriptado
    #insert
    id_usuario=Usuario.crear_uno(data)
    #agregar datos del usuario
    session['nombre']=data['nombre']
    session['apellido']=data['apellido']
    session['id_usuario']=id_usuario
    #redireccionar al home
    return redirect('/admin')

@app.route('/login', methods = ['POST'])
def procesa_login():
    data={
        "email":request.form['email_login']
    }
    usuario_existe = Usuario.obtener_uno_con_email(data)
    if usuario_existe==None:
        flash("Este usuario no existe", "error_email_login")
        return redirect ('/')
    else:
        if not bcrypt.check_password_hash(usuario_existe.password, request.form['password_login']):
            flash("Error de password.", "error_password_login")
            return redirect('/')
        else:
            session['nombre']=usuario_existe.nombre
            session['apellido']=usuario_existe.apellido
            session['id_usuario']=usuario_existe.id
            return redirect('/recetas')

@app.route('/logout', methods=['POST'])
def haz_logout():
    session.clear()
    return redirect('/')