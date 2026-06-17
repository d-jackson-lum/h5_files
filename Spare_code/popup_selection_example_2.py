# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 14:10:10 2025

@author: DanielJackson
"""

"""
Source: https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
"""


# Python program to create 
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *
from tkinter import messagebox, simpledialog, ttk, filedialog


# import filedialog module
#from tkinter import filedialog

# Function for opening the 
# file explorer window
def browseFiles():
	filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("Text files",
														"*.txt*"),
													("all files",
														"*.*")))
	# Change label contents
	label_file_explorer.configure(text="File Opened: "+filename)
	
	
def browse_folder():
    folder_path = filedialog.askdirectory()
    print(f"Selected Folder: {folder_path}")
    return folder_path

																								
# Create the root window
window = Tk()

# Set window title
window.title('File Explorer')

# Set window size
window.geometry("500x500")

#Set window background color
window.config(background = "white")

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.columnconfigure(0, weight=2)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=2)

# Create a File Explorer label
label_file_explorer = Label(window, 
							text = "File Explorer using Tkinter",
							width = 100, height = 4, 
							fg = "blue")

	
button_explore = Button(window, 
						text = "Browse Files",
						command = browseFiles)  

button_exit = Button(window, text = "Exit")#, command = exit) 

# Grid method is chosen for placing
# the widgets at respective positions 
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 0)

button_explore.grid(column = 1, row = 1)

button_exit.grid(column = 1,row = 2)

# Let the window wait for any events
window.mainloop()
