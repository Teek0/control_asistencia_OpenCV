import cv2 as cv
import os
import numpy as np
from time import time

dataRuta = 'C:/Users/Administrador/Desktop/TT2/ttini/ReconocimientoFacial/DATA'
listaData = os.listdir(dataRuta)
# Crear una lista para almacenar modelos de entrenamiento
modelos_entrenados = []

for persona in listaData:
    rutaCompleta = dataRuta + '/' + persona
    print('Leyendo las imágenes de: ', persona, '...')
    
    # Crear una instancia de EigenFaceRecognizer para cada persona
    entrenamientoEigenFaceRecognizer = cv.face_EigenFaceRecognizer.create()
    
    ids = []
    rostrosData = []
    id = 0

    for archivo in os.listdir(rutaCompleta):
        ids.append(id)
        rostrosData.append(cv.imread(os.path.join(rutaCompleta, archivo), 0))
        id += 1

    entrenamientoEigenFaceRecognizer.train(rostrosData, np.array(ids))
    
    # Guardar el modelo en un archivo
    modelo_file = f"modelo_{persona}.xml"
    entrenamientoEigenFaceRecognizer.save(os.path.join(dataRuta, modelo_file))
    
    modelos_entrenados.append(entrenamientoEigenFaceRecognizer)

print("Entrenamiento concluido.")

