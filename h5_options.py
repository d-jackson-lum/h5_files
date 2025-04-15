# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:38:53 2025

@author: DanielJackson
"""

"""
Plotting Options
"""

Channels = [
    ['1+2 position', ['X', 'Y', 'Z']],
    ['Bead diameter', ['Template 1', 'Template 2']],
    ['Bead position', ['Bead 1 X', 'Bead 1 Y', 'Bead 2 X', 'Bead 2 Y']],
    ['Diagnostics', ['Microstage position X', 'Microstage position Y']],
    ['Distance', ['Distance 1', 'Piezo Distance']],
    ['Force HF', ['Force 1x', 'Force 1y', 'Force 2x', 'Force 2y']],
    ['Force LF', ['Force 1x', 'Force 1y', 'Force 2x', 'Force 2y', 'Trap 1', 'Trap 2']],
    ['Trap position',['1X', '1Y', '2X', '2Y']],
    ['Tracking Matching Score', ['Bead 1', 'Bead 2']],
    ['Nanostage position',['X', 'X (analog)', 'Y', 'Y (analog)', 'Z', 'Z (analog)']]
    ]

#print(Options)


def Data_Slice(Choice):
    for choices in Channels:
        if choices[0]==Choice:
            return choices[1]