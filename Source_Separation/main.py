# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 23:58:24 2023

@author: Bill
"""

from demucs.Source_Separation import Source_Separation
import soundfile as sf

path1 = 'D:\\LAB\\碩一下\\音樂資訊檢索\\final\\MIR-FINAL\\Source_Separation\\separated\\mdx_extra\\idol (mp3cut.net)\\no_vocals.mp3'
path2 = 'D:\\LAB\\碩一下\\音樂資訊檢索\\final\\MIR-FINAL\\Source_Separation\\separated\\mdx_extra\\idol (mp3cut.net)\\vocals.mp3'

file = 'idol (mp3cut.net).mp3'
vocal, no_vocal = Source_Separation(file)

sr = 44100 

#sf.write('no_vocal.wav', no_vocal, sr)

#sf.write('vocals.wav', vocal, sr)