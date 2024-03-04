from flask import render_template, Response, jsonify
from app_attendward import app
import cv2
import os

# Directorio de entrenamientos
entrenamientos_ruta = 'app_attendward/rfacial/entrenamientos'

# Lista para almacenar las personas detectadas
listaDeDetectados = []

def generate():
    modelos_entrenados = []
    nombres_personas = []

    # for modelo_file in os.listdir(entrenamientos_ruta):
    #     modelo_entrenado = cv2.face_EigenFaceRecognizer.create()
    #     modelo_entrenado.read(os.path.join(entrenamientos_ruta, modelo_file))
    #     modelos_entrenados.append(modelo_entrenado)
    #     nombres_personas.append(os.path.splitext(os.path.basename(modelo_file))[0])

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

@app.route('/captura_asistencia', methods=['GET'])
def get_all_alumnos():
    return render_template('captura_asistencia.html')

@app.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

