from flask import render_template, request, redirect, url_for, flash
from app_attendward import app
from app_attendward.config.mysqlconnection import connectToMySQL
import os

@app.route('/admin', methods=['GET'])
def admin_page():
    resultados = None
    return render_template('admin.html', resultados=resultados)

@app.route('/buscar_alumno', methods=['POST'])
def buscar_alumno():

    entrenamientos_ruta = 'app_attendward/rfacial/entrenamientos'

    # Obtener el rut ingresado por el usuario desde el formulario
    rut = request.form.get('rut')

    # Crear una conexión a la base de datos
    db = connectToMySQL('attend_bd')

    # Consulta SQL para buscar al alumno por rut
    query = "SELECT * FROM alumnos WHERE rut = %s"

    
    data = (rut,)
    resultados = db.query_db(query, data)

    trainFound = False
    for modelo_file in os.listdir(entrenamientos_ruta):
        if int(rut) == int(os.path.splitext(os.path.basename(modelo_file))[0]):
            trainFound = True

    resultados = {"trainFound":trainFound,"resultados":resultados}
    # Renderizar la misma página admin.html con los resultados de la búsqueda
    return render_template('admin.html', resultados=resultados)

@app.route('/crear_alumno', methods=['POST'])
def crear_alumno():
    # Obtener los datos del formulario
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    rut = request.form.get('rut_nuevo')

    # Validar que todos los campos estén llenos
    if not nombre or not apellido or not rut:
        # Si alguno de los campos está vacío, redireccionar a la página admin con un mensaje de error
        flash('Todos los campos son obligatorios', 'error')
        return redirect(url_for('admin_page'))

    # Crear una conexión a la base de datos
    db = connectToMySQL('attend_bd')

    # Consulta SQL para verificar si el rut ya existe en la base de datos
    query = "SELECT * FROM alumnos WHERE rut = %s"
    data = (rut,)
    resultado = db.query_db(query, data)

    # Si el rut ya existe en la base de datos, mostrar un mensaje de error y redireccionar
    if resultado:
        flash('El rut proporcionado ya está registrado', 'error')
        return redirect(url_for('admin_page'))

    # Consulta SQL para insertar un nuevo alumno en la base de datos
    query = "INSERT INTO alumnos (nombre, apellido, rut) VALUES (%s, %s, %s)"
    data = (nombre, apellido, rut)
    
    # Ejecutar la consulta
    db.query_db(query, data)

    # Mostrar un mensaje de éxito y redireccionar a la página admin
    flash('Alumno creado exitosamente', 'success')
    return redirect(url_for('admin_page'))