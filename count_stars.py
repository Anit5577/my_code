#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 12:01:22 2017

@author: php17cs
"""

import pandas as pd
import numpy as np


fname = input('Choose data file to be read into array: ')
nsnaps = 101
#nstars= input('How many stars in snapshot? ')


df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velz':np.float64})

#The following bit passes the filename and the number of snaps and stars to the Fortran subroutine that calculates the COD and adjusts the radii by that COD.

nstars = int((df1.index.size)/nsnaps)


print (nstars, nsnaps )
