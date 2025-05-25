import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
from personajes import mostrar_info_personaje
from captura_emocion import detectar_emocion_desde_imagen

# TAMAÑO DE VENTANA
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
win_w = int(screen_width * 0.8)
win_h = int(screen_height * 0.8)
img_w = int(win_h * 1)
img_h = img_w

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
        mostrar_imagen(ruta_foto)
        procesar_emocion(ruta_foto)

def procesar_emocion(ruta):
    emocion_es = detectar_emocion_desde_imagen(ruta)
    label_emocion.config(text=f"Emoción: {emocion_es}")
    if "rostro" in emocion_es or "cargar" in emocion_es:
        label_personaje.config(text="")
    else:
        info = mostrar_info_personaje(emocion_es)
        label_personaje.config(text=info)

def mostrar_imagen(ruta):
    imagen = Image.open(ruta).resize((img_w, img_h))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen.configure(image=imagen_tk)
    label_imagen.image = imagen_tk

# INTERFAZ TKINTER
ventana = tk.Tk()
ventana.title("Detección de Emociones con PyTorch")
ventana.geometry(f"{win_w}x{win_h}")
ventana.configure(bg="#e0e0e0")

frame_principal = tk.Frame(ventana, bg="#e0e0e0")
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

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

frame_derecho = tk.Frame(frame_principal, bg="#e0e0e0")
frame_derecho.grid(row=0, column=1, sticky="n", padx=(40, 0))

estilo_label = {"bg": "#e0e0e0", "fg": "#333333"}
label_emocion = tk.Label(frame_derecho, text="", **estilo_label, font=("Segoe UI", 22, "bold"),
                         anchor="w", justify="left", wraplength=int(win_w * 0.3))
label_emocion.pack(pady=(40, 30), fill="x")

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