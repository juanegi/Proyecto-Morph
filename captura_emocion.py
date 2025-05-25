import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_b0
import cv2
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from personajes import mostrar_info_personaje
from detectar_emocion import detectar_emocion_desde_imagen

EMOCIONES = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar modelo EfficientNet-B0
model = efficientnet_b0(weights=None)
model.classifier = nn.Sequential(
    nn.Dropout(p=0.4),
    nn.Linear(model.classifier[1].in_features, 7)
)
model.load_state_dict(torch.load('modelo_emociones/modelo_emociones_efficientnet.pth', map_location=DEVICE))
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

# TAMAÑO DE VENTANA (pantalla completa)
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
win_w = screen_width
win_h = screen_height

# Tamaño de la cámara reducido
img_w = 480
img_h = 360

camara = None
frame_actual = None

def actualizar_video():
    global frame_actual
    if camara:
        ret, frame = camara.read()
        if ret:
            frame_actual = frame.copy()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img).resize((img_w, img_h))
            imgtk = ImageTk.PhotoImage(image=img)
            label_imagen.imgtk = imgtk
            label_imagen.configure(image=imgtk)
        ventana.after(20, actualizar_video)

def tomar_captura():
    global frame_actual
    if camara and frame_actual is not None:
        ruta_foto = 'foto_usuario.jpg'
        cv2.imwrite(ruta_foto, frame_actual)
        mostrar_imagen_camara(ruta_foto)
        procesar_emocion(ruta_foto)

def procesar_emocion(ruta):
    emocion_es = detectar_emocion_desde_imagen(ruta)
    label_emocion.config(text=f"Emoción: {emocion_es}")
    if "rostro" in emocion_es or "cargar" in emocion_es:
        label_personaje.config(text="")
        label_foto_capturada.config(image="")
        label_foto_capturada.image = None
    else:
        info = mostrar_info_personaje(emocion_es)
        label_personaje.config(text=info)
        mostrar_foto_capturada(ruta)

def mostrar_imagen_camara(ruta):
    imagen = Image.open(ruta).resize((img_w, img_h))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen.configure(image=imagen_tk)
    label_imagen.image = imagen_tk

def mostrar_foto_capturada(ruta):
    # Mostrar la foto capturada a la derecha, debajo de la info
    imagen = Image.open(ruta).resize((320, 240))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_foto_capturada.configure(image=imagen_tk)
    label_foto_capturada.image = imagen_tk

# INTERFAZ TKINTER
ventana = tk.Tk()
ventana.title("Detección de Emociones con PyTorch")
ventana.geometry(f"{win_w}x{win_h}")
ventana.configure(bg="#e0e0e0")

frame_principal = tk.Frame(ventana, bg="#e0e0e0")
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Frame izquierdo (cámara + botón)
frame_izquierdo = tk.Frame(frame_principal, bg="#e0e0e0")
frame_izquierdo.grid(row=0, column=0, sticky="n")

label_imagen = tk.Label(frame_izquierdo, bg="#e0e0e0", width=img_w, height=img_h)
label_imagen.pack(pady=(0, 20))

estilo_boton = {
    "bg": "#2196f3", "fg": "#ffffff",
    "activebackground": "#0d47a1",
    "activeforeground": "#ffffff",
    "font": ("Segoe UI", 16, "bold"),
    "bd": 0, "relief": "flat",
    "cursor": "hand2", "highlightthickness": 0,
    "padx": 24, "pady": 16
}

btn_captura = tk.Button(
    frame_izquierdo,
    text="Tomar Captura",
    command=tomar_captura,
    **estilo_boton
)
btn_captura.pack()

# Frame derecho (foto capturada arriba, info abajo)
frame_derecho = tk.Frame(frame_principal, bg="#e0e0e0")
frame_derecho.grid(row=0, column=1, sticky="n", padx=(40, 0))

label_foto_capturada = tk.Label(frame_derecho, bg="#e0e0e0")
label_foto_capturada.pack(pady=(30, 10))  # Foto arriba

estilo_label = {"bg": "#e0e0e0", "fg": "#333333"}
label_emocion = tk.Label(frame_derecho, text="", **estilo_label, font=("Segoe UI", 22, "bold"),
                         anchor="w", justify="left", wraplength=int(win_w * 0.3))
label_emocion.pack(pady=(10, 10), fill="x")

label_personaje = tk.Label(frame_derecho, text="", **estilo_label, font=("Segoe UI", 15),
                           anchor="w", justify="left", wraplength=int(win_w * 0.3))
label_personaje.pack(pady=10, fill="x")

# INICIAR CÁMARA
camara = cv2.VideoCapture(0)
if not camara.isOpened():
    messagebox.showerror("Error", "No se pudo acceder a la cámara.")
else:
    actualizar_video()

ventana.mainloop()