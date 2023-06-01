import tkinter as tk
from tkinter import filedialog, messagebox
import difflib

def comparar_archivos():
    archivo1 = filedialog.askopenfilename(title="Seleccionar archivo 1", filetypes=(("Archivos de texto", "*.txt"),))
    archivo2 = filedialog.askopenfilename(title="Seleccionar archivo 2", filetypes=(("Archivos de texto", "*.txt"),))

    if archivo1 and archivo2:
        texto1 = ""
        texto2 = ""

        with open(archivo1, 'r') as f1, open(archivo2, 'r') as f2:
            texto1 = f1.read()
            texto2 = f2.read()

        diferencias = difflib.ndiff(texto1.splitlines(), texto2.splitlines())
        resultado = list(diferencias)
        diff_output = '\n'.join(resultado)

        cantidad_diferencias = sum(1 for linea in resultado if linea.startswith('- ') or linea.startswith('+ '))
        if cantidad_diferencias > 0:
            mostrar_diferencias(diff_output, cantidad_diferencias)
        else:
            messagebox.showinfo("Comparación de archivos", "No se encontraron diferencias.")

def mostrar_diferencias(diferencias, cantidad):
    ventana = tk.Toplevel()
    ventana.title("Diferencias entre archivos")
    ventana.geometry("800x400")

    texto_diferencias = tk.Text(ventana)
    texto_diferencias.pack(fill=tk.BOTH, expand=True)

    # Mostrar diferencias subrayadas
    texto_diferencias.insert(tk.END, diferencias)
    for i, linea in enumerate(diferencias.splitlines()):
        if linea.startswith('+'):
            texto_diferencias.tag_add("agregado", f"{i+1}.0", f"{i+1}.end")
            texto_diferencias.tag_config("agregado", background="lightgreen")
        elif linea.startswith('-'):
            texto_diferencias.tag_add("eliminado", f"{i+1}.0", f"{i+1}.end")
            texto_diferencias.tag_config("eliminado", background="pink")

    messagebox.showinfo("Comparación de archivos", f"Se encontraron {cantidad} diferencias.")

    ventana.mainloop()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Comparador de archivos")
ventana.geometry("300x150")

# Botón para seleccionar archivos
boton_seleccionar = tk.Button(ventana, text="Seleccionar archivos", command=comparar_archivos)
boton_seleccionar.pack(pady=20)

# Ejecutar la interfaz
ventana.mainloop()
