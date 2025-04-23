# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 10:24:38 2025

@author: DanielJackson
"""

"""
Drop down menu
"""

import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_value = combo.get()
    print(f"Selected: {selected_value}")

root = tk.Tk()
root.title("Drop-down Menu Example")

combo = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
combo.bind("<<ComboboxSelected>>", on_select)
combo.pack(pady=20)

root.mainloop()

