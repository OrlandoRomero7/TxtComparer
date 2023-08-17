import tkinter as tk
from pandastable import Table
import pandas as pd
from tkinter import filedialog



def mostrar_tabla(documentos,fracciones,nicos,valor_dolares,cantidad_comercial,array_tipo_movimiento,unidades_medida_com,uds_medida_tar):
    
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
    'Valor Dolares': valor_dolares,
    'Cantidad Comercial': cantidad_comercial,
    'Unidad Medida Comercial': unidades_medida_com,
    'Unidad Medida Tarifa': uds_medida_tar
    })

    # Ajustar el ancho de las columnas en el DataFrame
    # Puedes ajustar los valores de ancho como desees
    column_widths = {'Documento': 10,
                     'Tipo Movimiento': 10,
                     'Fraccion': 10,
                     'Nico': 5,
                     'Valor Dolares': 10,
                     'Cantidad Comercial': 10,
                     'Unidad Medida Comercial': 15,
                     'Unidad Medida Tarifa': 15
                     
                     
                     }

    for column, width in column_widths.items():
        df[column] = df[column].apply(lambda x: f'{{:<{width}}}'.format(x))

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
    

