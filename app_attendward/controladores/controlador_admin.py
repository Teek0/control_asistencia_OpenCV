from flask import render_template, request, redirect, url_for, flash
from app_attendward import app
from app_attendward.config.mysqlconnection import connectToMySQL
import os
import cv2 as cv
import numpy as np
import imutils
from time import time
from shutil import rmtree

@app.route('/admin', methods=['GET'])
def admin_page():
    resultados = None
    return render_template('admin.html', resultados=resultados)

@app.route('/buscar_alumno', methods=['POST'])
def buscar_alumno():
    entrenamientos_ruta = 'app_attendward/rfacial/entrenamientos'
    # Obtener el rut ingresado por el usuario desde el formulario
    rut = request.form.get('rut')

    db = connectToMySQL('attend_bd')
    query = "SELECT * FROM alumnos WHERE rut = %s"

    data = (rut,)
    resultados = db.query_db(query, data)

    train_found = False
    for modelo_file in os.listdir(entrenamientos_ruta):
        if int(rut) == int(os.path.splitext(os.path.basename(modelo_file))[0]):
            train_found = True

    resultados = {"train_found":train_found,"resultados":resultados}
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
        # Si algún campo está vacío, enviar un mensaje de error y redireccionar a la página admin
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


@app.route('/entrenar', methods=['POST'])
def entrenar_modelo():
    # Configuración para el entrenamiento
    rut = request.form.get('rut')
    modelo = rut
    ruta1 = 'app_attendward/rfacial/DATA'
    ruta_completa = os.path.join(ruta1, modelo)

    if not os.path.exists(ruta_completa):
        os.makedirs(ruta_completa)

    camara = cv.VideoCapture(0)
    print("Cámara lista")
    ruidos = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')    # detector de rostros
    tiempo_inicial = time()

    id = 1
    while True:
        respuesta, captura = camara.read()
        if respuesta == False:
            break
        captura = imutils.resize(captura, width=640)

        gris = cv.cvtColor(captura, cv.COLOR_BGR2GRAY)  # escala de grises
        idcaptura = captura.copy()

        cara = ruidos.detectMultiScale(gris, 1.3, 5)   # detecta rostros

        for (x, y, e1, e2) in cara:
            cv.rectangle(captura, (x, y), (x+e1, y+e2),
                        (0, 255, 0), 2)  # dibuja rectangulo
            rostrocapturado = idcaptura[y:y+e2, x:x+e1]   # rostro capturado
            rostrocapturado = cv.resize(
                rostrocapturado, (160, 160), interpolation=cv.INTER_CUBIC)  # redimensiona
            cv.imwrite(os.path.join(ruta_completa, f'imagen_{id}.jpg'), rostrocapturado)  # guarda imagen
            id += 1

        cv.imshow("Resultado", captura)

        if id == 251:
            break
    print("Tiempo de captura: ", round(time() - tiempo_inicial, 1), " segundos")
    camara.release()
    cv.destroyAllWindows()

    # Entrenamiento del modelo
    data_ruta = 'app_attendward/rfacial/DATA'
    lista_data = os.listdir(data_ruta)
    modelos_entrenados = []

    for persona in lista_data:
        ruta_completa = os.path.join(data_ruta, persona)
        print('Leyendo las imágenes de:', persona)
        
        entrenamiento_eigen_face_recognizer = cv.face_EigenFaceRecognizer.create()
        
        ids = []
        rostros_data = []
        id = 0

        for archivo in os.listdir(ruta_completa):
            ids.append(id)
            rostros_data.append(cv.imread(os.path.join(ruta_completa, archivo), 0))
            id += 1

            os.remove(os.path.join(ruta_completa, archivo))

        entrenamiento_eigen_face_recognizer.train(rostros_data, np.array(ids))
        
        modelo_file = f"{persona}.xml"
        entrenamiento_eigen_face_recognizer.save(os.path.join('app_attendward/rfacial/entrenamientos', modelo_file))
        
        modelos_entrenados.append(entrenamiento_eigen_face_recognizer)

        if os.path.exists(ruta_completa):
            rmtree(ruta_completa)

    flash('Entrenamiento completado exitosamente', 'success')  # Mensaje de éxito
    return redirect(url_for('admin_page'))