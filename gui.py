import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from functions import seleccionar_archivo1, seleccionar_archivo2, comparar_archivos
from CTkToolTip import *
#from tktooltip import ToolTip
# --Create the main window------------------------------------------------------------------------------
window = ctk.CTk()
window.iconbitmap(r'assets/icons/app.ico')
window.title("  Comparador")
window.geometry("865x680")
window.resizable(False, False)

frame = ctk.CTkFrame(window, fg_color="#4D5057")
# Utilizamos sticky="nsew" para anclar el marco en las cuatro direcciones (norte, sur, este, oeste)
frame.grid(row=0, column=0, sticky="nsew")

# Ajustamos la configuración de la fila 0 para que se expanda verticalmente
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
# --*---------------------------------------------------------------------

archivo1_filename = ""
archivo2_filename = ""

file1_tooltip = None

def on_select_file1_button_pressed():
    global archivo1_filename,file1_tooltip
    archivo1,nombre_archivo1 = seleccionar_archivo1()
    archivo1_filename = nombre_archivo1

    """ if len(nombre_archivo1)>40:
        messagebox.showerror("Error", "No puedes agregar archivos con nombre muy largos.")
        return """

    if file1_tooltip:
        file1_tooltip.hide()

    # Usa el nombre del archivo para actualizar el texto del label
    if nombre_archivo1:
        if len(nombre_archivo1)>=12:
            archivo1_cargado.configure(
                text=nombre_archivo1[:9]+"...", text_color="#B7D47F", font=("Roboto", 12, "bold"))
            
            file1_tooltip = CTkToolTip(archivo1_cargado, message=nombre_archivo1)
        else:
            archivo1_cargado.configure(
                text=nombre_archivo1, text_color="#B7D47F", font=("Roboto", 12, "bold"))
    else:
        archivo1_cargado.configure(
            text="VACIO", text_color="#B7D47F", font=("Roboto", 12, "bold"))


file2_tooltip= None  

def on_select_file2_button_pressed():
    global archivo2_filename,nombre_archivo2,file2_tooltip
    archivo2, nombre_archivo2 = seleccionar_archivo2()
    archivo2_filename = nombre_archivo2
    # Usa el nombre del archivo para actualizar el texto del label

    """ if len(nombre_archivo2)>40:
        messagebox.showerror("Error", "No puedes agregar archivos con nombre muy largos.")
        return """
    
    if file2_tooltip:
        file2_tooltip.hide()

    if nombre_archivo2:
        if len(nombre_archivo2)>=12:
            archivo2_cargado.configure(
                text=nombre_archivo2[:9]+"...", text_color="#B7D47F", font=("Roboto", 12, "bold"))
            
            file2_tooltip = CTkToolTip(archivo2_cargado, message=nombre_archivo2)
        else:
            archivo2_cargado.configure(
                text=nombre_archivo2, text_color="#B7D47F", font=("Roboto", 12, "bold"))
    else:
        archivo2_cargado.configure(
            text="VACIO", text_color="#B7D47F", font=("Roboto", 12, "bold"))
    
# ------------------------------------------------------------------------------
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
add_first_icon.grid(row=1, column=0, padx=(30, 0), pady=(115, 0))

# ----------------------------------------------------------------------------

separator = ctk.CTkFrame(frame, width=115, height=2, fg_color="#787c7f")
separator.grid(row=1, column=1, padx=(30, 0), pady=(135, 0), sticky="w")

# # ----------------------------------------------------------------------------

raw_add_second_icon = Image.open(r'assets/icons/AGREGAR2.png')
add_second_width, add_second_height = 80, 90
resized_add_second_icon = raw_add_second_icon.resize(
    (add_second_width, add_second_height))
converted_add_second_icon = ctk.CTkImage(
    resized_add_second_icon, size=(60, 60))

add_second_icon = ctk.CTkLabel(
    frame, image=converted_add_second_icon, text=None, fg_color="#4D5057")
add_second_icon.grid(row=1, column=2, pady=(115, 0))

