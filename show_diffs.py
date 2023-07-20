import tkinter as tk
from tkinter import filedialog


def mostrar_diferencias(diferencias, grupos_restantes1, grupos_restantes2, grupos1, grupos2):
    ventana = tk.Toplevel()
    ventana.title("Diferencias entre grupos de líneas que inician con 551")
    ventana.geometry("1080x720")

    def buscar_texto(event):
        texto_buscar = entry_buscar.get()
        resaltar_texto(texto_buscar)

    def resaltar_texto(texto_buscar):
        # Eliminar el resaltado anterior
        texto_diferencias.tag_remove("encontrado_texto", "1.0", tk.END)

        if texto_buscar:
            indice = "1.0"
            while True:
                indice = texto_diferencias.search(texto_buscar, indice, nocase=True, stopindex=tk.END)
                if not indice:
                    break
                fin_indice = f"{indice}+{len(texto_buscar)}c"
                texto_diferencias.tag_add("encontrado_texto", indice, fin_indice)
                indice = fin_indice
        # Aplicar color al resaltado del texto encontrado
        texto_diferencias.tag_config("encontrado_texto", background="yellow", foreground="black")


    # Variable para mantener el estado del resaltado del símbolo |
    global resaltado_simbolo
    resaltado_simbolo = False

    def buscar_simbolo():
        global resaltado_simbolo

        if resaltado_simbolo:
            # Si el símbolo ya está resaltado, eliminar el resaltado
            texto_diferencias.tag_remove("encontrado_simbolo", "1.0", tk.END)
            resaltado_simbolo = False
        else:
            # Si el símbolo no está resaltado, realizar la búsqueda y resaltado
            resaltar_simbolo()
            resaltado_simbolo = True

    def resaltar_simbolo():
        texto_diferencias.tag_remove("encontrado_simbolo", "1.0", tk.END)
        indice = "1.0"
        while True:
            indice = texto_diferencias.search("|", indice, nocase=True, stopindex=tk.END)
            if not indice:
                break
            fin_indice = f"{indice}+1c"
            texto_diferencias.tag_add("encontrado_simbolo", indice, fin_indice)
            indice = fin_indice
        # Aplicar color al resaltado del símbolo encontrado
        texto_diferencias.tag_config("encontrado_simbolo", background="#95A0DB", foreground="black")


    # Función para guardar el contenido en un archivo
    def guardar_contenido():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            contenido = texto_diferencias.get("1.0", tk.END)
            with open(file_path, "w") as file:
                file.write(contenido)

    # Crear el widget de desplazamiento vertical
    scroll_y = tk.Scrollbar(ventana)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    texto_diferencias = tk.Text(ventana, yscrollcommand=scroll_y.set)
    texto_diferencias.pack(fill=tk.BOTH, expand=True)

    # Configurar la barra de desplazamiento
    scroll_y.config(command=texto_diferencias.yview)

    # Frame para contener los widgets de búsqueda y guardar y resaltar
    control_frame = tk.Frame(ventana)
    control_frame.pack(pady=5)


    # Cuadro de entrada y botón de búsqueda
    entry_buscar = tk.Entry(control_frame, width=30)
    entry_buscar.grid(row=0, column=1, padx=5)
    
    
    btn_buscar = tk.Button(
        control_frame, text="🔎 Buscar")
    btn_buscar.grid(row=0, column=2, padx=5)
    btn_buscar.bind("<Button-1>",  buscar_texto)
    entry_buscar.bind("<Return>", buscar_texto)

    # Botón para guardar contenido en un archivo
    btn_guardar = tk.Button(control_frame, text="Exportar 💾",
                            command=guardar_contenido)
    btn_guardar.grid(row=0, column=3, padx=5)

    # Botón para resaltar |
    btn_guardar = tk.Button(control_frame, text="Resaltar |", command=buscar_simbolo)#,
    btn_guardar.grid(row=0, column=4, padx=5)

    # Mostrar las diferencias grupo por grupo
    for clave, grupo1, grupo2 in diferencias:
        # Verificar si el grupo actual está en grupos_restantes1 o grupos_restantes2
        if clave not in grupos_restantes1 and clave not in grupos_restantes2:
            texto_diferencias.insert(tk.END, f"Grupo {clave}:\n")
            texto_diferencias.insert(tk.END, "| Archivo 1 |:\n")
            suma_campo8_grupo1 = 0.0
            suma_campo9_grupo1 = 0.0
            suma_campo10_grupo1 = 0.0
            suma_campo13_grupo1 = 0.0

            for linea in grupo1:
                texto_diferencias.insert(tk.END, f"{linea}\n", "archivo1")
                campos = linea.strip().split("|")
                suma_campo8_grupo1 += float(campos[7])
                suma_campo9_grupo1 += float(campos[8])
                suma_campo10_grupo1 += float(campos[9])
                suma_campo13_grupo1 += float(campos[12])
                campo_11 = campos[11]

            texto_diferencias.insert(
                tk.END, f"Suma Cantidad UMC: {round(suma_campo8_grupo1,3)}\n")
            texto_diferencias.insert(
                tk.END, f"Suma Valor Comercial: {round(suma_campo10_grupo1,3)}\n")
            texto_diferencias.insert(
                tk.END, f"Suma Monto: {round(suma_campo9_grupo1,2)}\n")
            texto_diferencias.insert(
                tk.END, f"Suma UMT: {round(suma_campo13_grupo1,5)}\n")
            texto_diferencias.insert(
                tk.END, f"UMC: {campo_11}\n")
            texto_diferencias.insert(
                tk.END, f"-" * 30)
            texto_diferencias.insert(
                tk.END, f"\n")

            texto_diferencias.insert(tk.END, "| Archivo 2 |:\n")

            suma_campo8_grupo2 = 0.0
            suma_campo9_grupo2 = 0.0
            suma_campo10_grupo2 = 0.0
            suma_campo13_grupo2 = 0.0

            for linea in grupo2:
                texto_diferencias.insert(tk.END, f"{linea}\n", "archivo2")
                campos = linea.strip().split("|")
                suma_campo8_grupo2 += float(campos[7])
                suma_campo9_grupo2 += float(campos[8])
                suma_campo10_grupo2 += float(campos[9])
                suma_campo13_grupo2 += float(campos[12])
                campo_11 = campos[11]

            texto_diferencias.insert(
                tk.END, f"Suma Cantidad UMC: {round(suma_campo8_grupo2,3)}\n")
            texto_diferencias.insert(
                tk.END, f"Suma Valor Comercial: {round(suma_campo10_grupo2,3)}\n")
            texto_diferencias.insert(
                tk.END, f"Suma Monto: {round(suma_campo9_grupo2,2)}\n")
            texto_diferencias.insert(
                tk.END, f"Suma UMT: {round(suma_campo13_grupo2,5)}\n")
            texto_diferencias.insert(
                tk.END, f"UMC: {campo_11}\n")
            texto_diferencias.insert(
                tk.END, f"-" * 130)
            texto_diferencias.insert(
                tk.END, f"\n")

            texto_diferencias.insert(tk.END, "\n")

    # Mostrar los grupos restantes del archivo 1
    if grupos_restantes1:
        texto_diferencias.insert(tk.END, "Grupos restantes en archivo 1:\n")
        for grupo in grupos_restantes1:
            texto_diferencias.insert(tk.END, f"Grupo {grupo}:\n")
            suma_campo8 = 0.0
            suma_campo9 = 0.0
            suma_campo10 = 0.0
            suma_campo13 = 0.0

            for linea in grupos1[grupo]:
                texto_diferencias.insert(
                    tk.END, f"{linea}\n", "restante_archivo1")
                campos = linea.strip().split("|")
                suma_campo8 += float(campos[7])
                suma_campo9 += float(campos[8])
                suma_campo10 += float(campos[9])
                suma_campo13 += float(campos[12])
                campo_11 = campos[11]
            texto_diferencias.insert(
                tk.END, f"Suma Cantidad UMC: {round(suma_campo8,3)}\n")
            texto_diferencias.insert(
                tk.END, f"Suma Valor Comercial: {round(suma_campo10,3)}\n")
            texto_diferencias.insert(tk.END, f"Suma Monto: {round(suma_campo9,2)}\n")
            texto_diferencias.insert(tk.END, f"Suma UMT: {round(suma_campo13,5)}\n")

            texto_diferencias.insert(
                tk.END, f"UMC: {campo_11}\n")
            texto_diferencias.insert(
                tk.END, f"-" * 30)
            texto_diferencias.insert(
                tk.END, f"\n")
            texto_diferencias.insert(tk.END, "\n")
    # Mostrar los grupos restantes del archivo 2
    if grupos_restantes2:
        texto_diferencias.insert(tk.END, "Grupos restantes en archivo 2:\n")
        for grupo in grupos_restantes2:
            texto_diferencias.insert(tk.END, f"Grupo {grupo}:\n")
            suma_campo8 = 0.0
            suma_campo9 = 0.0
            suma_campo10 = 0.0
            suma_campo13 = 0.0

            for linea in grupos2[grupo]:
                texto_diferencias.insert(
                    tk.END, f"{linea}\n", "restante_archivo2")
                campos = linea.strip().split("|")
                suma_campo8 += float(campos[7])
                suma_campo9 += float(campos[8])
                suma_campo10 += float(campos[9])
                suma_campo13 += float(campos[12])
                campo_11 = campos[11]
            texto_diferencias.insert(
                tk.END, f"Suma Cantidad UMC: {round(suma_campo8,3)}\n")
            texto_diferencias.insert(
                tk.END, f"Suma Valor Comercial: {round(suma_campo10,3)}\n")
            texto_diferencias.insert(tk.END, f"Suma Monto: {round(suma_campo9,2)}\n")
            texto_diferencias.insert(tk.END, f"Suma UMT: {round(suma_campo13,5)}\n")
            texto_diferencias.insert(
                tk.END, f"UMC: {campo_11}\n")
            texto_diferencias.insert(
                tk.END, f"-" * 130)
            texto_diferencias.insert(
                tk.END, f"\n")
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
        
    # Llamar a ambas funciones de búsqueda para resaltar al mismo tiempo
    buscar_texto(None)
    #buscar_simbolo()

    ventana.mainloop()

    

