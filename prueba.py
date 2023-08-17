import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter as ctk
from tkinter import filedialog
import os

def handle_drop(event):
    filepath = event.data.replace("{", "").replace("}", "")
    
    # Check if the dropped file has the desired extension (e.g., '.txt')
    desired_extension = '.txt'  # Change this to the desired extension
    if filepath.lower().endswith(desired_extension):
        entry.delete(0, tk.END)
        entry.insert(0, filepath)
    else:
        entry.delete(0, tk.END)
        entry.insert(0, "Archivo incorrecto. Debe ser de tipo {}".format(desired_extension))
    

def open_file_dialog():
    filepath = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filepath)

root = ctk.CTk()
root.title("Arrastrar y Soltar Archivos")

frame = ctk.CTkFrame(root)
frame.pack(padx=20, pady=20)

label = ctk.CTkLabel(frame, text="Arrastra y suelta un archivo aquí:")
label.pack()

entry = ctk.CTkEntry(frame)
entry.pack(fill=tk.X, padx=10, pady=10)

button_open = ctk.CTkButton(frame, text="Seleccionar archivo", command=open_file_dialog)
button_open.pack(fill=tk.X, padx=10, pady=5)

entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', handle_drop)

root.mainloop()
