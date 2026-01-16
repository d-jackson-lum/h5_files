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
    filepath = filedialog.askopenfilename(initialdir = "C:/Users/DanielJackson/Desktop/",
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
    global file
    global Channels
    file_ID = filepath.split('.')[0]
    file = lk.File(filepath)
    Slices, Channels, checker = Get_Slices(file, "")
    channeled['values'] = Channels
    print("File loaded succesfully.")
    
def pick_channel(event):
    global Data_Channel
    global Slices
    Data_Channel = channeled.get()
    print(f"Selected channel: {Data_Channel}")
    Slices, Channels, checker = Get_Slices(file, Data_Channel)
    Slices.append('All Slices')
    sliced['values'] = Slices
    #print(Slices)

def pick_slice(Data_Channel):
    global Slice
    Slice = sliced.get()
    print(f"Selected slice: {Slice}")
    check_check()
    #print(Slice)
	
def plotting_script():
    #show_message()
    file_path = 'C:/Users/DanielJackson/Documents/GitHub/h5_files/Load_plot_h5s.py'
    check_check()
    with open(file_path, 'r') as file:
        code = file.read()
        exec(code)

def check_fft():
    global check_fft_val
    global check_fit_val
    if fft_var.get():
        print('Will do!')
    else:
        print('Will not do.')
    check_fft_val = fft_var.get()
    check_fit_val = fit_var.get()
        
def check_fit():
    global check_fft_val
    global check_fit_val
    if fit_var.get():
        print('Will do!')
    else:
        print('Will not do.')
    check_fit_val = fit_var.get()
    check_fft_val = fft_var.get()

def check_check():
    global check_fft_val
    global check_fit_val
    check_fft_val = fft_var.get()
    check_fit_val = fit_var.get()
    
def Set_start_time():
    global Start_value
    global End_value
    Start_value = Start_spinbox.get()
    End_value = End_spinbox.get()
    print("Starting second for plot:", Start_value)
    if(Start_value>=End_value):
        start_plus_one = int(float(Start_value)+1)
        End_value =  str(start_plus_one)
        Set_end_time()

def Set_end_time():
    global End_value
    global Start_value
    End_value = End_spinbox.get()
    Start_value = Start_spinbox.get()
    print(End_value)
    if(Start_value>=End_value):
        start_plus_one = int(float(Start_value)+1)
        End_value =  str(start_plus_one) #f"{start_plus_one:.3f}"
        #Set_end_time()
    print("Ending second for plot:", End_value)
																							
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
window.columnconfigure(3, weight=col_weight)
window.columnconfigure(4, weight=col_weight)
#window.columnconfigure(5, weight=col_weight)

# Create a File Explorer label
label_file_explorer = Label(window,text = "Load and Plot h5 Files", height = 4, fg = "blue")#, width = 100)
button_explore = Button(window, text = "Browse Files",command = browseFiles) 
button_plotter = Button(window, text="Plot Data", command=plotting_script)

label_channel = Label(window, text="Select data channel")
channeled = ttk.Combobox(window)
channeled.bind("<<ComboboxSelected>>", pick_channel)
label_slice = Label(window, text="Select data slice")
sliced = ttk.Combobox(window)
sliced.bind("<<ComboboxSelected>>", pick_slice)

fft_var = BooleanVar()
fit_var = BooleanVar()
check_fft = ttk.Checkbutton(window, text='Plot FFT?', command=check_fft, variable=fft_var)
check_fit = ttk.Checkbutton(window, text='Fit FFT?', command=check_fit, variable=fit_var)

Start_var = StringVar(window)
Start_var.set("0")
Start_spinbox = ttk.Spinbox(window, from_=0, to=100, width=10, font=("Arial", 12), textvariable=Start_var, command=Set_start_time)
Start_spinbox.config(state="normal", cursor="hand2", justify="center", wrap=False)

End_var = StringVar(window)
End_var.set("1")
End_spinbox = ttk.Spinbox(window, from_=0, to=100, width=10, font=("Arial", 12), command=Set_end_time)
End_spinbox.config(state="normal", cursor="hand2", justify="center", wrap=False, textvariable=End_var)

Set_start_time()
Set_end_time()

label_file_explorer.grid(column = 0, row = 0, columnspan=5, sticky=EW)
middle_col = 2
button_explore.grid(column = middle_col, row = 1)
#button_loader.grid(column = 1,row = 2)
label_channel.grid(column = middle_col, row = 2)
channeled.grid(column = middle_col,row = 3)
label_slice.grid(column = middle_col, row = 4)
sliced.grid(column = middle_col,row = 5)
button_plotter.grid(column = middle_col,row = 6)
check_fft.grid(column = middle_col+1,row = 5)
check_fit.grid(column = middle_col+1,row = 6)
Start_spinbox.grid(column = middle_col-1,row = 5)
End_spinbox.grid(column = middle_col-1,row = 6)

# Let the window wait for any events
window.mainloop()