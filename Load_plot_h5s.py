# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 17:03:03 2025

@author: DanielJackson
"""


""" User Inputs """

Data_Channel = 'Force HF'
start_time = 0
end_time = 10

"""
Import Modules
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq # fft, fftfreq ## fft and rfft do the same thing, but rfft eliminates symmettry around 0
import lumicks.pylake as lk
import sys
#from h5_options import Data_Slice
#import h5py
#import pandas as pd

"""
Load the file
"""
folder_path = 'C:/Users/DanielJackson/Downloads/'
file_name = 'Marker_during_phone_recording.h5'
file_ID = file_name.split('.')[0]

file = lk.File(folder_path + file_name)
#print(file)

"""
Choose the data column to load
-calls a list of all options in h5 files. Will plot all the choices for each data type
-saves time in plotting multiple axes at the same time
"""



Channels = sorted(file.h5.items())
channel = ''
channels = ''
for channel, slices in Channels:
    channels += channel + ', '
    data_slices = []
    if Data_Channel == channel:
        for sli in slices:
            data_slices.append(sli)
            checker = 1
        break
    else:
        checker = 0
        
if checker == 0:
    sys.exit('No matching channels in this file. Try again using the following options: ' + channels)

#Slices = Data_Slice(Data_Channel)
Slices = data_slices

for s in Slices:
    
    Data_slice = s
    
    data = file[Data_Channel][Data_slice].data
    points = file[Data_Channel][Data_slice].timestamps
    time_ns = (points-points[0])
    time_s = time_ns*1e-9
    Nd = len(data)
    
    """
    Perform transform on the data
    """
    
    Sample_rate = 1/(time_s[1] - time_s[0]) #Hz
    datafft = rfft(data)
    abs_datafft = np.abs(datafft)
    freq = rfftfreq(Nd, 1/Sample_rate) #(Number of points, sample rate)
    
    """
    Plotting region
    """

    start_pnt = start_time * Sample_rate
    end_pnt = end_time * Sample_rate
    
    if start_pnt < 0:
        start_pnt = 0
    if end_pnt > (Nd - 1):
        end_pnt = Nd - 1
    if start_pnt >= end_pnt:
        start_pnt = end_pnt - 1
        
    start_plt = int(start_pnt)
    end_plt = int(end_pnt)
    data_plt = data[start_plt:end_plt]
    time_plt = time_s[start_plt:end_plt]
    
    
    """
    Plot the data
    """
    
    plt.figure()
    plt.plot(time_plt, data_plt)
    plt.xlabel('Time (s)')
    plt.ylabel('y axis')
    plot_title = Data_Channel + ' ' + s
    plt.title(plot_title)
    plt.show()
    
    #plt.figure()
    #plt.plot(freq, abs_datafft)
    #plt.xscale('log')
    #plt.yscale('log')
    #plt.xlabel('Time (s)')
    #plt.ylabel('Position (um)')
    #plt.title('Transform of Trap 2 position')
    #plt.show()

