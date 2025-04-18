# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 17:03:03 2025

@author: DanielJackson
"""


"""
User Inputs
"""
#Choosing the desired file
folder_path = 'C:/Users/DanielJackson/Documents/Service/BA003_HQ/25.02.19_PI_Nanostage_Tests/Stuck_bead/'
#'C:/Users/DanielJackson/Downloads/'
file_name = 'Stuck_bead_2nd_min_378fps.h5'
#'Marker_during_phone_recording.h5'

#Choosing the desired channel and setting the time range to be plotted
Data_Channel = 'Force HF' #Will proccess all data associated with this channel #e.g. Force 1x, Force 2x, etc.
start_time = 2
end_time = 3

#Settings used for plotting (applies only to raw data output, not FFT)
Xaxis = 'Time (s)' 
Yaxis = 'Force (pN)' 
X_scale = 'linear' 
Y_scale = 'linear' 

#Choose whether to calculate and plot the FFT
Do_FFT = 1 # "1" to calculate the FFT. "0" does not calculate it.
#If Do_FFT is "0" then plotting and fitting will not happen
Plot_FFT = 1 # "1" to also plot the FFT of the data. "0" to only plot data
Fit_FFT = 1 # "1" to include a fit to the FFT. "0" to not include 
downsampling_number = 1

#Choose to export data. Raw data as csv or txt file, and the png of plot
export = 'no' #options are 'yes' or 'no'
export_type = 'txt'  #Options are 'txt' or 'csv' #Defualts to 'txt' for incorrect values
Destination_folder = 'C:/Users/DanielJackson/Documents/h5_saving/'

"""
End of User Inputs
"""


"""
Import Modules
"""
import matplotlib.pyplot as plt
import lumicks.pylake as lk
from h5_functions import Get_Slices, Get_FFT, fit_analytical_lorentzian, Prepare_export#, lorentzian
from lumicks.pylake.force_calibration.power_spectrum import PowerSpectrum
import pandas as pd
#import numpy as np
#from scipy.fft import rfft, rfftfreq # fft, fftfreq ## fft and rfft do the same thing, but rfft eliminates symmettry around 0
#import sys
#from h5_options import Data_Slice
#import h5py

"""
Load the file
"""

file_ID = file_name.split('.')[0]
file = lk.File(folder_path + file_name)
#print(file)

"""
Choose the data column to load
Finds all slices present for the chosen data channel
Will proccess all data associated with this channel #e.g. Force HF: Force 1x, Force 2x, etc.
"""

Slices = Get_Slices(file, Data_Channel)

for s in Slices:
    
    Data_slice = s
    
    data = file[Data_Channel][Data_slice].data
    timestamp = file[Data_Channel][Data_slice].timestamps
    time_ns = (timestamp - timestamp[0])
    time_s = time_ns*1e-9
    Nd = len(data)
    
    """
    Check for empty slice -> skip if empty
    """
    if Nd < 2:
        continue
    
    """
    Perform fourier transform on the data
    """
    
    data_fft, freq_fft, Sample_rate = Get_FFT(data, time_s[0], time_s[1]) #outputs (FFT_of_data, Frequencies_of_data, Sample_rate)
    
    """
    Plotting region
    """
    #start and end points of the data being analyzed
    start_pnt = start_time * Sample_rate
    end_pnt = end_time * Sample_rate
    
    #some fail safes to prevent errors
    if start_pnt < 0:
        start_pnt = 0
    if end_pnt > (Nd - 1):
        end_pnt = Nd - 1
    if start_pnt >= end_pnt:
        start_pnt = end_pnt - 1
        
    #Creat array of the desired time window    
    start_plt = int(start_pnt)
    end_plt = int(end_pnt)
    data_plt = data[start_plt:end_plt]
    time_plt = time_s[start_plt:end_plt]
    
    ps_data = PowerSpectrum(data_plt, Sample_rate)
    ps_data = ps_data.downsampled_by(downsampling_number)

    """
    Exporting parameters
    """
    #Set folder -> control at the top of page
    Save_as = Destination_folder + Data_Channel + ' ' + s
    #Convert yes/no to binary control for exporting
    if export == 'yes':
        do_export = 1
    else:
        do_export = 0
    
    #Set type to txt or csv  
    if export_type != 'txt' and export_type != 'csv':
        print('Improper export type set. Defaulting to .txt file type.')
        export_type = 'txt'

    """
    Plot the data
    """
    plot_title = Data_Channel + ' ' + s
    
    X_plt = time_plt
    Y_plt = data_plt
    
    plt.figure()
    plt.plot(X_plt, Y_plt) #, label='Data', color='blue')
    plt.xlabel(Xaxis)
    plt.ylabel(Yaxis)
    plt.xscale(X_scale)
    plt.yscale(Y_scale)
    plt.title(plot_title)
    if do_export: plt.savefig(Save_as + ' plot.png')
    plt.show()
    
    if do_export:
        framed_data = Prepare_export(X_plt,Y_plt,Xaxis,Yaxis)
        framed_data.to_csv(Save_as + '.' + export_type)
    
    """
    Calculating the FFT and fit
    """
    #These are pylake functions. makes data into a power spectrum object that
    #gets passed through the pylake package
    if Do_FFT:
        
        data_freq = ps_data.frequency
        data_amplitude = ps_data.power
        if Fit_FFT:    
            Fit_Results = fit_analytical_lorentzian(ps_data)
        
            fc = Fit_Results[0]
            D = Fit_Results[1]
            sigma_fc = Fit_Results[2]
            sigma_D = Fit_Results[3]
            ps_fit = Fit_Results[4]

            fit_freq = ps_fit.frequency
            fit_amplitude = ps_fit.power
    
        if Plot_FFT:
            plt.figure#(figsize=(8, 6))
            #Ignore very first data point in plotting FFT. Keeps giving  a miniscule value (e.g. 1e-41)
            plt.plot(data_freq[1:], data_amplitude[1:], label='Data', color='blue')
            if Fit_FFT: plt.plot(fit_freq[1:], fit_amplitude[1:], label='Lorentzian Fit', color='red')
            plt.xlabel('Frequencies')
            plt.ylabel('Amplitudes (V**2/Hz)')
            plt.xscale('log')
            plt.yscale('log')
            plt.legend()
            if do_export: plt.savefig(Save_as + ' FFT plot.png')
            plt.title('Lorentzian Fit to ' + plot_title)
            plt.show()
            
            if do_export:
                data_freq = ps_data.frequency
                data_amplitude = ps_data.power
                fit_freq = ps_fit.frequency
                fit_amplitude = ps_fit.power
                framed_data = Prepare_export(data_freq,data_amplitude,'Frequencies','Amplitudes')
                if Fit_FFT:
                    framed_fit = Prepare_export(fit_freq,fit_amplitude,'Fit Frequencies','Fit Amplitudes')
                    FFT_with_fit = pd.concat([framed_data,framed_fit])
                    FFT_with_fit.to_csv(Save_as + ' FFT with fit.' + export_type)
                else:
                    framed_data.to_csv(Save_as + ' FFT.' + export_type)

print('Analysis completed.')







