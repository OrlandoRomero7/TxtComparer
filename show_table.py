import tkinter as tk
from pandastable import Table
import pandas as pd
from tkinter import filedialog



def mostrar_tabla(documentos,fracciones,nicos,cantidad_comercial,cantidad_tarifa,array_tipo_movimiento,unidades_medida):
    
    def export_data():
        # Abre un cuadro de diálogo para que el usuario elija la ubicación y el nombre del archivo
        archivo = filedialog.asksaveasfilename(parent=root,
                                            defaultextension=".xlsx",
                                            filetypes=[("Archivo Excel", "*.xlsx")],
                                            initialfile="Tabla")
        
        if archivo:
            # Exporta el DataFrame a Excel
            df.to_excel(archivo, index=False)  # Si quieres incluir el índice, cambia a index=True
            

    df = pd.DataFrame({
    'Documento': documentos,
    'Tipo Movimiento': array_tipo_movimiento,
    'Fraccion': fracciones,
    'Nico': nicos,
    'Cantidad Comercial': cantidad_comercial,
    'Cantidad Tarifa': cantidad_tarifa,
    'Unidad Medida': unidades_medida
    })

    root = tk.Toplevel()
    root.title('Tabla')
    root.geometry("800x400")

    frame = tk.Frame(root)
    frame.pack(fill='both',expand=True)

    pt = Table(frame, dataframe=df)
    pt.show()
    
    #pt.setRowColors(rows=0, clr='red', cols='all')
    button = tk.Button(root, text='Exportar 💾', command=export_data)
    button.pack()
    

    root.mainloop()
    

