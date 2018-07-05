#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates the energy of each star after it calls the function to read in 20 simulation data.
# it contains the callable function unbound_stars, which uses the F2PY - routine BUS to calculate the energy in Fortran and then loads it as an additional column to each file in dflist.

import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from fractions import Fraction
from function_file import read_in_any_datafiles, energy_stars

#%%

dflist,dname,nlines  = read_in_any_datafiles('file.txt') #this reads in the .dat files from an inputfile list

dflist = energy_stars(dflist,dname,nlines) 

#%% this calculates the unbound-fraction for different mass regimes, it requires that simulations have been already read-in
 
snaps = [0, 10, 50, 100]

UB_fraction = np.zeros((nlines, len(snaps)))
HM_fraction = np.zeros((nlines, len(snaps)))
HMUB_AllHM_fraction = np.zeros((nlines, len(snaps)))
HMUB_AllUB_fraction = np.zeros((nlines, len(snaps)))
LMUB_AllLM_fraction = np.zeros((nlines, len(snaps)))

for i, n in product(range(nlines), range(len(snaps))): 
    
    UB_fraction[i,n] = Fraction(len(dflist[i].loc[snaps[n]][dflist[i].loc[snaps[n],'Unbound'] == True]), \
    len(dflist[i].loc[snaps[n]]))
    
    HM_fraction[i,n] = Fraction(len(dflist[i].loc[snaps[n]][dflist[i].loc[snaps[n],'mass'] >= 8.]), \
    len(dflist[i].loc[snaps[n]]))
    
    LMUB_AllLM_fraction[i,n] = Fraction(len(dflist[i].loc[snaps[n]][(dflist[i].loc[snaps[n],'mass']< 8.) \
                  & (dflist[i].loc[snaps[n],'Unbound']== True)]), \
                len(dflist[i].loc[snaps[n]][(dflist[i].loc[snaps[n],'mass'] < 8.)]))
    
    if len(dflist[i].loc[snaps[n]][(dflist[i].loc[snaps[n],'mass']>= 8.)]) != 0:
        HMUB_AllHM_fraction[i,n] = Fraction(len(dflist[i].loc[snaps[n]][(dflist[i].loc[snaps[n],'mass']>= 8.) \
                          & (dflist[i].loc[snaps[n],'Unbound']== True)]), \
                        len(dflist[i].loc[snaps[n]][(dflist[i].loc[snaps[n],'mass']>= 8.)]))
    else:
        continue
    
    if len(dflist[i].loc[snaps[n]][(dflist[i].loc[snaps[n],'Unbound']== True)]) != 0:   
        HMUB_AllUB_fraction[i,n] = Fraction(len(dflist[i].loc[snaps[n]][(dflist[i].loc[snaps[n],'mass']>= 8.) \
                                  & (dflist[i].loc[snaps[n],'Unbound']== True)]), \
                            len(dflist[i].loc[snaps[n]][(dflist[i].loc[snaps[n],'Unbound']== True)]))
    else:
        continue


#%%
 
snaps = 101    
    
UB_fraction = np.zeros((nlines, snaps))
HM_fraction = np.zeros((nlines, snaps))
HMUB_AllHM_fraction = np.zeros((nlines, snaps))
HMUB_AllUB_fraction = np.zeros((nlines, snaps))
LMUB_AllLM_fraction = np.zeros((nlines, snaps))

for i, n in product(range(nlines), range(snaps)): 
    
#    UB_fraction[i,n] = Fraction(len(dflist[i].loc[n][dflist[i].loc[n,'Unbound'] == True]), \
#    len(dflist[i].loc[n]))
#    
#    HM_fraction[i,n] = Fraction(len(dflist[i].loc[n][dflist[i].loc[n,'mass'] >= 8.]), \
#    len(dflist[i].loc[n]))
    
    LMUB_AllLM_fraction[i,n] = Fraction(len(dflist[i].loc[n][(dflist[i].loc[n,'mass']< 8.) \
                  & (dflist[i].loc[n,'Unbound']== True)]), \
                len(dflist[i].loc[n][(dflist[i].loc[n,'mass'] < 8.)]))
    
    if len(dflist[i].loc[n][(dflist[i].loc[n,'mass']>= 8.)]) != 0:
        HMUB_AllHM_fraction[i,n] = Fraction(len(dflist[i].loc[n][(dflist[i].loc[n,'mass']>= 8.) \
                          & (dflist[i].loc[n,'Unbound']== True)]), \
                        len(dflist[i].loc[n][(dflist[i].loc[n,'mass']>= 8.)]))
    else:
        continue
#    
#    if len(dflist[i].loc[n][(dflist[i].loc[n,'Unbound']== True)]) != 0:   
#        HMUB_AllUB_fraction[i,n] = Fraction(len(dflist[i].loc[n][(dflist[i].loc[n,'mass']>= 8.) \
#                                  & (dflist[i].loc[n,'Unbound']== True)]), \
#                            len(dflist[i].loc[n][(dflist[i].loc[n,'Unbound']== True)]))
#    else:
#        continue

#%%

x = np.arange(0.,snaps,1.)

for i in range(nlines):
    fig, ax = plt.subplots()
    ax.scatter(x, HMUB_AllHM_fraction[i], s=0.5, label ='HMUB of HMtotal fraction')    
    ax.scatter(x, LMUB_AllLM_fraction[i], s=0.5, label ='LMUB of LMtotal fraction') 

    ax.set_title(dname[i])
    ax.legend(loc='upper left')
plt.show()