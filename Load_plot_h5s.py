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
#Data_Channel = 'Force HF' #Will proccess all data associated with this channel #e.g. Force 1x, Force 2x, etc.
global Start_value
global End_value
start_time = int(Start_value)
end_time = int(End_value)

#Choose whether to calculate and plot the FFT
Do_FFT = 1 # "1" to calculate the FFT. "0" does not calculate it.
#If Do_FFT is "0" then plotting and fitting will not happen
global check_fft_val
global check_fit_val
Plot_FFT = check_fft_val # "1" to also plot the FFT of the data. "0" to only plot data
Fit_FFT = check_fit_val # "1" to include a fit to the FFT. "0" to not include 
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
import scipy as sp
import lumicks.pylake as lk
from h5_functions import Get_Slices, Get_FFT, fit_analytical_lorentzian, Prepare_export#, lorentzian
from lumicks.pylake.force_calibration.power_spectrum import PowerSpectrum
import pandas as pd
import sys
from scipy.optimize import curve_fit
import numpy as np
import math
#matplotlib inline
width = 8
height = 4.5
resolution_dpi = 200
plt.rcParams['figure.figsize'] = [width, height]
plt.rcParams['figure.dpi'] = resolution_dpi
#from scipy.fft import rfft, rfftfreq # fft, fftfreq ## fft and rfft do the same thing, but rfft eliminates symmettry around 0
#import sys
#from h5_options import Data_Slice
#import h5py

#global global_test
#print(global_test)



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

print(' ')
print('------------------------')
print(' ')

global Data_Channel
Slices, Channels, checker = Get_Slices(file, Data_Channel)
#print(Slices)
#if checker == 0:
#    sys.exit('No matching channels in this file. Try again using the following data channel options: ' )#+ channels)

global Slice
if Slice == 'All Slices':
    print('Will analyze...')
    print(Slices)
else:
    Slices = [Slice]
    print('Will analyze ' + Slice)

for s in Slices:
    
    Data_slice = s
    #print(file)
    
    data = file[Data_Channel][Data_slice].data
    timestamp = file[Data_Channel][Data_slice].timestamps
    time_ns = (timestamp - timestamp[0])
    time_s = time_ns*1e-9
    Nd = len(data)
    #print(Nd)
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
    #Settings used for plotting (applies only to raw data output, not FFT)
    Xaxis = 'Time (s)' 
    Yaxis = ''
    if(Data_Channel=='Force LF' or Data_Channel=='Force HF'):
        Yaxis = 'Force (pN)'
    elif(Data_Channel=='Bead position' or Data_Channel=='Nanostage position'):
        Yaxis = 'Position (um)'
    elif(Data_Channel=='Trap position' or Data_Channel=='1+2 position'):
        Yaxis = 'Position (um)'
    else:
        Yaxis = 'Units'
    
    X_scale = 'linear' 
    Y_scale = 'linear'
    
    plot_title = Data_Channel + ' ' + s
    
    X_plt = time_plt
    Y_plt = data_plt

    IQR = sp.stats.iqr(Y_plt)
    bin_width = 2 * IQR / (Nd**(1/3)) ##based on Freedman-Diaconis rule for data spread
    start_bin = min(Y_plt)
    end_bin = max(Y_plt)
    histing_offset_percent = 0.3
    histing_bins = int(abs(((end_bin - start_bin)/bin_width)) * histing_offset_percent)
    print(histing_bins)
    
    if histing_bins > 100:
        histing_bins = int(histing_bins/2)

    fig = plt.figure(num=0)
    gs = fig.add_gridspec(1, 2, hspace=0, wspace=0.005, width_ratios=[2,1])
    (raw, histo) = gs.subplots(sharey=True)
    fig.suptitle(plot_title)#('Raw data with histogram')
    raw.plot(X_plt, Y_plt, label='Data')
    raw.set(xlabel=Xaxis, ylabel=Yaxis)
    #histed, binned = np.histogram(Y_plt, bins = histing_bins)
    
    histed, binned, _ = histo.hist(Y_plt, orientation='horizontal', bins = histing_bins, label='Histogram', color='C7')
    histo.set(xlabel='Amplitude')
    histo.axes.get_xaxis().set_visible(False)
    histo.axes.get_yaxis().set_visible(False)
    histo.axis('off')
    #Fit the Histrogram
    def gauss(x, H, A, x0, sigma):
        import numpy as np
        return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))
    
    bin_centers=[]
    i=0
    for histt in histed:
        bin1 = binned[i]
        bin2 = binned[i+1]
        bin_center = (bin1 + bin2)/2
        bin_centers.append(bin_center)
        i += 1
    guess_H = 0
    guess_A = max(histed)
    Guess_x0 = bin_centers[int(len(bin_centers)/2)]
    Guess_sigma = bin_centers[int(len(bin_centers)/1.5)] - bin_centers[int(len(bin_centers)/2)]
    #print(guess_H, guess_A, Guess_x0, Guess_sigma)
    guess = [guess_H, guess_A, Guess_x0, Guess_sigma]
    params, something = curve_fit(gauss, bin_centers, histed, guess)
    fit_H = params[0]
    fit_A = params[1]
    fit_x0 = params[2]
    fit_sigma = params[3]
    FWHM = 2.35*fit_sigma
    fit_histed = gauss(bin_centers, fit_H, fit_A, fit_x0, fit_sigma)
    #plt.figure(num=1)
    #plt.plot(bin_centers, histed, 'o', label='data')#, orientation='horizontal', label='Histogram', color='C7')
    #plt.plot(bin_centers, fit_histed, '-', label='fit')
    #plt.show()
    histo.plot(fit_histed, bin_centers)#, color='r')
    peak = 'Peak: ' + str('%s' % float('%.3g' % fit_x0))
    FWHM_ = 'FWHM: ' + str('%s' % float('%.3g' % FWHM))
    width_pixels = width * resolution_dpi
    height_pixels = height * resolution_dpi
    w_frac_1 = 0.67
    w_frac_2 = 0.67
    h_frac_1 = 0.12
    h_frac_2 = 0.075
    histo.annotate(peak, xy=(width_pixels*w_frac_1, height_pixels*h_frac_1), xycoords='figure pixels')
    histo.annotate(FWHM_, xy=(width_pixels*w_frac_2, height_pixels*h_frac_2), xycoords='figure pixels')
    histo.axes.set_xbound(lower = 0)
    #histo.annotate(peak,
    #        xy=(.95, .12), xycoords='figure fraction', fontsize=10,
    #        horizontalalignment='right')
    #histo.annotate(FWHM_,
    #        xy=(.95, .075), xycoords='figure fraction', fontsize=10,
    #        horizontalalignment='right')
    fig.show()
    
    #print(histed)
    #print(binned)
    #print('Peak position: ' + str(fit_x0))
    #print(Guess_sigma)
    #print(fit_sigma)
    plt.show()
    
    
    
    if do_export:
        plt.savefig(Save_as + ' plot.png')

    
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
            plt.figure(num=2)#(figsize=(8, 6))
            #Ignore very first data point in plotting FFT. Keeps giving  a miniscule value (e.g. 1e-41)
            plt.plot(data_freq[1:], data_amplitude[1:], label='Data', color='C7') #C7 is a gray color
            if Fit_FFT: plt.plot(fit_freq[1:], fit_amplitude[1:], label='Lorentzian Fit', color='C3') #C3 is a red color
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

print('Analysis completed')
#sys.exit('Analysis completed')






