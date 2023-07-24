import tkinter as tk
from pandastable import Table
import pandas as pd

df = pd.DataFrame({
    'A': [1,2,3,4,5,6,],
    'B': [1,1,2,2,3,3,],
    'C': [1,2,3,1,2,3,],
    'D': [1,1,1,2,2,2,],
})

root = tk.Tk()
root.title('PandasTable Example')

frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

pt = Table(frame, dataframe=df)
pt.show()

pt.columncolors['A'] = 'red'
pt.columncolors['B'] = 'green'

root.mainloop()
