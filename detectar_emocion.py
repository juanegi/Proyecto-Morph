import os
import sys
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_b0
import cv2
from PIL import Image

EMOCIONES = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar modelo EfficientNet-B0
model = efficientnet_b0(weights=None)
model.classifier = nn.Sequential(
    nn.Dropout(p=0.4),
    nn.Linear(model.classifier[1].in_features, 7)
)

def obtener_ruta_relativa(ruta):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta)
    return ruta

ruta_modelo = obtener_ruta_relativa("modelo_emociones/modelo_emociones_efficientnet.pth")
model.load_state_dict(torch.load(ruta_modelo, map_location=DEVICE))
#model.load_state_dict(torch.load('modelo_emociones/modelo_emociones_efficientnet.pth', map_location=DEVICE))
model.to(DEVICE)
model.eval()

# Preprocesamiento
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Mapeo inglés a español
MAPEO_EMOCIONES = {
    "angry": "Enojo",
    "disgust": "Disgusto",
    "fear": "Miedo",
    "happy": "Feliz",
    "sad": "Triste",
    "surprise": "Sorpresa",
    "neutral": "Neutral"
}

def detectar_emocion_desde_imagen(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        return "No se pudo cargar la imagen."
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    rostros = face_cascade.detectMultiScale(gris, scaleFactor=1.3, minNeighbors=5)
    if len(rostros) == 0:
        return "No se detectó ningún rostro."
    for (x, y, w, h) in rostros:
        rostro = imagen[y:y+h, x:x+w]
        rostro = cv2.cvtColor(rostro, cv2.COLOR_BGR2RGB)
        rostro = Image.fromarray(rostro)
        tensor = transform(rostro).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            output = model(tensor)
            pred_idx = torch.argmax(output, dim=1).item()
            emocion = EMOCIONES[pred_idx]
        emocion_es = MAPEO_EMOCIONES.get(emocion, emocion)
        return emocion_es
    return "No se detectó ningún rostro."