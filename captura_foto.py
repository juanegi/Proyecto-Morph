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

def capturar_y_detectar():
    nombre_archivo = 'foto_usuario.jpg'
    camara = cv2.VideoCapture(0)
    if not camara.isOpened():
        messagebox.showerror("Error", "No se pudo acceder a la cámara.")
        return

    ret, frame = camara.read()
    camara.release()

    if not ret:
        messagebox.showerror("Error", "No se pudo capturar la imagen.")
        return

    cv2.imwrite(nombre_archivo, frame)

    # Mostrar imagen en la interfaz
    mostrar_imagen(nombre_archivo)

    # Procesar imagen
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
    imagen = Image.open(ruta).resize((200, 200))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen.configure(image=imagen_tk)
    label_imagen.image = imagen_tk  # mantener referencia

# Crear ventana
ventana = tk.Tk()
ventana.title("Detección de Emociones")
ventana.geometry("350x400")
ventana.configure(bg="#e0e0e0")  # Fondo gris claro

# Estilos minimalistas
estilo_boton = {
    "bg": "#ff9800",         # Naranja
    "fg": "#ffffff",         # Texto blanco
    "activebackground": "#e65100",
    "activeforeground": "#ffffff",
    "font": ("Segoe UI", 11, "bold"),
    "bd": 0,
    "relief": "flat",
    "cursor": "hand2",
    "highlightthickness": 0,
    "padx": 10,
    "pady": 8
}

estilo_label = {
    "bg": "#e0e0e0",
    "fg": "#333333"
}

btn_ejecutar = tk.Button(ventana, text="Capturar Foto y Detectar Emoción", command=capturar_y_detectar, **estilo_boton)
btn_ejecutar.pack(pady=18)

label_imagen = tk.Label(ventana, **estilo_label)
label_imagen.pack(pady=10)

label_emocion = tk.Label(ventana, text="", **estilo_label, font=("Segoe UI", 12, "bold"))
label_emocion.pack(pady=8)

label_personaje = tk.Label(ventana, text="", **estilo_label, font=("Segoe UI", 10))
label_personaje.pack(pady=8)

ventana.mainloop()
