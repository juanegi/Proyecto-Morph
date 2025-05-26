import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


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
#from face_swap import realizar_faceswap 
from face_swap_insight import realizar_faceswap_insightface

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
    global frame_original
    if camara:
        ret, frame = camara.read()
        if ret:
            frame_original = frame.copy()  # sin espejo → para análisis y guardar
            frame_preview = cv2.flip(frame_original, 1)  # con espejo → para mostrar

            # Filtro cálido leve
            frame_filtro = cv2.convertScaleAbs(frame_preview, alpha=1.03, beta=5)
            frame_filtro[:, :, 2] = cv2.add(frame_filtro[:, :, 2], 5)

            img = cv2.cvtColor(frame_filtro, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img).resize((img_w, img_h))
            imgtk = ImageTk.PhotoImage(image=img)
            label_imagen.imgtk = imgtk
            label_imagen.configure(image=imgtk)

        ventana.after(20, actualizar_video)


def tomar_captura():
    global frame_original
    if camara and frame_original is not None:
        # Crear imagen espejada desde la imagen original
        frame_espejo = cv2.flip(frame_original, 1)

        # Guardar la imagen espejada como la imagen oficial del usuario (para face swap)
        ruta_foto = 'foto_usuario.jpg'
        cv2.imwrite(ruta_foto, frame_espejo)

        # También guardarla temporalmente para mostrarla como vista previa
        temp_ruta = "__temp_espejo.jpg"
        cv2.imwrite(temp_ruta, frame_espejo)

        # Procesar emoción con la imagen en espejo
        procesar_emocion(ruta_foto)


def procesar_emocion(ruta):
    emocion_es = detectar_emocion_desde_imagen(ruta)
    label_emocion.config(text=f"Emoción: {emocion_es}")
    
    if "rostro" in emocion_es or "cargar" in emocion_es:
        label_personaje.config(text="")
        label_foto_capturada.config(image="")
        label_foto_capturada.image = None
    else:
        ruta_imagen_personaje, texto = mostrar_info_personaje(emocion_es)
        label_personaje.config(text=texto)

        # Face swap y control de error
        #exito_swap = realizar_faceswap("foto_usuario.jpg", ruta_imagen_personaje)
        exito_swap = realizar_faceswap_insightface("foto_usuario.jpg", ruta_imagen_personaje)

        if exito_swap and os.path.exists("resultado_faceswap.jpg"):
            mostrar_foto_capturada("resultado_faceswap.jpg")
        else:
            print(" No se pudo generar el face swap.")
            mostrar_foto_capturada(ruta)


def mostrar_foto_capturada(ruta):
    ancho_deseado = 500
    alto_deseado = 400

    imagen = Image.open(ruta).resize((ancho_deseado, alto_deseado))
    label_foto_capturada.config(width=ancho_deseado, height=alto_deseado)

    imagen_tk = ImageTk.PhotoImage(imagen)
    label_foto_capturada.configure(image=imagen_tk)
    label_foto_capturada.image = imagen_tk

# INTERFAZ TKINTER
ventana = tk.Tk()
ventana.title("RetroMorph")
ventana.geometry(f"{win_w}x{win_h}")
ventana.configure(bg="#121212")  # Fondo tipo Magicam

frame_principal = tk.Frame(ventana, bg="#121212")
frame_principal.pack(fill="both", expand=True, padx=40, pady=30)

# Título arriba izquierda

# Título estilo logo (simple, moderno, un solo color)
titulo = tk.Label(
    frame_principal,
    text="RetroMorph",
    font=("Segoe UI", 26, "bold italic"),  # un poco más grande y con inclinación
    fg="white",                            # blanco sólido
    bg="#121212",                          # fondo tipo Magicam
    anchor="w"
)
titulo.grid(row=0, column=0, sticky="nw", padx=10, pady=(0, 20), columnspan=2)
frame_izquierdo = tk.Frame(frame_principal, bg="#121212")
frame_izquierdo.grid(row=1, column=0, sticky="n")

# Imagen de cámara sin fondo extra
label_imagen = tk.Label(frame_izquierdo, bg="#121212")  # Igual al fondo de la ventana
label_imagen.pack(pady=(0, 20))  # Espacio para el botón debajo

# Botón de captura con estilo
btn_captura = tk.Button(
    frame_izquierdo,
    text="🎬 Tomar Captura",
    command=tomar_captura,
    bg="#6c63ff",              
    fg="white",
    activebackground="#574fcf",
    activeforeground="white",
    font=("Segoe UI", 15, "bold"),
    bd=0,
    relief="flat",
    cursor="hand2",
    padx=32, pady=14
)
btn_captura.pack()

# Frame derecho con fondo propio (panel completo)
panel_ancho = int(win_w * 0.35)
panel_alto = int(win_h * 100)  # puedes ajustar esto

frame_derecho = tk.Frame(frame_principal, bg="#1c1c1e", width=panel_ancho, height=panel_alto)
frame_derecho.grid(row=1, column=1, sticky="nsew", padx=(40, 0))
frame_derecho.grid_propagate(False)  # No dejar que se encoja


label_foto_capturada = tk.Label(
    frame_derecho,
    bg="#1c1c1e",  # mismo color del panel derecho para que se camufle
    width=320,
    height=240,
    relief="flat",
    bd=0,
    highlightthickness=0
)

label_foto_capturada.pack(pady=(30, 20), padx=25) # Margenes

# Texto emoción
label_emocion = tk.Label(frame_derecho, text="", font=("Segoe UI", 18, "bold"),
                         fg="white", bg="#1c1c1e", justify="left", anchor="w",
                         wraplength=int(win_w * 0.3))
label_emocion.pack(pady=(0, 10), fill="x", padx=20)

# Texto personaje
label_personaje = tk.Label(frame_derecho, text="", font=("Segoe UI", 13),
                           fg="#cccccc", bg="#1c1c1e", justify="left", anchor="w",
                           wraplength=int(win_w * 0.3))
label_personaje.pack(pady=(0, 20), fill="x", padx=20)


# INICIAR CÁMARA
camara = cv2.VideoCapture(0)
if not camara.isOpened():
    messagebox.showerror("Error", "No se pudo acceder a la cámara.")
else:
    actualizar_video()

ventana.mainloop()