import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
from collections import defaultdict
from itertools import zip_longest

# --Create the main window------------------------------------------------------------------------------
window = ctk.CTk()
window.iconbitmap(r'assets/icons/app.ico')
window.title("  Comparador")
window.geometry("800x475")
window.resizable(False, False)

frame = ctk.CTkFrame(window, fg_color="#4D5057")
# Utilizamos sticky="nsew" para anclar el marco en las cuatro direcciones (norte, sur, este, oeste)
frame.grid(row=0, column=0, sticky="nsew")

# Ajustamos la configuración de la fila 0 para que se expanda verticalmente
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
# --ENCABEZADO------------------------------------------------------------------

# Create two labels
label1 = ctk.CTkLabel(frame, text="TXT", fg_color="#4D5057",
                      text_color="#A5DE37", font=("Cascadia Code", 20, "bold"))
label2 = ctk.CTkLabel(frame, text="Comparador", fg_color="#4D5057",
                      text_color="white", font=("Cascadia Code", 20, "bold"))

label1.grid(row=0, column=2, sticky="w", padx=(0, 0), pady=2)
label2.grid(row=0, column=2, sticky="w", padx=(36, 0), pady=10)

# ------------------------------------------------------------------------------


# ----------------------------------------------------------------------------


raw_add_first_icon = Image.open(r'assets/icons/AGREGAR1.png')
add_first_width, add_first_height = 80, 90
resized_add_first_icon = raw_add_first_icon.resize(
    (add_first_width, add_first_height))
converted_add_first_icon = ctk.CTkImage(resized_add_first_icon, size=(60, 60))

add_first_icon = ctk.CTkLabel(
    frame, image=converted_add_first_icon, text=None, fg_color="#4D5057")
add_first_icon.grid(row=1, column=0, padx=(50, 0), pady=(110, 0))

# ----------------------------------------------------------------------------

separator = ctk.CTkFrame(frame, width=115, height=2, fg_color="#787c7f")
separator.grid(row=1, column=1, padx=(30, 0), pady=(130, 0), sticky="w")

# # ----------------------------------------------------------------------------

raw_add_second_icon = Image.open(r'assets/icons/AGREGAR2.png')
add_second_width, add_second_height = 80, 90
resized_add_second_icon = raw_add_second_icon.resize(
    (add_second_width, add_second_height))
converted_add_second_icon = ctk.CTkImage(
    resized_add_second_icon, size=(60, 60))

add_second_icon = ctk.CTkLabel(
    frame, image=converted_add_second_icon, text=None, fg_color="#4D5057")
add_second_icon.grid(row=1, column=2, pady=(110, 0))

# ----------------------------------------------------------------------------

second_separator = ctk.CTkFrame(
    frame, width=115, height=2, fg_color="#787c7f")
second_separator.grid(row=1, column=3, padx=(30, 0), pady=(130, 0), sticky="w")

# ----------------------------------------------------------------------------

raw_generate_icon = Image.open(r'assets/icons/COMPARAR.png')
generate_width, generate_height = 80, 90
resized_generate_icon = raw_generate_icon.resize(
    (generate_width, generate_height))
converted_generate_icon = ctk.CTkImage(resized_generate_icon, size=(60, 60))
generate_icon = ctk.CTkLabel(
    frame, image=converted_generate_icon, text=None, fg_color="#4D5057")
generate_icon.grid(row=1, column=4, padx=(50, 0), pady=(110, 0))

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

    mostrar_diferencias(diferencias, grupos_restantes1, grupos_restantes2)


