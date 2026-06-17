# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 09:59:12 2025

@author: DanielJackson
"""

"""
Making a GUI
"""

#import Load_plot_h5s #C:/Users/DanielJackson/Documents/GitHub/h5_files
#import os
import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Simple UI")
root.geometry("300x200")

# Function to display a message
def show_message():
    messagebox.showinfo("Message", "Hello, Tkinter!")
    
# Function to run a script
def run_script():
    file_path = 'C:/Users/DanielJackson/Documents/GitHub/h5_files/Load_plot_h5s.py'
    with open(file_path, 'r') as file:
        code = file.read()
        exec(code)
        
# Create a label
label = tk.Label(root, text="Plot the data")
label.pack(pady=10)

# Create a button
button = tk.Button(root, text="Click Me", command=run_script)
button.pack(pady=10)

# Run the application
root.mainloop()