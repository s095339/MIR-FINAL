# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 23:58:24 2023

@author: Bill
"""

from .demucs.Source_Separation import Source_Separation
import soundfile as sf



def getSeparation(file):
    sr = 44100
    vocal, no_vocal= Source_Separation(file)
    return vocal, no_vocal, sr
