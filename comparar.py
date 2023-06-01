import tkinter as tk
from tkinter import filedialog, messagebox

archivo1 = None
archivo2 = None

def seleccionar_archivo1():
    global archivo1
    archivo1 = filedialog.askopenfilename(title="Seleccionar archivo 1", filetypes=(("Archivos de texto", "*"),))

def seleccionar_archivo2():
    global archivo2
    archivo2 = filedialog.askopenfilename(title="Seleccionar archivo 2", filetypes=(("Archivos de texto", "*"),))

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

    # Configurar el estilo del texto
    texto_diferencias.tag_config("archivo1", background="lightgreen")
    texto_diferencias.tag_config("archivo2", background="pink")

    ventana.mainloop()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Comparador de líneas que inician con 551")
ventana.geometry("300x200")

# Botones para seleccionar archivos
boton_seleccionar1 = tk.Button(ventana, text="Seleccionar archivo 1", command=seleccionar_archivo1)
boton_seleccionar1.pack(pady=10)

boton_seleccionar2 = tk.Button(ventana, text="Seleccionar archivo 2", command=seleccionar_archivo2)
boton_seleccionar2.pack(pady=10)

boton_comparar = tk.Button(ventana, text="Comparar archivos", command=comparar_archivos)
boton_comparar.pack(pady=10)

# Ejecutar la interfaz
ventana.mainloop()
