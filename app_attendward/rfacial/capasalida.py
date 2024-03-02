import cv2 as cv
import os

# Directorio de entrenamientos
entrenamientos_ruta = 'app_attendward/rfacial/entrenamientos'

# Cargar modelos entrenados y sus respectivos nombres
modelos_entrenados = []
nombres_personas = []

for modelo_file in os.listdir(entrenamientos_ruta):
    modelo_entrenado = cv.face.EigenFaceRecognizer.create()
    modelo_entrenado.read(os.path.join(entrenamientos_ruta, modelo_file))
    modelos_entrenados.append(modelo_entrenado)
    nombres_personas.append(os.path.splitext(os.path.basename(modelo_file))[0])

# Iniciar la cámara
camara = cv.VideoCapture(0)

while True:
    respuesta, captura = camara.read()
    if respuesta == False:
        break

    gris = cv.cvtColor(captura, cv.COLOR_BGR2GRAY)  # Convertir a escala de grises
    caras = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gris, 1.3, 5)

    for (x, y, e1, e2) in caras:
        rostro = gris[y:y+e2, x:x+e1]  # Obtener el rostro
        rostro = cv.resize(rostro, (160, 160), interpolation=cv.INTER_CUBIC)  # Redimensionar el rostro

        # Realizar la predicción con cada modelo de entrenamiento
        persona_encontrada = False
        for i, modelo_entrenado in enumerate(modelos_entrenados):
            resultado = modelo_entrenado.predict(rostro)

            if resultado[1] < 8000:
                nombre_persona = nombres_personas[i]
                cv.putText(captura, nombre_persona, (x, y - 20), 2, 1.1, (0, 255, 0), 1, cv.LINE_AA)
                cv.rectangle(captura, (x, y), (x+e1, y+e2), (255, 0, 0), 2)
                persona_encontrada = True
                break  # Salir del bucle si se encuentra una persona

        if not persona_encontrada:
            cv.putText(captura, "No encontrado", (x, y - 20), 2, 0.7, (0, 255, 0), 1, cv.LINE_AA)
            cv.rectangle(captura, (x, y), (x+e1, y+e2), (255, 0, 0), 2)

    cv.imshow("Identificación Facial", captura)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
