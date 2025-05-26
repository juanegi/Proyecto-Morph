# face_swap_insight.py

import insightface
import cv2
import numpy as np
from PIL import Image

# Cargar el modelo del face swap
swapper = insightface.model_zoo.get_model("inswapper_128.onnx")  # ← NO lleva .prepare()

# Cargar detector de rostros
face_model = insightface.app.FaceAnalysis(name='buffalo_l')
face_model.prepare(ctx_id=0)

def realizar_faceswap_insightface(ruta_usuario, ruta_personaje, ruta_salida="resultado_faceswap.jpg"):
    try:
        img_src = cv2.imread(ruta_usuario)
        img_dst = cv2.imread(ruta_personaje)

        if img_src is None or img_dst is None:
            print(" No se pudieron leer las imágenes.")
            return False

        faces_src = face_model.get(img_src)
        faces_dst = face_model.get(img_dst)

        if len(faces_src) == 0:
            print(" No se detectó rostro en la imagen del usuario.")
            return False
        if len(faces_dst) == 0:
            print(" No se detectó rostro en la imagen del personaje.")
            return False

        face_dst = faces_dst[0]
        face_src = faces_src[0]

        output = swapper.get(img_dst, face_dst, face_src, paste_back=True)
        cv2.imwrite(ruta_salida, output)
        print(" Face swap generado con éxito (InsightFace).")
        return True

    except Exception as e:
        print(f" Error en InsightFace swap: {e}")
        return False