def mostrar_diferencias(diferencias, grupos_restantes1, grupos_restantes2):
    ventana = tk.Toplevel()
    ventana.title("Diferencias entre grupos de líneas que inician con 551")
    ventana.geometry("800x400")

    # Función de búsqueda de texto
    def buscar_texto():
        texto_buscar = entry_buscar.get()
        texto_diferencias.tag_remove("encontrado", "1.0", tk.END)
        if texto_buscar:
            indice = "1.0"
            while True:
                indice = texto_diferencias.search(
                    texto_buscar, indice, stopindex=tk.END)
                if not indice:
                    break
                fin_indice = f"{indice}+{len(texto_buscar)}c"
                texto_diferencias.tag_add("encontrado", indice, fin_indice)
                indice = fin_indice

    # Crear el widget de desplazamiento vertical
    scroll_y = tk.Scrollbar(ventana)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    texto_diferencias = tk.Text(ventana, yscrollcommand=scroll_y.set)
    texto_diferencias.pack(fill=tk.BOTH, expand=True)

    # Configurar la barra de desplazamiento
    scroll_y.config(command=texto_diferencias.yview)

    # Cuadro de entrada y botón de búsqueda
    entry_buscar = tk.Entry(ventana, width=30)
    entry_buscar.pack(pady=5)
    btn_buscar = tk.Button(ventana, text="Buscar", command=buscar_texto)
    btn_buscar.pack()

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
            texto_diferencias.insert(
                tk.END, f"Suma Cantidad UMC: {suma_campo8_grupo1}\n")
            texto_diferencias.insert(
                tk.END, f"Suma Monto: {suma_campo9_grupo1}\n")
            texto_diferencias.insert(tk.END, "Archivo 2:\n")

            suma_campo8_grupo2 = 0.0
            suma_campo9_grupo2 = 0.0
            for linea in grupo2:
                texto_diferencias.insert(tk.END, f"{linea}\n", "archivo2")
                campos = linea.strip().split("|")
                suma_campo8_grupo2 += float(campos[7])
                suma_campo9_grupo2 += float(campos[8])
            texto_diferencias.insert(
                tk.END, f"Suma Cantidad UMC: {suma_campo8_grupo2}\n")
            texto_diferencias.insert(
                tk.END, f"Suma Monto: {suma_campo9_grupo2}\n")

            texto_diferencias.insert(tk.END, "\n")

    # Mostrar los grupos restantes del archivo 1
    if grupos_restantes1:
        texto_diferencias.insert(tk.END, "Grupos restantes en archivo 1:\n")
        for grupo in grupos_restantes1:
            texto_diferencias.insert(tk.END, f"Grupo {grupo}:\n")
            suma_campo8 = 0.0
            suma_campo9 = 0.0
            for linea in grupos1[grupo]:
                texto_diferencias.insert(
                    tk.END, f"{linea}\n", "restante_archivo1")
                campos = linea.strip().split("|")
                suma_campo8 += float(campos[7])
                suma_campo9 += float(campos[8])
            texto_diferencias.insert(
                tk.END, f"Suma Cantidad UMC: {suma_campo8}\n")
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
                texto_diferencias.insert(
                    tk.END, f"{linea}\n", "restante_archivo2")
                campos = linea.strip().split("|")
                suma_campo8 += float(campos[7])
                suma_campo9 += float(campos[8])
            texto_diferencias.insert(
                tk.END, f"Suma Cantidad UMC: {suma_campo8}\n")
            texto_diferencias.insert(tk.END, f"Suma Monto: {suma_campo9}\n")
            texto_diferencias.insert(tk.END, "\n")

    # Configurar el estilo del texto
    texto_diferencias.tag_config(
        "archivo1", background="lightgreen", font=("Roboto", 11))
    texto_diferencias.tag_config(
        "archivo2", background="pink", font=("Roboto", 11))
    texto_diferencias.tag_config(
        "restante_archivo1", background="tomato", font=("Roboto", 11))
    texto_diferencias.tag_config(
        "restante_archivo2", background="tomato", font=("Roboto", 11))
    texto_diferencias.tag_config(
        "encontrado", background="yellow", foreground="black")

    ventana.mainloop()


# Botones
# ----------------------------------------------------------------------------

select_file1_button = ctk.CTkButton(frame, text="Archivo 1", command=seleccionar_archivo1,
                                    bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)
select_file1_button.grid(row=2, column=0, padx=(50, 0), pady=(45, 0))

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
select_file2_button = ctk.CTkButton(frame, text="Archivo 2", command=seleccionar_archivo2,
                                    bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)
select_file2_button.grid(row=2, column=2, pady=(45, 0))

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
compare_button = ctk.CTkButton(frame, text="Comparar", command=comparar_archivos,
                               bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)
compare_button.grid(row=2, column=4, padx=(50, 0), pady=(45, 0))

# Start the main application loop
window.mainloop()
