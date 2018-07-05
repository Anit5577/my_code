#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 09:58:36 2018

@author: php17cs
"""

# Code to plot x-y plane for 20 simulations to investigate unbound behaviour

import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from fractions import Fraction
import matplotlib.ticker as ticker

#%%

from function_file import read_in_any_datafiles, energy_stars, plots_legend, velocity_elements
#reads in the .dat files from an inputfile list
dflist, dname, nlines = read_in_any_datafiles('file.txt')

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

plt.style.use('seaborn-poster')

j = 100

for n in range(nlines):
    fig, ax = plt.subplots(figsize=(10., 10.))
#    ax.set(xlim=(-20., 20.), ylim=(-20., 20.))

    ax.set_xlabel('x (pc)')
    ax.set_ylabel('z (pc)')

    ax.scatter(dflist[n].loc[j,'radx'],dflist[n].loc[j,'radz'], s=5.0, c='grey')
#    ax.scatter(dflist[n].loc[j,'rady'][(dflist[n].loc[j,'Unbound']== True)],dflist[n].loc[j,'radz']\
#               [(dflist[n].loc[j,'Unbound']== True)], s=6.0, c='goldenrod', label='Ejected stars')
  

#    ax.scatter(dflist[n].loc[j,'radx'],dflist[n].loc[j,'rady'], s=10.0, label='Cluster stars')
#    ax.scatter(dflist[n].loc[j,'radx'][(dflist[n].loc[j,'Unbound']== True) & (dflist[n].loc[j,'PM-velxy'] > 2.5)],dflist[n].loc[j,'rady']\
#               [(dflist[n].loc[j,'Unbound']== True) & (dflist[n].loc[j,'PM-velxy'] > 2.5)], s=10.0, c='goldenrod', label='Ejected stars')
#
    ax.tick_params(which='both', direction='in', top=True, right=True)
    plt.show()

    ax.set_title('Cluster age %s Myr, %s' %(np.round(dflist[n].loc[j].iloc[0]['time'], decimals=1), dname[n]))

#    leg = ax.legend(loc='upper right', frameon=False)
#
#    for text in leg.get_texts():
#        text.set_color('#002342')
    plt.savefig('Cluster_check_xz_%s.png' %dname[n])
#plt.show()

#%%

import mpl_toolkits.mplot3d.axes3d as p3

for n in range(nlines):
    fig, ax = plt.subplots(figsize=(10., 10.))
    ax = p3.Axes3D(fig)
    
    ax.set_xlabel('x [pc]')
    ax.set_ylabel('y [pc]')
    ax.set_zlabel('z [pc]')
    
    ax.scatter(dflist[n].loc[j, 'radx'],  dflist[n].loc[j, 'rady'], dflist[n].loc[j, 'radz'] , s=5.0, c='grey')
    ax.scatter(dflist[n].loc[j,'radx'][(dflist[n].loc[j,'Unbound']== True)],dflist[n].loc[j,'rady']\
           [(dflist[n].loc[j,'Unbound']== True)], dflist[n].loc[j,'radz'][(dflist[n].loc[j,'Unbound']== True)],\
           s=6.0, c='goldenrod', label='Ejected stars')

    ax.view_init(30, 135)
    ax.grid(False)
#ax.set(xlim=(-5., 5.), ylim=(-5., 5.), zlim=(-5., 5.))
#ax.set(xlim=(-2., 2.), ylim=(-2., 2.), zlim=(-2., 2.))



#%%

snaps = 101

HMUB_AllHM_fraction = np.zeros((nlines, snaps))
LMUB_AllLM_fraction = np.zeros((nlines, snaps))

for n, i in product(range(nlines), range(snaps)):

    LMUB_AllLM_fraction[n, i] = Fraction(len(dflist[n].loc[i][(dflist[n].loc[i, 'mass']<= 2) \
                  & (dflist[n].loc[i,'Unbound']== True)]), \
                len(dflist[n].loc[i][(dflist[n].loc[i, 'mass'] <= 2)]))

    if len(dflist[n].loc[i][(dflist[n].loc[i, 'mass']>= 8.)]) != 0:
        HMUB_AllHM_fraction[n, i] = Fraction(len(dflist[n].loc[i][(dflist[n].loc[i, 'mass']>= 8.) \
                          & (dflist[n].loc[i, 'Unbound']== True)]), \
                        len(dflist[n].loc[i][(dflist[n].loc[i, 'mass']>= 8.)]))
    else:
        continue
    
x = np.arange(0., 10.1, 0.1)

for n in range(nlines):
    fig, ax = plt.subplots()
    plt.subplots_adjust(top=0.95, bottom=0.135, left=0.106, right=0.968)
    ax.plot(x, LMUB_AllLM_fraction[n],  label ='Low-mass', c='steelblue')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.plot(x, HMUB_AllHM_fraction[n], label ='High-mass', c='seagreen')
    ax.tick_params(which='both', direction='in')

    ax.set_xlabel('Cluster age (Myr)')
    ax.set_ylabel('Ejected fraction')
    ax.set_xlim(0., 10.1)
    ax.set_ylim(-0.01, 0.5)
    ax.set_title('Sim %s' %(dname[n]))
    plt.savefig('Unbound_fraction_bymass%s.png' %dname[n])

plt.show()  

#    plt.savefig('Unbound_fraction_bymass%s.png' %fname[i])