# ----------------------------------------------------------------------------

second_separator = ctk.CTkFrame(
    frame, width=115, height=2, fg_color="#787c7f")
second_separator.grid(row=1, column=3, padx=(30, 0), pady=(135, 0), sticky="w")

# ----------------------------------------------------------------------------

raw_generate_icon = Image.open(r'assets/icons/COMPARAR.png')
generate_width, generate_height = 80, 90
resized_generate_icon = raw_generate_icon.resize(
    (generate_width, generate_height))
converted_generate_icon = ctk.CTkImage(resized_generate_icon, size=(60, 60))
generate_icon = ctk.CTkLabel(
    frame, image=converted_generate_icon, text=None, fg_color="#4D5057")
generate_icon.grid(row=1, column=4, padx=(0, 20), pady=(115, 0))



################## Frame Historial ###########################################
log_frame_container = ctk.CTkFrame(
    frame, fg_color="#B0B0B0", border_color="#1f6aa5", border_width=3, width=560, height=110
)
log_frame_container.grid(row=4, column=1,
                         columnspan=3, pady=(40, 0), padx=(10, 0))


log_title = ctk.CTkLabel(log_frame_container, text="🕤 Historial", fg_color="#B0B0B0",
                         text_color="#1f6aa5", font=("Cascadia Code", 16, "bold"))
log_title.grid(row=0, column=0, sticky="nsew", padx=(100, 0), pady=(15, 0))


log_frame = ctk.CTkScrollableFrame(
    log_frame_container, fg_color="#B0B0B0",  border_width=0, width=500, height=80
)
log_frame.grid(row=1, column=0,
               columnspan=3, pady=(2, 0), padx=(5, 0))


archivo1_log_frame = ctk.CTkFrame(
    log_frame, fg_color="#B0B0B0",   border_width=0)
archivo1_log_frame.grid(row=1, column=1, sticky="nsew", padx=(50, 0), pady=1)

archivo2_log_frame = ctk.CTkFrame(
    log_frame, fg_color="#B0B0B0",  border_width=0)
archivo2_log_frame.grid(row=1, column=3, sticky="nsew", padx=(150, 0), pady=1) 


####################### Botones #################################
# ----------------------------------------------------------------------------

select_file1_button = ctk.CTkButton(frame, text="Archivo 1", command=on_select_file1_button_pressed,
                                    bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)
select_file1_button.grid(row=2, column=0, padx=(30, 0), pady=(50, 0))

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
select_file2_button = ctk.CTkButton(frame, text="Archivo 2", command=on_select_file2_button_pressed,
                                    bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)
select_file2_button.grid(row=2, column=2, pady=(50, 0))

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
compare_button = ctk.CTkButton(frame, text="Comparar", command=lambda: comparar_archivos(archivo1_filename,archivo2_filename,archivo1_log_frame,archivo2_log_frame),
                               bg_color="#4D5057", corner_radius=7, font=("Segoe UI", 15), width=114)
compare_button.grid(row=2, column=4, padx=(0, 20), pady=(50, 0))

#################### Indicador archivos cargados #####################################

# 
archivo1_cargado = ctk.CTkLabel(
    frame, text="VACIO", text_color="#B7D47F", font=("Roboto", 12, "bold"))
archivo1_cargado.grid(row=3, column=0, padx=(30, 0), pady=(10, 0))

archivo2_cargado = ctk.CTkLabel(
    frame, text="VACIO", text_color="#B7D47F", font=("Roboto", 12, "bold"))
archivo2_cargado.grid(row=3, column=2, pady=(10, 0))

################# Mostrar Hisotrial ################################################

HISTORY_FILE1 = 'history_file1.txt'
HISTORY_FILE2 = 'history_file2.txt'

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
                        

# ------------------------------------

# Display history when application starts
display_history(archivo1_log_frame, HISTORY_FILE1)
display_history(archivo2_log_frame, HISTORY_FILE2)

window.mainloop()
