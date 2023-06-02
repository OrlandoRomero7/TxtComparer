import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
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

#Funciones para seleccionar los archivos 
#-----------------------------------------------------------------------------

archivo1 = None
archivo2 = None

def seleccionar_archivo1():
    global archivo1
    archivo1 = filedialog.askopenfilename(title="Seleccionar archivo 1", filetypes=(("Archivos de texto", "*"),))

def seleccionar_archivo2():
    global archivo2
    archivo2 = filedialog.askopenfilename(title="Seleccionar archivo 2", filetypes=(("Archivos de texto", "*"),))
#------------------------------------------------------------------------------

ocurrencias_adicionales = []

#Funciones para comparar
def comparar_archivos():
    if archivo1 is None or archivo2 is None:
        messagebox.showerror("Error", "Debes seleccionar ambos archivos.")
        return

    lineas1 = []
    lineas2 = []

    with open(archivo1, 'r') as f1, open(archivo2, 'r') as f2:
        lineas1 = [linea.strip() for linea in f1 if linea.startswith('551')]
        lineas2 = [linea.strip() for linea in f2 if linea.startswith('551')]

    cantidad_lineas1 = len(lineas1)
    cantidad_lineas2 = len(lineas2)

    messagebox.showinfo("Comparación de archivos", f"Archivo 1 tiene {cantidad_lineas1} líneas que inician con '551'.\nArchivo 2 tiene {cantidad_lineas2} líneas que inician con '551'.")

    diferencias = []

    for i, (linea1, linea2) in enumerate(zip(lineas1, lineas2)):
        if linea1 != linea2:
            diferencias.append((i + 1, linea1, linea2))

    ocurrencias_adicionales1 = lineas1[len(diferencias):]
    ocurrencias_adicionales2 = lineas2[len(diferencias):]

    if ocurrencias_adicionales1:
        ocurrencias_adicionales.append(("Archivo 1", ocurrencias_adicionales1))

    if ocurrencias_adicionales2:
        ocurrencias_adicionales.append(("Archivo 2", ocurrencias_adicionales2))


    if len(diferencias) == 0:
        messagebox.showinfo("Comparación de archivos", "No se encontraron diferencias entre las líneas que inician con '551'.")
        return

    mostrar_diferencias(diferencias)

def mostrar_diferencias(diferencias):
    ventana = tk.Toplevel()
    ventana.title("Diferencias entre líneas que inician con 551")
    ventana.geometry("800x400")

    # Crear el widget de desplazamiento vertical
    scroll_y = tk.Scrollbar(ventana)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    texto_diferencias = tk.Text(ventana, yscrollcommand=scroll_y.set)
    texto_diferencias.pack(fill=tk.BOTH, expand=True)

    # Configurar la barra de desplazamiento
    scroll_y.config(command=texto_diferencias.yview)

    # Mostrar las diferencias línea por línea
    for linea, linea1, linea2 in diferencias:
        texto_diferencias.insert(tk.END, f"Línea {linea}:\n")
        texto_diferencias.insert(tk.END, f"Archivo 1: {linea1}\n", "archivo1")
        texto_diferencias.insert(tk.END, f"Archivo 2: {linea2}\n", "archivo2")
        texto_diferencias.insert(tk.END, "\n")

    # Mostrar las ocurrencias adicionales en rojo
    for archivo, ocurrencias in ocurrencias_adicionales:
        texto_diferencias.insert(tk.END, f"Ocurrencias adicionales en {archivo}:\n")
        for ocurrencia in ocurrencias:
            texto_diferencias.insert(tk.END, f"{ocurrencia}\n", "ocurrencia_adicional")

    # Configurar el estilo del texto
    texto_diferencias.tag_config("archivo1", background="lightgreen")
    texto_diferencias.tag_config("archivo2", background="pink")
    texto_diferencias.tag_config("ocurrencia_adicional", background="#CBD0E2")
    

    ventana.mainloop()
# ----------------------------------------------------------------------------   
#Botones
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
