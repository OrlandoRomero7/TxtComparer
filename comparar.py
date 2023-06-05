import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
from collections import defaultdict
from itertools import zip_longest
# --Create the main window# ------------------------------------------------------------------------------
window = ctk.CTk()
window.title("My Application")
window.geometry("800x475")
# window.configure(bg="#4D5057")
window.resizable(False, False)
# ------------------------------------------------------------------------------

frame = ctk.CTkFrame(window, width=800, height=475, fg_color="#4D5057")
frame.place(x=0, y=0)

# --ENCABEZADO------------------------------------------------------------------
# Create two labels
label1 = ctk.CTkLabel(window, text="TXT", fg_color="#4D5057",
                      text_color="#A5DE37", font=("Cascadia Code", 20, "bold"))
label2 = ctk.CTkLabel(window, text="Comparer", fg_color="#4D5057",
                      text_color="white", font=("Cascadia Code", 20, "bold"))

window.update()  # Render the window

# Compute label coordinates
x_center = window.winfo_width() // 2
y_center = window.winfo_height() // 2  # 20 pixels below the top
# Place the labels
label1.place(x=x_center - label1.winfo_reqwidth(), y=10)
label2.place(x=x_center, y=10)
# ------------------------------------------------------------------------------


def close_app():
    window.destroy()
# ----------------------------------------------------------------------------


raw_add_first_icon = Image.open(
    r'assets/icons/AGREGAR1.png')

add_first_width, add_first_height = 80, 90
resized_add_first_icon = raw_add_first_icon.resize(
    (add_first_width, add_first_height))
converted_add_first_icon = ctk.CTkImage(resized_add_first_icon, size=(60, 60))


add_first_icon = ctk.CTkLabel(window, image=converted_add_first_icon,
                              text=None, fg_color="#4D5057")
add_first_icon.place(x=x_center-260, y=y_center-40)


# ----------------------------------------------------------------------------


separator = ctk.CTkFrame(window, width=115, height=2, fg_color="#787c7f")
separator.place(x=x_center-154, y=y_center-10)


# # ----------------------------------------------------------------------------
raw_add_second_icon = Image.open(
    r'assets/icons/AGREGAR2.png')

add_second_width, add_second_height = 80, 90
resized_add_second_icon = raw_add_second_icon.resize(
    (add_second_width, add_second_height))
converted_add_second_icon = ctk.CTkImage(
    resized_add_second_icon, size=(60, 60))


add_second_icon = ctk.CTkLabel(window, image=converted_add_second_icon,
                               text=None, fg_color="#4D5057")
add_second_icon.place(x=x_center, y=y_center-40)


# ----------------------------------------------------------------------------

second_separator = ctk.CTkFrame(
    window, width=115, height=2, fg_color="#787c7f")
second_separator.place(x=x_center+100, y=y_center-10)

# ----------------------------------------------------------------------------


raw_generate_icon = Image.open(
    r'assets/icons/COMPARAR.png')

generate_width, generate_height = 80, 90
resized_generate_icon = raw_generate_icon.resize(
    (generate_width, generate_height))
converted_generate_icon = ctk.CTkImage(
    resized_generate_icon, size=(60, 60))


generate_icon = ctk.CTkLabel(window, image=converted_generate_icon,
                             text=None, fg_color="#4D5057")
generate_icon.place(x=x_center+245, y=y_center-40)

# Funciones para seleccionar los archivos
# -----------------------------------------------------------------------------
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


def seleccionar_archivo2():
    global archivo2
    archivo2 = filedialog.askopenfilename(
        title="Seleccionar archivo 2", filetypes=(("Archivos de texto", "*"),))
    # Obtener el nombre del archivo
    global nombre_archivo1
    nombre_archivo1 = os.path.basename(archivo2)


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
                grupos1[datos[1]].append(linea.strip())

        for linea in f2:
            if linea.startswith('551'):
                datos = linea.strip().split('|')
                grupos2[datos[1]].append(linea.strip())

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

    mostrar_diferencias(diferencias, grupos_restantes1, grupos_restantes2)


