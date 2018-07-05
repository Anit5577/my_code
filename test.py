#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:46:27 2017

@author: php17cs
"""
import pandas as pd
import numpy as np
import astropy.units as u
from astropy import constants as const
import statistics
import matplotlib.pyplot as plt


fname = input('Choose data file to be read into array: ')

if fname[17] == 'X':
    legendtitle = (r'N=1000 stars, D=%s.%s, $\alpha_{vir}$=%s.%s, initial radius=%s pc$' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
elif fname[17] == '5':
    legendtitle = (r'N=500 stars, D=%s.%s, $\alpha_{vir}$=%s.%s, initial radius=%s pc' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
elif fname[17] == '2':    
    legendtitle = (r'N=2000 stars, D=%s.%s, $\alpha_{vir}$=%s.%s, initial radius=%s pc' %(fname[7],fname[8],fname[22],fname[23],fname[12]))

#%%
    
    