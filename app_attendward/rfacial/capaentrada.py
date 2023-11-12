# pip install opencv-python
# python.exe -m pip install --upgrade pip
# pip install opencv-contrib-python
# pip install imutils

import cv2 as cv
import os
import imutils
from time import time

modelo = '18085868'
ruta1 = 'C:/Users/Administrador/Desktop/TT2/ttini/ReconocimientoFacial/DATA'
rutacompleta = ruta1+'/'+modelo

if not os.path.exists(rutacompleta):
    os.makedirs(rutacompleta)

camara = cv.VideoCapture(0)
print("camara lista")
ruidos = cv.CascadeClassifier('ReconocimientoFacial/haarcascade_frontalface_default.xml')    # detector de rostros
tiempoInicial = time()

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
        cv.imwrite(rutacompleta+'/imagen_{}.jpg'.format(id),
                rostrocapturado)  # guarda imagen
        id = id+1

    cv.imshow("Resultado", captura)

    if id == 100:
        break
print("Tiempo de captura: ", round(time() - tiempoInicial, 1), " segundos")
camara.release()
cv.destroyAllWindows()
