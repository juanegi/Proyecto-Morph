import os

import estilo_nst
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
from tkinter import ttk
import threading
from tkinter import filedialog


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

    try:
        imagen = Image.open(ruta).resize((ancho_deseado, alto_deseado))
        imagen_tk = ImageTk.PhotoImage(imagen)

        label_foto_capturada.config(image=imagen_tk)
        label_foto_capturada.image = imagen_tk  # Conserva referencia
        label_foto_capturada.config(width=ancho_deseado, height=alto_deseado)
    except Exception as e:
        print(f" Error al mostrar imagen: {e}")

def guardar_imagen_final():
    ruta_guardar = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("Todos los archivos", "*.*")]
    )
    if ruta_guardar:
        try:
            imagen = Image.open("resultado_estilizado.jpg")
            imagen.save(ruta_guardar)
            print(f"Imagen guardada en {ruta_guardar}")
        except Exception as e:
            print(f"Error al guardar la imagen: {e}")


# Inicio de interfaz
ventana = tk.Tk()
ventana.title("RetroMorph")
ventana.geometry("1280x720")
ventana.configure(bg="#121212")

frame_principal = tk.Frame(ventana, bg="#121212")
frame_principal.pack(fill="both", expand=True, padx=40, pady=30)
frame_principal.grid_rowconfigure(0, minsize=80)

frame_principal.grid_rowconfigure(0, weight=0)  # fila del título principal
frame_principal.grid_rowconfigure(1, weight=0)  # fila del panel central
frame_principal.grid_rowconfigure(2, weight=1)  # fila para los botones de estilo

# Título
titulo = tk.Label(
    frame_principal,
    text="RetroMorph",
    font=("Segoe UI", 26, "bold italic"),
    fg="white",
    bg="#121212",
    anchor="w"
)
titulo.grid(row=0, column=0, sticky="nw", padx=10, pady=(0, 20), columnspan=3)

# Panel izquierdo - Cámara
frame_izquierdo = tk.Frame(frame_principal, bg="#121212")
frame_izquierdo.grid(row=1, column=0, sticky="n")

label_imagen = tk.Label(frame_izquierdo, bg="#121212", width=480, height=360)
label_imagen.pack(pady=(0, 20))

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

# Panel central - Imagen y textos
frame_central = tk.Frame(frame_principal, bg="#1c1c1e", width=500, height=500)
frame_central.grid(row=1, column=1, sticky="n", padx=40)
frame_central.grid_propagate(False)

label_foto_capturada = tk.Label(frame_central, bg="#1c1c1e", width=320, height=240)
label_foto_capturada.pack(pady=(30, 20), padx=25)


label_emocion = tk.Label(frame_central, text="Emoción:", font=("Segoe UI", 18, "bold"),
                         fg="white", bg="#1c1c1e", wraplength=460, anchor="w", justify="left")
label_emocion.pack(pady=(0, 10), fill="x", padx=20)

label_personaje = tk.Label(frame_central, text="Personaje:", font=("Segoe UI", 13),
                           fg="#cccccc", bg="#1c1c1e", wraplength=460, anchor="w", justify="left")
label_personaje.pack(pady=(0, 20), fill="x", padx=20)

# Panel derecho - Estilos (más grande y centrado)
frame_estilos = tk.Frame(frame_principal, bg="#1c1c1e", width=300, height=500)
frame_estilos.grid(row=1, column=2, sticky="n", padx=(20, 30), pady=(60, 0))
frame_estilos.grid_propagate(False)

label_estilos = tk.Label(
    frame_principal,
    text="Escoger estilo",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#121212",
    anchor="w"
)
label_estilos.grid(row=1, column=2, sticky="n", padx=(0, 0), pady=(0, 120))

# Barra de progreso centrada bajo el panel central
progress_bar = ttk.Progressbar(frame_principal, mode="indeterminate", length=300)
progress_bar.grid(row=2, column=1, pady=(20, 10))  # Centrado debajo del panel central
progress_bar.grid_remove()

