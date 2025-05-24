import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
from personajes import mostrar_info_personaje

# Verificar existencia del modelo
if not os.path.exists("modelo_emociones.h5"):
    raise FileNotFoundError("El archivo del modelo 'modelo_emociones.h5' no se encontró.")

# Cargar modelo y etiquetas
modelo = load_model("modelo_emociones.h5", compile=False)
emociones = ['Enojo', 'Disgusto', 'Miedo', 'Feliz', 'Triste', 'Sorpresa', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Estado de la cámara y frame actual
camara = None
frame_actual = None

# Obtener tamaño de pantalla y calcular 80%
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
win_w = int(screen_width * 0.8)
win_h = int(screen_height * 0.8)
img_w = int(win_h * 0.8)  # Imagen cuadrada, 80% del alto de la ventana
img_h = img_w

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
    global camara, frame_actual
    if camara and frame_actual is not None:
        nombre_archivo = 'foto_usuario.jpg'
        cv2.imwrite(nombre_archivo, frame_actual)
        mostrar_imagen(nombre_archivo)
        procesar_imagen(nombre_archivo)

def procesar_imagen(nombre_archivo):
    imagen = cv2.imread(nombre_archivo)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    rostros = face_cascade.detectMultiScale(gris, scaleFactor=1.3, minNeighbors=5)

    if len(rostros) == 0:
        label_emocion.config(text="No se detectó ningún rostro.")
        label_personaje.config(text="")
        return

    for (x, y, w, h) in rostros:
        rostro = gris[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (64, 64))
        rostro = rostro.astype("float32") / 255.0
        rostro = np.expand_dims(rostro, axis=0)
        rostro = np.expand_dims(rostro, axis=-1)

        prediccion = modelo.predict(rostro, verbose=0)
        emocion_idx = np.argmax(prediccion)
        emocion = emociones[emocion_idx]

        label_emocion.config(text=f"Emoción: {emocion}")
        info_personaje = mostrar_info_personaje(emocion)
        label_personaje.config(text=info_personaje)
        return

def mostrar_imagen(ruta):
    imagen = Image.open(ruta).resize((img_w, img_h))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen.configure(image=imagen_tk)
    label_imagen.image = imagen_tk  # mantener referencia

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Detección de Emociones")
ventana.geometry(f"{win_w}x{win_h}")
ventana.configure(bg="#e0e0e0")

# Layout principal
frame_principal = tk.Frame(ventana, bg="#e0e0e0")
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Frame izquierdo (imagen + botón)
frame_izquierdo = tk.Frame(frame_principal, bg="#e0e0e0")
frame_izquierdo.grid(row=0, column=0, sticky="n")

label_imagen = tk.Label(frame_izquierdo, bg="#e0e0e0", width=img_w, height=img_h)
label_imagen.pack(pady=(0, 20))

estilo_boton = {
    "bg": "#ff9800",
    "fg": "#ffffff",
    "activebackground": "#e65100",
    "activeforeground": "#ffffff",
    "font": ("Segoe UI", 16, "bold"),
    "bd": 0,
    "relief": "flat",
    "cursor": "hand2",
    "highlightthickness": 0,
    "padx": 24,
    "pady": 16
}

btn_ejecutar = tk.Button(frame_izquierdo, text="Tomar Captura", command=tomar_captura, **estilo_boton)
btn_ejecutar.pack()

# Frame derecho (resultados)
frame_derecho = tk.Frame(frame_principal, bg="#e0e0e0")
frame_derecho.grid(row=0, column=1, sticky="n", padx=(40, 0))

estilo_label = {
    "bg": "#e0e0e0",
    "fg": "#333333"
}

label_emocion = tk.Label(frame_derecho, text="", **estilo_label, font=("Segoe UI", 22, "bold"), anchor="w", justify="left", wraplength=int(win_w*0.3))
label_emocion.pack(pady=(40, 30), fill="x")

label_personaje = tk.Label(frame_derecho, text="", **estilo_label, font=("Segoe UI", 15), anchor="w", justify="left", wraplength=int(win_w*0.3))
label_personaje.pack(pady=10, fill="x")

# Iniciar cámara y mostrar video automáticamente
camara = cv2.VideoCapture(0)
if not camara.isOpened():
    messagebox.showerror("Error", "No se pudo acceder a la cámara.")
else:
    actualizar_video()

ventana.mainloop()
