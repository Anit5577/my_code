#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:05:42 2017

@author: php17cs
"""

#import numpy as np

#F_COD_Radius! corrects the radius of each star by the respective COD and returns the COD-corrected positions of all stars.
# results in an array nrad(i,1:3) with i representing the snapshot and the 1:3 the three vector components -> to call the values for each dimension:
# x: nrad[i,0], y: nrad[i,1] and z: nrad[i,2]


import F_COD_Radius_Nstars as CODRN

fname = input('Choose data file to be read into array: ')
nsnaps = 101
nstars = 1000 # define nstars depending on initial conditions

nrad = CODRN.cod_radius(fname,nsnaps,nstars)

print(nrad[0])



#%% Centre of Mass code to practise (not used in COD calculation)
#
#com = []
#for ssnap in range(0, nsnaps):
#    summass=0
#    mradx=0
#    mrady=0
#    mradz=0 
#    summass = df1.loc[ssnap,'mass'].sum()
#    mradx = np.sum(df1.loc[ssnap,'radx']*df1.loc[ssnap,'mass'])/summass
#    mrady = np.sum(df1.loc[ssnap,'rady']*df1.loc[ssnap,'mass'])/summass
#    mradz = np.sum(df1.loc[ssnap,'radz']*df1.loc[ssnap,'mass'])/summass
#    com.append([mradx,mrady,mradz])

  

            



