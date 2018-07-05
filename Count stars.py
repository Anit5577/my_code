#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:57:52 2018

@author: php17cs
"""

import numpy as np
import F_Transverse_Velocity_final as TV
from function_file import read_in_any_datafiles

#reads in the .dat files from an inputfile list
dflist, dname, nlines = read_in_any_datafiles('file_nstars.txt')

#%%

pc = 3.08567758*10**13   #in km
  # takes the snapshotlength from the time of the first snapshot after initial conditions
 # takes the snapshotlength from the time of the first snapshot after initial conditions
timestep_in_seconds = (3.1556926*10**13)*(np.round(dflist[0].loc[1].iloc[1]\
                          ['time'],decimals=4))
distance_to_velocity = pc/timestep_in_seconds

nsnaps=101
numb_stars = np.zeros((nlines,nsnaps))

for n in range(nlines):
    for j in range(nsnaps):
        numb_stars[n,j] = dflist[n].loc[j].index.size      
        
    transvellist = TV.transverse_velocity(dname[n],nsnaps,numb_stars[n,j]) # need to make my stars allocatable variable
    for ssnap in range(0,nsnaps):
        dflist[n].loc[0, 'xdist'] = 0
        dflist[n].loc[0, 'ydist'] = 0
        dflist[n].loc[0, 'zdist'] = 0
        dflist[n].loc[ssnap, 'xdist'] = transvellist[ssnap,0]
        dflist[n].loc[ssnap, 'ydist'] = transvellist[ssnap,1]
        dflist[n].loc[ssnap, 'zdist'] = transvellist[ssnap,2]

    dflist[n]['xvel'] = dflist[n]['xdist'].multiply(distance_to_velocity)
    dflist[n]['yvel'] = dflist[n]['ydist'].multiply(distance_to_velocity)
    dflist[n]['zvel'] = dflist[n]['zdist'].multiply(distance_to_velocity)
    dflist[n]['3D-veldist'] = (np.sqrt(dflist[n]['xvel']**2.+dflist[n]['yvel']**2.\
    +dflist[n]['zvel']**2.)) #3D-velocity from distance/snapshot length
    dflist[n]['PM-veldist'] = (np.sqrt(dflist[n]['xvel']**2.+dflist[n]['yvel']**2.))
    dflist[n]['3D-velxyz'] = (np.sqrt(dflist[n]['velx']**2.+dflist[n]['vely']**2.+\
          dflist[n]['velz']**2.)) #3D-velocity from distance/snapshot length
    dflist[n]['PM-velxy'] = (np.sqrt(dflist[n]['velx']**2.+dflist[n]['vely']**2.))

