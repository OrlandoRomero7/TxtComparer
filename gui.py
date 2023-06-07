
import customtkinter as ctk
from PIL import Image
from functions import seleccionar_archivo1, seleccionar_archivo2, comparar_archivos

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
