# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 10:26:25 2025

@author: DanielJackson
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import lumicks.pylake as lk
from h5_functions import Get_All_Slices, Get_Slices

global global_test
global_test = "testing, testing, 1, 2, 3"

Channel_input = ""
global Slices
global Channels
global checker
global folder_path


#Choosing the desired file
folder_path = 'C:/Users/DanielJackson/Documents/Service/BA003_HQ/25.02.19_PI_Nanostage_Tests/Stuck_bead/'
#'C:/Users/DanielJackson/Downloads/'
file_name = 'Stuck_bead_2nd_min_378fps.h5'

file_ID = file_name.split('.')[0]
file = lk.File(folder_path + file_name)

Slices, Channels, checker = Get_Slices(file, Channel_input)
Data_options = Get_All_Slices(file)
print(Data_options)
print(Channels)
#print(Data_options)

def popup_selection():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    options = ["Option 1", "Option 2", "Option 3"]
    selection = simpledialog.askstring("Select an option", "Choose one:", initialvalue=options[0])

def on_select(event):
    global Data_Channel
    Data_Channel = channeled.get()
    print(f"Selected channel: {Data_Channel}")

def select_slice(Data_Channel):
    Slice = sliced.get()
    print(f"Selected slice: {Slice}")
    print(Slice)

# Function to display a message
def show_message():
    messagebox.showinfo("Message", "Hello, Tkinter!")
    
# Function to run a script
def run_script():
    #show_message()
    file_path = 'C:/Users/DanielJackson/Documents/GitHub/h5_files/Load_plot_h5s.py'
    with open(file_path, 'r') as file:
        code = file.read()
        exec(code)
    root.destroy()

def browse_folder():
    folder_path = filedialog.askdirectory()
    print(f"Selected Folder: {folder_path}")
    return folder_path


# Create the main window
root = tk.Tk()
root.title("Plotting Tweezer Data")
root.geometry("300x200")

folder_button = tk.Button(root, text="Browse", command=browse_folder)
folder_button.pack()

# Create a button
button = tk.Button(root, text="Plot Data", command=run_script)
button.pack(pady=20)

# Create a label
label = tk.Label(root, text="Select data channel")
label.pack(pady=2)

channeled = ttk.Combobox(root)
channeled['values'] = Channels
channeled.bind("<<ComboboxSelected>>", on_select)
channeled.pack(pady=10)

sliced = ttk.Combobox(root)
sliced['values'] = Slices
sliced.bind("<<ComboboxSelected>>", select_slice)
sliced.pack(pady=10)

# Run the application
root.mainloop()