def aplicar_estilo_desde_boton(ruta_estilo):
    ruta_contenido = "resultado_faceswap.jpg"
    salida_estilizada = "resultado_estilizado.jpg"

    emocion_anterior = label_emocion.cget("text")
    personaje_anterior = label_personaje.cget("text")

    label_emocion.config(
        text="Aplicando estilo...",
        font=("Segoe UI", 12, "italic"),
        fg="#cccccc",
        anchor="center",
        justify="center"
    )
    label_personaje.config(text="")
    label_foto_capturada.config(image=None)
    label_foto_capturada.image = None

    progress_bar.grid(row=2, column=1, pady=(20, 10))
    progress_bar.start()
    ventana.update_idletasks()

    def procesar():
        try:
            if ruta_estilo.startswith("feedforward_"):
                estilo = ruta_estilo.split("_")[1]
                modulo_path = f"estilos_feedforward.{estilo}.aplicar_estilo_{estilo}"
                import importlib
                modulo = importlib.import_module(modulo_path)
                funcion = getattr(modulo, f"aplicar_estilo_{estilo}")
                funcion(ruta_contenido, salida_estilizada)
            else:
                from estilo_nst import aplicar_estilizado_nst
                aplicar_estilizado_nst(ruta_contenido, ruta_estilo, salida_estilizada)

            if os.path.exists(salida_estilizada):
                ventana.after(0, lambda: mostrar_foto_capturada(salida_estilizada))
                ventana.after(0, lambda: label_emocion.config(
                    text=emocion_anterior,
                    font=("Segoe UI", 18, "bold"),
                    anchor="w",
                    justify="left"
                ))
                ventana.after(0, lambda: label_personaje.config(text=personaje_anterior))
                ventana.after(0, lambda: boton_guardar.pack(pady=(10, 20), anchor="w", padx=12))
            else:
                ventana.after(0, lambda: label_emocion.config(text="No se pudo aplicar el estilo."))
        except Exception as e:
            print(f" Error al aplicar el estilo: {e}")
            import traceback
            traceback.print_exc()
            ventana.after(0, lambda: label_emocion.config(text="Error al aplicar el estilo."))
        finally:
            ventana.after(0, lambda: progress_bar.stop())
            ventana.after(0, lambda: progress_bar.grid_remove())

    threading.Thread(target=procesar, daemon=True).start()


estilos = [
    ("Fantasía", "estilos/fantasia.jpg"),
    ("Terror", "estilos/terror.png"),
    ("Aventura", "estilos/aventura.jpg"),
    ("Drama", "estilos/drama.jpg"),
    ("Crimen", "estilos/crimen.png"),
    ("Comedia", "estilos/comedia.png")]


# Contenedor centrado para los botones
contenedor_botones = tk.Frame(frame_estilos, bg="#1c1c1e")
contenedor_botones.pack(expand=True)

for i, (nombre, ruta) in enumerate(estilos):
    boton = tk.Button(
        contenedor_botones,
        text=nombre,
        command=lambda r=ruta: aplicar_estilo_desde_boton(r),
        bg="#6c63ff",
        fg="white",
        activebackground="#574fcf",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        width=12,
        height=2,
        bd=0,
        relief="flat",
        cursor="hand2"
    )
    fila = i // 2
    columna = i % 2
    boton.grid(row=fila, column=columna, padx=12, pady=10)


# 2. BOTÓN DE GUARDAR - ¡fuera del contenedor!
# Crear el botón pero NO lo mostramos todavía
boton_guardar = tk.Button(
    frame_estilos,
    text="💾",
    command=guardar_imagen_final,
    bg="#574fcf",
    fg="#cccccc",
    activebackground="#1c1c1e",
    activeforeground="white",
    font=("Segoe UI", 10, "bold"),
    bd=0,
    relief="flat",
    cursor="hand2"
)

# Ocultarlo al inicio
boton_guardar.pack_forget()


# INICIAR CÁMARA (se asegura de iniciar después de crear todo)
camara = cv2.VideoCapture(0)

def iniciar_video_si_camara_funciona():
    if camara.isOpened():
        actualizar_video()
    else:
        messagebox.showerror("Error", "No se pudo acceder a la cámara.")

# Forzar cierre seguro
def cerrar_ventana():
    try:
        if camara and camara.isOpened():
            camara.release()
        ventana.destroy()
    except Exception as e:
        print(f"Error al cerrar: {e}")
        os._exit(0)

ventana.after(100, iniciar_video_si_camara_funciona)
ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)
ventana.mainloop()
