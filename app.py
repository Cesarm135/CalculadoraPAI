import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import time
import customtkinter
from PIL import Image
import json
import os
app = customtkinter.CTk()

# Ajustes app
customtkinter.set_appearance_mode("System")
app.title("To-DoList PAI")
customtkinter.set_default_color_theme("blue")
app.configure(fg_color='gray88')
app.geometry("920x520")
app.minsize(width=920, height=520)
icono_ruta = Path(__file__).parent / "Media" / "icono.ico"
tareas_ruta = Path(__file__).parent / "Data" / "tareas.json"
app.after(201, lambda :app.iconbitmap(icono_ruta))
customtkinter.set_default_color_theme("green")

#Frame tarea principal
frameprincipal = customtkinter.CTkFrame(app)
frameprincipal.pack(fill="both", expand=True, padx=20, pady=20, anchor="nw")


#Tareas que hacer texto:
label1 = customtkinter.CTkLabel(frameprincipal, text="Tareas que hacer:", fg_color="transparent", text_color="black", anchor="nw", width=10, height=10, font=("Catamaran", 30))
label1.pack(padx=6, pady=6, fill="both")

#Añadir Tareas
tareaAANadir = ""
frameanadirtarea = customtkinter.CTkFrame(frameprincipal, fg_color="transparent")
frameanadirtarea.pack(padx=3, pady=3, anchor="nw")

#Imagen Añadir
addImage_ruta = Path(__file__).parent / "Media" / "add.png"
addImage = customtkinter.CTkImage(light_image=Image.open(addImage_ruta),
                                  dark_image=Image.open(addImage_ruta),
                                  size=(25, 25))

addImageLabel = customtkinter.CTkLabel(frameanadirtarea, image=addImage, text="")
addImageLabel.pack(side="left")

# Texto para añadir tarea
textotarea = customtkinter.CTkEntry(frameanadirtarea, placeholder_text="Escriba su tarea", font=("Catamaran", 12), height=25, fg_color="transparent")
textotarea.pack(side="left", padx= 3)



# Lista de tareas
listaTareas = customtkinter.CTkScrollableFrame(frameprincipal, fg_color="transparent")
listaTareas.pack(anchor="nw", fill="both")

def cargarTareas():
    if os.path.exists(tareas_ruta):  
        with open(tareas_ruta, "r") as file:
            try:
                tareas = json.load(file)
            except json.JSONDecodeError:
                tareas = []

        for tarea in tareas:
            mostrarTarea(tarea["tarea"], tarea["completada"])

def mostrarTarea(texto, completada):
    # Contenedor para la tarea
    tarea_frame = customtkinter.CTkFrame(listaTareas, fg_color="white", corner_radius=5)
    tarea_frame.pack(fill="x", pady=5, padx=10)

    # Checkbox
    checkbox = customtkinter.CTkCheckBox(
        tarea_frame, text="", command=lambda: actualizarTarea(texto, checkbox)
    )
    checkbox.pack(side="left", padx=5)
    if completada == "Completada":
        checkbox.select()
    else:
        checkbox.deselect()

# Tarea
    tarea_label = customtkinter.CTkLabel(
        tarea_frame, text=texto, font=("Catamaran", 12), text_color="black"
    )
    tarea_label.pack(side="left", padx=10)
# Función para actualizar el estado de una tarea
def actualizarTarea(texto, checkbox):
    # Leer archivo JSON
    if os.path.exists(tareas_ruta):
        with open(tareas_ruta, "r") as file:
            tareas = json.load(file)
    else:
        tareas = []

    # Actualizar el estado de la tarea correspondiente
    for tarea in tareas:
        if tarea["tarea"] == texto:
            tarea["completada"] = "Completada" if checkbox.get() else "Pendiente"
            break

    # Guardar los cambios en el archivo
    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)

# Función para añadir nueva tarea
def addTask():
    tareaAANadir = textotarea.get().strip()
    if not tareaAANadir:
        print("La tarea no puede estar vacía.")
        return

    fecha = "Sin definir"
    nueva_tarea = {
        "tarea": tareaAANadir,
        "fecha": fecha,
        "completada": "Pendiente"
    }

    # Leer archivo JSON
    try:
        with open(tareas_ruta, "r") as file:
            tareas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tareas = []

    # Añadir nueva tarea
    tareas.append(nueva_tarea)

    # Guardar en el archivo
    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)

    # Mostrar en la interfaz
    mostrarTarea(tareaAANadir, "Pendiente")

    # Limpiar entrada
    textotarea.delete(0, customtkinter.END)

# Botón para añadir tarea
buttonAddTask = customtkinter.CTkButton(
    frameanadirtarea, text="Añadir Tarea", command=addTask,
    width=30, height=25, fg_color="lime green", font=("Catamaran", 12)
)
buttonAddTask.pack(padx=4, anchor="n", side="left")

# Cargar tareas al iniciar
cargarTareas()

# Ejecutar la aplicación
app.mainloop()