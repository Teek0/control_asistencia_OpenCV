import cv2 as cv
import imutils
from capaentrenamiento import listaData, modelos_entrenados

dataRuta = 'app_attendward/rfacial/DATA'
ruidos = cv.CascadeClassifier(cv.data.haarcascade + 'haarcascade_frontalface_default.xml')
camara = cv.VideoCapture(0)

while True:
    respuesta, captura = camara.read()
    
    if respuesta is False:
        break
        
    captura = imutils.resize(captura, width=640)
    gris = cv.cvtColor(captura, cv.COLOR_BGR2GRAY)
    idcaptura = gris.copy()
    
    cara = ruidos.detectMultiScale(gris, 1.3, 5)
    
    for (x, y, e1, e2) in cara:
        rostrocapturado = idcaptura[y:y+e2, x:x+e1]
        rostrocapturado = cv.resize(rostrocapturado, (160, 160), interpolation=cv.INTER_CUBIC)
        
        # Realizar la predicción con cada modelo de entrenamiento
        for modelo_entrenado in modelos_entrenados:
            resultado = modelo_entrenado.predict(rostrocapturado)
            
            if resultado[1] < 7000:
                nombre_persona = listaData[resultado[0]]
                cv.putText(captura, nombre_persona, (x, y - 20), 2, 1.1, (0, 255, 0), 1, cv.LINE_AA)
                cv.rectangle(captura, (x, y), (x+e1, y+e2), (255, 0, 0), 2)
            else:
                cv.putText(captura, "No encontrado", (x, y - 20), 2, 0.7, (0, 255, 0), 1, cv.LINE_AA)
                cv.rectangle(captura, (x, y), (x+e1, y+e2), (255, 0, 0), 2)

    cv.imshow("Resultado", captura)
    
    if cv.waitKey(1) == ord('s'):
        break

camara.release()
cv.destroyAllWindows()
