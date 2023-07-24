import tkinter as tk
from pandastable import Table
import pandas as pd

def mostrar_tabla(documentos,fracciones,nicos,cantidad_comercial,cantidad_tarifa):
    #print("Documentos: ",documentos,"Fracciones: ",fracciones)
    df = pd.DataFrame({
    'Documento': documentos,
    'Tipo Movimiento': " ",
    'Fraccion': fracciones,
    'Nico': nicos,
    'Cantidad Comercial': cantidad_comercial,
    'Cantidad Tarifa': cantidad_tarifa,
    'Unidad Medida': " "
    })

    root = tk.Tk()
    root.title('PandasTable Example')

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=df)
    

    pt.show()
    pt.setRowColors(rows=0, clr='red', cols='all')
    

    root.mainloop()
    """ print("Documento1: ",documento1,"Fraccion1: ",fraccion1)
    print("Documento2: ",documento2,"Fraccion2: ",fraccion2) """

