# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 10:12:52 2025

@author: DanielJackson
"""

import numpy as np
from scipy.fft import rfft, rfftfreq # fft, fftfreq ## fft and rfft do the same thing, but rfft eliminates symmettry around 0
from collections import namedtuple
import math
from itertools import product
import pandas as pd
#from lumicks.pylake.force_calibration.detail.power_models import (
#    ScaledModel, fit_analytical_lorentzian,)
#import lumicks.pylake as lk


def Get_Slices(file, Data_Channel):
    Channels = sorted(file.h5.items())
    #N_channels = len(Channels)
    channel = ''
    #channels = ''
    ind = 0
    #channels = ar.array(["String used to record channel names","String used to record channel names"])
    #channels = np.resize(channels, N_channels)
    channels = []
    for channel, slices in Channels:
        #channels += channel + ', '
        #channels[ind] = channel
        channels.append(channel)
        data_slices = []
        if Data_Channel == channel:
            for sli in slices:
                data_slices.append(sli)
                checker = 1
            break
        else:
            checker = 0
        ind += 1
    return data_slices, channels, checker

def Get_All_Slices(file):
    Channels = sorted(file.h5.items())
    channel = ''
    ind = int(0)
    Data_options = [[],[]]
    N_channels = len(Channels)
    Data_options_big = Data_options + [[]]*int(N_channels - 1)
    for channel, slices in Channels:
        data_slices = [channel]
        for sli in slices:
            data_slices.append(sli)
        Data_options_big[ind]=data_slices
        ind +=int(1)
    return Data_options_big

def Get_FFT(data, time_0, time_1):
    
    Nd = len(data)
    Sample_rate = 1/(time_1 - time_0) #Hz
    FFT_of_data = rfft(data)
    absolute_value_FFT = np.abs(FFT_of_data)
    Frequencies_of_FFT = rfftfreq(Nd, 1/Sample_rate) #(Number of points, sample rate)
    
    return absolute_value_FFT, Frequencies_of_FFT, Sample_rate


def Basic_Lorentzian(D, f_c, f):
    return (D/(2*(np.pi**2)))/(f_c**2 + f**2)


def fit_analytical_lorentzian(ps):
    """Performs an analytical least-squares fit of a Lorentzian Power Spectrum.

    Based on Section IV from ref. 1. Note that the equations for the statistics Spq are divided
    by a factor of two since we defined the power spectrum in V^2/Hz instead of 0.5 V^2/Hz.

    Parameters
    ----------
    ps : PowerSpectrum
        Power spectrum data. Should generally be block-averaged, before passing
        into this function.

    Returns
    -------
    namedtuple (fc, D, sigma_fc, sigma_D, ps_fit)
        Attributes:
        - `fc` : corner frequency [Hz]
        - `D`: diffusion constant [V^2/s]
        - `sigma_fc`, `sigma_D`: 1-sigma confidence intervals for `fc` and `D`
        - `ps_fit`: :class:`~lumicks.pylake.force_calibration.power_spectrum.PowerSpectrum` object with model fit

    """
    FitResults = namedtuple(
        "AnalyticalLorentzianFitResults", ["fc", "D", "sigma_fc", "sigma_D", "ps_fit"]
    )

    # Calculate S[p,q] elements (Ref. 1, Eq. 13-14).
    Spq = np.zeros((3, 3))
    for p, q in product(range(3), range(3)):
        Spq[p, q] = np.sum(np.power(ps.frequency, 2 * p) * np.power(ps.power, q))

    # Calculate a and b parameters (Ref. 1, Eq. 13-14).
    a = (Spq[0, 1] * Spq[2, 2] - Spq[1, 1] * Spq[1, 2]) / (
        Spq[0, 2] * Spq[2, 2] - Spq[1, 2] * Spq[1, 2]
    )
    b = (Spq[1, 1] * Spq[0, 2] - Spq[0, 1] * Spq[1, 2]) / (
        Spq[0, 2] * Spq[2, 2] - Spq[1, 2] * Spq[1, 2]
    )

    # Having a and b, calculating fc and D is trivial.
    a_div_b = a / b
    if a_div_b > 0:
        fc = math.sqrt(a_div_b)  # corner frequency [Hz]
    else:
        # When the corner frequency is very low and the power spectrum doesn't reach all the way,
        # this can fail. As initial guess we then use the half the lowest nonzero frequency observed
        # in the power spectrum (optimal when assuming uniform prior for our guess). Note that zero
        # isn't a valid choice, since this leads to nan's and infinities down the road.
        fc = 0.5 * (ps.frequency[0] if ps.frequency[0] > 0 else ps.frequency[1])

    if b > 0:
        D = (1 / b) * (math.pi**2)  # diffusion constant [V^2/s]
    else:
        # If b <= 0, the analytic estimation procedure failed. Using a negative value for the
        # diffusion would place the initial guess outside the feasible physical parameter range.
        # This would result in a failing non-linear fit. In this case, we need a different way of
        # estimating this quantity. The power spectral density at frequency zero is given by:
        #
        #   P0 = D / (pi**2 * fc**2)
        #
        # Therefore, an alternative method to get a rough estimate for this quantity would be:
        #
        #   D_guess = pi**2 * fc**2 * power[0]
        #
        # Where power[0] is the lowest frequency in the spectrum.
        D = math.pi**2 * fc**2 * ps.power[0]

    # Fitted power spectrum values.
    ps_fit = ps.with_spectrum(1 / (a + b * np.power(ps.frequency, 2)))

    # Error propagation (Ref. 1, Eq. 25-28).
    x_min = ps.frequency.min() / fc
    x_max = ps.frequency.max() / fc

    u = (
        (2 * x_max) / (1 + x_max**2)
        - (2 * x_min) / (1 + x_min**2)
        + 2 * math.atan((x_max - x_min) / (1 + x_min * x_max))
    )
    v = (4 / (x_max - x_min)) * (math.atan((x_max - x_min) / (1 + x_min * x_max))) ** 2
    s_fc = math.sqrt(math.pi / (u - v))
    sigma_fc = fc * s_fc / math.sqrt(math.pi * fc * ps.total_duration)

    s_D = math.sqrt(u / ((1 + math.pi / 2) * (x_max - x_min))) * s_fc
    sigma_D = D * math.sqrt((1 + math.pi / 2) / (math.pi * fc * ps.total_duration)) * s_D

    return FitResults(fc, D, sigma_fc, sigma_D, ps_fit)


def Prepare_export(Xdata,Ydata,Xaxis_label,Yaxis_label):
    raw_data = np.array([Xdata,Ydata])
    atad_war = np.transpose(raw_data)
    framed_data = pd.DataFrame(atad_war, columns=[Xaxis_label, Yaxis_label])
    framed_data = framed_data.drop(framed_data.index[0])
    return framed_data
    




