#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 15:49:48 2018

@author: php17cs
"""

import numpy as np
import os

from function_file import read_in_any_datafiles

#reads in the .dat files from an inputfile list
dflist, dname, nlines = read_in_any_datafiles('file.txt')

#%%

nsnaps = 101

for n in range(nlines):    
    path = '/home/php17cs/local/backed_up_on_astro3/analysis/snapshots/%s' %dname[n]    
    os.mkdir(path)
    os.chdir(path)
    
    
    for i in range(1, nsnaps+1):
        ifname ='snap'
        if i < 10:
            ifname += '000' + str(i)
        elif i < 100:
            ifname += '00' + str(i)
        elif i < 1000:
            ifname += '0' + str(i)
        elif i < 10000:
            ifname += '' + str(i)
        else:
            ifname += str(i)
        dflist[n].loc[i-1].to_csv('%s'%(ifname), sep=' ' ,columns=['time', \
           'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz'], header=False)

    