def mostrar_diferencias(diferencias, grupos_restantes1, grupos_restantes2):
    ventana = tk.Toplevel()
    ventana.title("Diferencias entre grupos de líneas que inician con 551")
    ventana.geometry("800x400")

    # Crear el widget de desplazamiento vertical
    scroll_y = tk.Scrollbar(ventana)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    texto_diferencias = tk.Text(ventana, yscrollcommand=scroll_y.set)
    texto_diferencias.pack(fill=tk.BOTH, expand=True)

    # Configurar la barra de desplazamiento
    scroll_y.config(command=texto_diferencias.yview)

    # Mostrar las diferencias grupo por grupo
    for clave, grupo1, grupo2 in diferencias:
        # Verificar si el grupo actual está en grupos_restantes1 o grupos_restantes2
        if clave not in grupos_restantes1 and clave not in grupos_restantes2:
            texto_diferencias.insert(tk.END, f"Grupo {clave}:\n")
            texto_diferencias.insert(tk.END, "Archivo 1:\n")
            suma_campo8_grupo1 = 0.0
            suma_campo9_grupo1 = 0.0
            for linea in grupo1:
                texto_diferencias.insert(tk.END, f"{linea}\n", "archivo1")
                campos = linea.strip().split("|")
                suma_campo8_grupo1 += float(campos[7])
                suma_campo9_grupo1 += float(campos[8])
            texto_diferencias.insert(tk.END, f"Suma Cantidad UMC: {suma_campo8_grupo1}\n")
            texto_diferencias.insert(tk.END, f"Suma Monto: {suma_campo9_grupo1}\n")
            texto_diferencias.insert(tk.END, "Archivo 2:\n")

            suma_campo8_grupo2 = 0.0
            suma_campo9_grupo2 = 0.0
            for linea in grupo2:
                texto_diferencias.insert(tk.END, f"{linea}\n", "archivo2")
                campos = linea.strip().split("|")
                suma_campo8_grupo2 += float(campos[7])
                suma_campo9_grupo2 += float(campos[8])
            texto_diferencias.insert(tk.END, f"Suma Cantidad UMC: {suma_campo8_grupo2}\n")
            texto_diferencias.insert(tk.END, f"Suma Monto: {suma_campo9_grupo2}\n")

            
            texto_diferencias.insert(tk.END, "\n")



    # Mostrar los grupos restantes del archivo 1
    if grupos_restantes1:
        texto_diferencias.insert(tk.END, "Grupos restantes en archivo 1:\n")
        for grupo in grupos_restantes1:
            texto_diferencias.insert(tk.END, f"Grupo {grupo}:\n")
            suma_campo8 = 0.0
            suma_campo9 = 0.0
            for linea in grupos1[grupo]:
                texto_diferencias.insert(tk.END, f"{linea}\n", "restante_archivo1")
                campos = linea.strip().split("|")
                suma_campo8 += float(campos[7])
                suma_campo9 += float(campos[8])
            texto_diferencias.insert(tk.END, f"Suma Cantidad UMC: {suma_campo8}\n")
            texto_diferencias.insert(tk.END, f"Suma Monto: {suma_campo9}\n")
            texto_diferencias.insert(tk.END, "\n")

    # Mostrar los grupos restantes del archivo 2
    if grupos_restantes2:
        texto_diferencias.insert(tk.END, "Grupos restantes en archivo 2:\n")
        for grupo in grupos_restantes2:
            texto_diferencias.insert(tk.END, f"Grupo {grupo}:\n")
            suma_campo8 = 0.0
            suma_campo9 = 0.0
            for linea in grupos2[grupo]:
                texto_diferencias.insert(tk.END, f"{linea}\n", "restante_archivo2")
                campos = linea.strip().split("|")
                suma_campo8 += float(campos[7])
                suma_campo9 += float(campos[8])
            texto_diferencias.insert(tk.END, f"Suma Cantidad UMC: {suma_campo8}\n")
            texto_diferencias.insert(tk.END, f"Suma Monto: {suma_campo9}\n")
            texto_diferencias.insert(tk.END, "\n")

    # Configurar el estilo del texto
    texto_diferencias.tag_config("archivo1", background="lightgreen")
    texto_diferencias.tag_config("archivo2", background="pink")
    texto_diferencias.tag_config("restante_archivo1", background="tomato")
    texto_diferencias.tag_config("restante_archivo2", background="tomato")

    ventana.mainloop()


# ----------------------------------------------------------------------------
# Botones
# ----------------------------------------------------------------------------
select_file1_button = ctk.CTkButton(
    window, text="Archivo 1", command=seleccionar_archivo1, bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)
select_file1_button.place(x=x_center-287, y=y_center+50)

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
select_file2_button = ctk.CTkButton(
    window, text="Archivo 2", command=seleccionar_archivo2, bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)
select_file2_button.place(x=x_center-26, y=y_center+50)


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
compare_button = ctk.CTkButton(
    window, text="Comparar", command=comparar_archivos, bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)

compare_button.place(x=x_center+221, y=y_center+50)

# ----------------------------------------------------------------------------

# Start the main application loop
window.mainloop()
