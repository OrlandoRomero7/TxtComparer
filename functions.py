import os
from collections import defaultdict
from tkinter import filedialog, messagebox
from show_diffs import mostrar_diferencias


archivo1 = None
archivo2 = None
grupos1 = defaultdict(list)
grupos2 = defaultdict(list)


def seleccionar_archivo1():
    global archivo1
    archivo1 = filedialog.askopenfilename(
        title="Seleccionar archivo 1", filetypes=(("Archivos de texto", "*"),))
    # Obtener el nombre del archivo
    global nombre_archivo1
    nombre_archivo1 = os.path.basename(archivo1)
    return archivo1, nombre_archivo1


def seleccionar_archivo2():
    global archivo2
    archivo2 = filedialog.askopenfilename(
        title="Seleccionar archivo 2", filetypes=(("Archivos de texto", "*"),))
    # Obtener el nombre del archivo
    global nombre_archivo1
    nombre_archivo1 = os.path.basename(archivo2)
    return archivo2, nombre_archivo1


def comparar_archivos():
    if archivo1 is None or archivo2 is None:
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

    mostrar_diferencias(diferencias, grupos_restantes1,
                        grupos_restantes2, grupos1, grupos2)
