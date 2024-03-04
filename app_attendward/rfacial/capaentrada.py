import cv2 as cv
import os
import imutils
from time import time

modelo = '18085868'
ruta1 = 'app_attendward/rfacial/DATA'
ruta_completa = ruta1+'/'+modelo

if not os.path.exists(ruta_completa):
    os.makedirs(ruta_completa)

camara = cv.VideoCapture(0)
print("camara lista")
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
        cv.imwrite(ruta_completa+'/imagen_{}.jpg'.format(id),
                rostrocapturado)  # guarda imagen
        id = id+1

    cv.imshow("Resultado", captura)

    if id == 26:
        break
print("Tiempo de captura: ", round(time() - tiempo_inicial, 1), " segundos")
camara.release()
cv.destroyAllWindows()