from flask import render_template, Response
from app_attendward import app
from app_attendward.config.mysqlconnection import connectToMySQL
from datetime import datetime
import cv2
import os

entrenamientos_ruta = 'app_attendward/rfacial/entrenamientos'

listaDeDetectados = []
listaDeEstudiantes = []

def generatex():
    modelos_entrenados = []
    nombres_personas = []

    for modelo_file in os.listdir(entrenamientos_ruta):
        for estudiante in listaDeEstudiantes:
            if estudiante['rut'] ==  int(os.path.splitext(os.path.basename(modelo_file))[0]):
                modelo_entrenado = cv2.face_EigenFaceRecognizer.create()
                modelo_entrenado.read(os.path.join(entrenamientos_ruta, modelo_file))
                modelos_entrenados.append(modelo_entrenado)
                nombres_personas.append(os.path.splitext(os.path.basename(modelo_file))[0])


    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                rostro = gray[y:y+h, x:x+w]  # Obtener el rostro
                rostro = cv2.resize(rostro, (160, 160), interpolation=cv2.INTER_CUBIC)  # Redimensionar el rostro

                # Realizar la predicción con cada modelo de entrenamiento
                for i, modelo_entrenado in enumerate(modelos_entrenados):
                    resultado = modelo_entrenado.predict(rostro)

                    if resultado[1] < 7000:
                        nombre_persona = nombres_personas[i]
                        # Si la persona no ha sido detectada previamente, agregarla a la lista
                        if nombre_persona not in listaDeDetectados:
                            listaDeDetectados.append(nombre_persona)
                        cv2.putText(frame, nombre_persona, (x, y - 20), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        break  # Salir del bucle si se encuentra una persona
                else:
                    cv2.putText(frame, "No encontradox", (x, y - 20), 2, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            (flag, encoded_image) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')


@app.route('/cursos', methods=['GET'])
def get_all_cursos():
    mysql = connectToMySQL('attend_bd')
    data = mysql.query_db("SELECT secciones.*, asignaturas.nombre AS nombre_asignatura FROM secciones JOIN asignaturas ON asignaturas.id_asignatura = secciones.id_asignatura;")
    mysql.close_connection()
    return render_template('cursos.html', cursos=data)

@app.route('/alumnos/<int:section_id>', methods=['GET'])
def get_alumnos_by_section(section_id):
    mysql = connectToMySQL('attend_bd')
    # Consulta para obtener los datos de la sección y la asignatura
    section_query = "SELECT secciones.*, asignaturas.nombre AS nombre_asignatura FROM secciones JOIN asignaturas ON asignaturas.id_asignatura = secciones.id_asignatura WHERE secciones.id_seccion = %s;"
    section_data = mysql.query_db(section_query, (section_id,))
    # Consulta para obtener los datos de los alumnos
    alumnos_query = "SELECT alumnos.* FROM alumnos JOIN inscritos ON inscritos.id_alumno = alumnos.id_alumno WHERE inscritos.id_seccion = %s;"
    alumnos_data = mysql.query_db(alumnos_query, (section_id,))
    auxList = []
    for alumno in alumnos_data:
        auxList.append(alumno)
    global listaDeEstudiantes
    listaDeEstudiantes = auxList 
    # Cerrar la conexión manualmente
    mysql.close_connection()
    fecha_actual = datetime.now()
    # Define un diccionario para traducir los nombres de los meses
    meses = {
        1: 'enero',
        2: 'febrero',
        3: 'marzo',
        4: 'abril',
        5: 'mayo',
        6: 'junio',
        7: 'julio',
        8: 'agosto',
        9: 'septiembre',
        10: 'octubre',
        11: 'noviembre',
        12: 'diciembre'
    }
    return render_template('alumnos.html', seccion=section_data[0], alumnos=alumnos_data, fecha_actual=fecha_actual, meses=meses)

@app.route('/video_feedx', methods=['GET'])
def video_feedx():
    return Response(generatex(), mimetype='multipart/x-mixed-replace; boundary=frame')