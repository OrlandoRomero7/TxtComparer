import os
from collections import defaultdict
from tkinter import filedialog, messagebox
from show_diffs import mostrar_diferencias
import customtkinter as ctk
from CTkToolTip import *

archivo1 = None
archivo2 = None
grupos1 = defaultdict(list)
grupos2 = defaultdict(list)

# Variable global para almacenar el nombre del archivo anterior
nombre_archivo_anterior1 = ""
archivo_anterior1 = ""


def seleccionar_archivo1():
    global archivo1, nombre_archivo_anterior1, archivo_anterior1
    archivo1 = filedialog.askopenfilename(
        title="Seleccionar archivo 1", filetypes=(("Archivos de texto", "*"),))
    
    # Obtener el nombre del archivo
    global nombre_archivo1
    nombre_archivo1 = os.path.basename(archivo1)

    if len(nombre_archivo1) > 40:
        messagebox.showerror("Error", "No puedes agregar archivos con nombre muy largos.")
        archivo1 = archivo_anterior1
        return archivo_anterior1,nombre_archivo_anterior1
    else:
        if len(nombre_archivo1)==0:
            archivo1 = archivo_anterior1
            return archivo_anterior1,nombre_archivo_anterior1
        else:
            nombre_archivo_anterior1 = nombre_archivo1
            archivo_anterior1 = archivo1
            return archivo1,nombre_archivo1

# Variable global para almacenar el nombre del archivo anterior
nombre_archivo_anterior2 = ""
archivo_anterior2 = ""

def seleccionar_archivo2():
    global archivo2,nombre_archivo_anterior2, archivo_anterior2
    archivo2 = filedialog.askopenfilename(
        title="Seleccionar archivo 2", filetypes=(("Archivos de texto", "*"),))
    
    # Obtener el nombre del archivo
    global nombre_archivo2
    nombre_archivo2 = os.path.basename(archivo2)

    if len(nombre_archivo2) > 40:
        messagebox.showerror("Error", "No puedes agregar archivos con nombre muy largos.")
        archivo2 = archivo_anterior2
        return archivo_anterior2,nombre_archivo_anterior2
    else:
        if len(nombre_archivo2) == 0:
            
            archivo2 = archivo_anterior2
            return archivo_anterior2,nombre_archivo_anterior2
        else:
            nombre_archivo_anterior2 = nombre_archivo2
            archivo_anterior2 = archivo2
            return archivo2, nombre_archivo2


def comparar_archivos(nombre1,nombre2,archivo1_log_frame,archivo2_log_frame):
    if archivo1 is None or archivo2 is None or archivo1 == "" or archivo2 == "":
        messagebox.showerror("Error", "Debes seleccionar ambos archivos.")
        return
    global grupos1, grupos2
    grupos1 = defaultdict(list)
    grupos2 = defaultdict(list)

    with open(archivo1, 'r') as f1, open(archivo2, 'r') as f2:
        for linea in f1:
            if linea.startswith('551'):
                datos = linea.strip().split('|')
                grupos1[datos[2]].append(linea.strip())

        for linea in f2:
            if linea.startswith('551'):
                datos = linea.strip().split('|')
                grupos2[datos[2]].append(linea.strip())

    diferencias = []

    for clave in set(grupos1.keys()) | set(grupos2.keys()):
        if clave in grupos1 and clave in grupos2:
            if grupos1[clave] != grupos2[clave]:
                diferencias.append((clave, grupos1[clave], grupos2[clave]))
        elif clave in grupos1:
            diferencias.append((clave, grupos1[clave], []))
        else:
            diferencias.append((clave, [], grupos2[clave])
                               ) if clave in grupos2 else None

    grupos_restantes1 = [
        grupo for grupo in grupos1.keys() if grupo not in grupos2]
    grupos_restantes2 = [
        grupo for grupo in grupos2.keys() if grupo not in grupos1]

    if len(diferencias) == 0 and len(grupos_restantes1) == 0 and len(grupos_restantes2) == 0:
        messagebox.showinfo("Comparación de archivos",
                            "No se encontraron diferencias entre las líneas que inician con '551'.")
        return
        
    HISTORY_FILE1 = 'history_file1.txt'
    HISTORY_FILE2 = 'history_file2.txt'
    MAX_RECORDS = 100
    #-------------------------------------------------------

    # Leer el contenido actual del archivo si existe
    if os.path.exists(HISTORY_FILE1):
        with open(HISTORY_FILE1, 'r') as file:
            contenido_actual = file.read()
    else:
        contenido_actual = ''

    # Agregar las nuevas líneas al inicio del contenido
    contenido_nuevo = nombre1 + '\n' + contenido_actual

    # Limitar el archivo a un máximo de 100 registros
    contenido_nuevo = '\n'.join(contenido_nuevo.splitlines()[:MAX_RECORDS])

    with open(HISTORY_FILE1, 'w') as file:
        file.write(contenido_nuevo)

    display_history(archivo1_log_frame, HISTORY_FILE1)
    #---------------------------------------------------------------

    # Leer el contenido actual del archivo si existe
    if os.path.exists(HISTORY_FILE2):
        with open(HISTORY_FILE2, 'r') as file:
            contenido_actual2 = file.read()
    else:
        contenido_actual2 = ''

    # Agregar las nuevas líneas al inicio del contenido
    contenido_nuevo2 = nombre2 + '\n' + contenido_actual2

    # Limitar el archivo a un máximo de 100 registros
    contenido_nuevo2 = '\n'.join(contenido_nuevo2.splitlines()[:MAX_RECORDS])
    
    with open(HISTORY_FILE2, 'w') as file:
        file.write(contenido_nuevo2)

    display_history(archivo2_log_frame,HISTORY_FILE2)
    #--------------------------------------------------------------------
    mostrar_diferencias(diferencias, grupos_restantes1,
                        grupos_restantes2, grupos1, grupos2)
    


def display_history(frame, history_file):
    # First, clear existing labels
    for widget in frame.winfo_children():
        widget.destroy()

    # If history file exists, read and display
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:  # Ignore empty lines
                    if len(line) > 12:
                        label = ctk.CTkLabel(
                            frame, text=line[:12]+"...", fg_color="#B0B0B0", text_color="#1f6aa5")
                        label.pack()
                        CTkToolTip(label, message=line)
                    else:
                        label = ctk.CTkLabel(
                            frame, text=line, fg_color="#B0B0B0", text_color="#1f6aa5")
                        label.pack()

    
