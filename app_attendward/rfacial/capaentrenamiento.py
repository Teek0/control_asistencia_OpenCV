import cv2 as cv
import os
import numpy as np

data_ruta = 'app_attendward/rfacial/DATA'
lista_data = os.listdir(data_ruta)
# Crear una lista para almacenar modelos de entrenamiento
modelos_entrenados = []

for persona in lista_data:
    ruta_completa = data_ruta + '/' + persona
    print('Leyendo las imágenes de: ', persona, '...')
    
    # Crear una instancia de EigenFaceRecognizer para cada persona
    entrenamiento_eigen_face_recognizer = cv.face_EigenFaceRecognizer.create()
    
    ids = []
    rostros_data = []
    id = 0

    for archivo in os.listdir(ruta_completa):
        ids.append(id)
        rostros_data.append(cv.imread(os.path.join(ruta_completa, archivo), 0))
        id += 1

    entrenamiento_eigen_face_recognizer.train(rostros_data, np.array(ids))
    
    # Guardar el modelo en un archivo
    modelo_file = f"modelo_{persona}.xml"
    entrenamiento_eigen_face_recognizer.save(os.path.join('app_attendward/rfacial/entrenamientos', modelo_file))
    
    modelos_entrenados.append(entrenamiento_eigen_face_recognizer)

print("Entrenamiento concluido.")

