#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:48:50 2018

@author: php17cs
"""

import numpy as np
from function_file import read_in_any_datafiles, velocity_elements, plots_legend

#reads in the .dat files from an inputfile list
dflist, dname, nlines = read_in_any_datafiles('file.txt')

#calculates the velocity (distance travelled/snapshot length
dflist = velocity_elements(dflist, dname, nlines)

#creates the legend for for plots of single simulations
legend = plots_legend(dname)

j = 50
velocity = 'PM-velxy'

dflist_mean = np.empty(1000) 

for line in range(1000):
    dflist_sumlist = []
    for n in range(nlines):
        dflist_sumlist.append((dflist[n].loc[j].sort_values(velocity)[velocity]).iloc[line])
    dflist_mean[line] = (np.mean(dflist_sumlist))      

np.savetxt('PM_sorted_mean_%s_%s_%sMyr.csv'%(legend[0][2:5], legend[0][22:25], j/10), (dflist_mean), delimiter="\t")