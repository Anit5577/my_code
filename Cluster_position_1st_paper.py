#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 09:58:36 2018

@author: php17cs
"""

# Code to plot x-y plane for 20 simulations to investigate unbound behaviour

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import PercentFormatter
import seaborn as sns

#%%

from function_file import read_in_any_datafiles, energy_stars, plots_legend, velocity_element
#reads in the .dat files from an inputfile list
dflist, dname, nlines = read_in_any_datafiles('file.txt')

#%%

#calculates energy of each star in each snapshot and adds this in a column
dflist = energy_stars(dflist, dname, nlines)

#calculates the radius/position of each star after COD-correction
#dflist = COD_corrected_location(dflist,dname,nlines)

#calculates the velocity (distance travelled/snapshot length
dflist = velocity_elements(dflist, dname, nlines)

#adds column identifying stars outside 2 half-mass radius
#dflist = stars_in_outside_2HMR(dflist, dname, nlines)

#creates the legend for for plots of single simulations
legend = plots_legend(dname)

#%%

