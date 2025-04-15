# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 17:03:03 2025

@author: DanielJackson
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq # fft, fftfreq ## fft and rfft do the same thing, but rfft eliminates symmettry around 0
import lumicks.pylake as lk
#import pandas as pd

"""
Load the file
"""
folder_path = 'C:/Users/DanielJackson/Downloads/' #'Documents/Service/BA003_HQ/25.02.19_PI_Nanostage_Tests/Waveform/'
file_name = 'Marker_during_phone_recording.h5'
file_ID = file_name.split('.')[0]

file = lk.File(folder_path + file_name)

print(file)

"""
Choose the data column to load
"""

Data_type = 'Trap position'
Data_choice = '1Y'

data = file[Data_type][Data_choice].data
points = file[Data_type][Data_choice].timestamps

time_ns = (points-points[0])
time_s = time_ns*1e-9
Nd = len(data)

"""
Perform transform on the data
"""

Sample_rate = 1#/(time_s[1] - time_s[0]) #Hz
datafft = rfft(data)
abs_datafft = np.abs(datafft)
freq = rfftfreq(Nd, 1/Sample_rate) #(Number of points, sample rate)

"""
Plot the data
"""

start_plt = int(Nd*(2.04/15))
end_plt = int(Nd*(2.2/15))
data_plt = data[start_plt:end_plt]
time_plt = time_s[start_plt:end_plt]

plt.figure()
plt.plot(time_plt, data_plt)
plt.xlabel('Time (s)')
plt.ylabel('Position (um)')
plt.title('Trap 1Y Position')
plt.show()

#plt.figure()
#plt.plot(freq, abs_datafft)
#plt.xscale('log')
#plt.yscale('log')
#plt.xlabel('Time (s)')
#plt.ylabel('Position (um)')
#plt.title('Transform of Trap 2 position')
#plt.show()

