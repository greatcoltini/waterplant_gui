import tkinter as tk
from tkinter import ttk

# reduce repeat code with this class
class Labelled_Lamp_Entry(tk.Entry):
    
    def __init__(self, parent, initial_value):
        tk.Entry.__init__(self, parent, selectborderwidth=2, width=30, justify="center")
        self.insert(0, initial_value)
        self.bind('<FocusIn>', lambda x: self.selection_range(0, tk.END))
        