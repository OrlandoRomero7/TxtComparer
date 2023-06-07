import tkinter as tk


def mostrar_diferencias(diferencias, grupos_restantes1, grupos_restantes2, grupos1, grupos2):
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
