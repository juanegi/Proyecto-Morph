import cv2
import numpy as np
from tensorflow.keras.models import load_model
#apesar de esta advertencia no se puede eliminar el error de la libreria tensorflow por el momento

# # Cargar modelo preentrenado lo saque de aqui https://github.com/otaha178/Emotion-recognition
# # Cargar modelo preentrenado (Agregando captura de foto y preparación para reconocimiento facial)
modelo = load_model("modelo_emociones.h5", compile=False)


# Etiquetas de emociones del dataset FER-2013
emociones = ['Enojo', 'Disgusto', 'Miedo', 'Feliz', 'Triste', 'Sorpresa', 'Neutral']

# Cargar clasificador Haar para detectar rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detectar_emocion(imagen_path):
    imagen = cv2.imread(imagen_path)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    rostros = face_cascade.detectMultiScale(gris, scaleFactor=1.3, minNeighbors=5)

    if len(rostros) == 0:
        return "Sin rostro detectado"

    for (x, y, w, h) in rostros:
        rostro = gris[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (64, 64)) #se modifica el tamaño de la imagen a 64x64 no funciona con 48x48
        rostro = rostro.astype("float32") / 255.0
        rostro = np.expand_dims(rostro, axis=0)
        rostro = np.expand_dims(rostro, axis=-1)

        prediccion = modelo.predict(rostro, verbose=0)
        emocion_idx = np.argmax(prediccion)
        return emociones[emocion_idx]

    return "Sin rostro detectado"
