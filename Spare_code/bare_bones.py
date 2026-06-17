# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 13:23:28 2026

@author: DanielJackson
"""

import lumicks.pylake as lk
import matplotlib.pyplot as plt

file = lk.File("b27.h5")
exp_slice = slice('0s', '0.005s')
trap_data = file['Trap position']['1X'][exp_slice].data
#raw_f1x = -file['Force HF']['Force 1x'][exp_slice].data
#raw_f2x = file['Force HF']['Force 2x'][exp_slice].data
plt.figure(figsize=(10, 4))
plt.plot(trap_data, 'grey',label='trap 1 position')
plt.plot(raw_f2x,'green',  label= 'force 2x')
plt.xlabel("Time")
plt.ylabel("Trap 1 position & Force 2HF")
plt.legend()
plt.tight_layout()
plt.show()