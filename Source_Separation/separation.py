# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 23:58:24 2023

@author: Bill
"""

from demucs.Source_Separation import Source_Separation
import soundfile as sf

file = '.mp3'
vocal, no_vocal = Source_Separation(file)

sr = 44100 

sf.write('no_vocal.wav', no_vocal, sr)

sf.write('vocals.wav', vocal, sr)