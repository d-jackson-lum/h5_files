# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 14:36:15 2025

@author: DanielJackson
"""

from tkinter import *
from tkinter import messagebox, simpledialog, ttk, filedialog
import lumicks.pylake as lk
from h5_functions import Get_All_Slices, Get_Slices


# Function for opening the 
# file explorer window
def browseFiles():
    global filepath
    filepath = filedialog.askopenfilename(initialdir = "C:/Users/DanielJackson/Documents/Service/BA003_HQ/25.02.19_PI_Nanostage_Tests/Stuck_bead/",
										title = "Select a File",
										filetypes = (("h5 files", "*.h5*"), ("all files", "*.*")))
    # Change label contents
    label_file_explorer.configure(text="Loaded: " + filepath)
    get_file()

def browse_folder():
    folder_path = filedialog.askdirectory()
    print(f"Selected Folder: {folder_path}")
    return folder_path

def get_file():
    file_ID = filepath.split('.')[0]
    global file
    file = lk.File(filepath)
    global Channels
    Slices, Channels, checker = Get_Slices(file, "")
    channeled['values'] = Channels
    print("File loaded succesfully.")
    
def pick_channel(event):
    global Data_Channel
    Data_Channel = channeled.get()
    print(f"Selected channel: {Data_Channel}")
    global Slices
    Slices, Channels, checker = Get_Slices(file, Data_Channel)
    Slices.append('All Slices')
    sliced['values'] = Slices
    #print(Slices)

def pick_slice(Data_Channel):
    global Slice
    Slice = sliced.get()
    print(f"Selected slice: {Slice}")
    #print(Slice)
	
def plotting_script():
    #show_message()
    file_path = 'C:/Users/DanielJackson/Documents/GitHub/h5_files/Load_plot_h5s.py'
    with open(file_path, 'r') as file:
        code = file.read()
        exec(code)
																							
# Create the root window
window = Tk()
window.title('File Explorer')
window.geometry("750x500")
window.config(background = "white")

row_weight = 2
label_weight = 1
col_weight = 1

window.rowconfigure(0, weight=label_weight)
window.rowconfigure(1, weight=row_weight)
window.rowconfigure(2, weight=label_weight)
window.rowconfigure(3, weight=row_weight)
window.rowconfigure(4, weight=label_weight)
window.rowconfigure(5, weight=row_weight)
window.rowconfigure(6, weight=row_weight)
window.columnconfigure(0, weight=col_weight)
window.columnconfigure(1, weight=col_weight)
window.columnconfigure(2, weight=col_weight)
#window.columnconfigure(3, weight=col_weight)
#window.columnconfigure(4, weight=col_weight)
#window.columnconfigure(5, weight=col_weight)

# Create a File Explorer label
label_file_explorer = Label(window,text = "Load and Plot h5 Files", height = 4, fg = "blue")#, width = 100)
button_explore = Button(window, text = "Browse Files",command = browseFiles)  
#button_loader = Button(window, text = "Load File", command = get_file)
button_plotter = Button(window, text="Plot Data", command=plotting_script)

label_channel = Label(window, text="Select data channel")
channeled = ttk.Combobox(window)
channeled.bind("<<ComboboxSelected>>", pick_channel)
label_slice = Label(window, text="Select data slice")
sliced = ttk.Combobox(window)
sliced.bind("<<ComboboxSelected>>", pick_slice)

label_file_explorer.grid(column = 0, row = 0, columnspan=3, sticky=EW)
button_explore.grid(column = 1, row = 1)
#button_loader.grid(column = 1,row = 2)
label_channel.grid(column = 1, row = 2)
channeled.grid(column = 1,row = 3)
label_slice.grid(column = 1, row = 4)
sliced.grid(column = 1,row = 5)
button_plotter.grid(column = 1,row = 6)
# Let the window wait for any events
window.mainloop()