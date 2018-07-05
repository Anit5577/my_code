#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 13:04:01 2018

@author: php17cs
"""

import numpy as np
from function_file import read_in_summary_datafiles, read_in_any_datafiles, energy_stars
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from itertools import product
from fractions import Fraction

#%% reading in all files with 20 simulations All_read

dflist, dname, nlines = read_in_any_datafiles('fileMod.txt')


#%%
#calculates energy of each star in each snapshot and adds this in a column
dflist = energy_stars(dflist, dname, nlines)

#%%

import matplotlib.pyplot as plt

snaps = 101

HMUB_AllHM_fraction = np.zeros((nlines, snaps))
LMUB_AllLM_fraction = np.zeros((nlines, snaps))

for i, n in product(range(nlines), range(snaps)):

    LMUB_AllLM_fraction[i,n] = Fraction(len(dflist[i].loc[n][(dflist[i].loc[n, 'mass']<= 2.5) \
                  & (dflist[i].loc[n,'Unbound']== True)]), \
                len(dflist[i].loc[n][(dflist[i].loc[n, 'mass'] <= 2.5)]))

    if len(dflist[i].loc[n][(dflist[i].loc[n, 'mass']>= 8.)]) != 0:
        HMUB_AllHM_fraction[i,n] = Fraction(len(dflist[i].loc[n][(dflist[i].loc[n, 'mass']>= 8.) \
                          & (dflist[i].loc[n, 'Unbound']== True)]), 6
                        len(dflist[i].loc[n][(dflist[i].loc[n, 'mass']>= 8.)]))
    else:
        continue

#%%
        
x = np.arange(0., 10.1, 0.1)

fig, ax = plt.subplots()

for i in range(1, nlines, 1):
#    fig, ax = plt.subplots()
    ax.plot(x, HMUB_AllHM_fraction[i], c='r')
    ax.plot(x, LMUB_AllLM_fraction[i], c='b')

for i in range(1):
#    fig, ax = plt.subplots()
    ax.plot(x, HMUB_AllHM_fraction[i], c='r', label ='High-mass >= 8M$_\odot$')
    ax.plot(x, LMUB_AllLM_fraction[i], c='b', label ='Low-mass <= 2.5M$_\odot$')

    ax.legend(loc='upper left', frameon=False, fontsize=8.)
    ax.set_xlabel('Cluster age (in Myr)')
    ax.set_ylabel('Unbound rate')
    ax.set_xlim(0., 10.1)
    ax.set_ylim(0., 0.5)
#    ax.set_title(r'D=3.0, $\alpha_{vir}$=, 2000 stars')
#    ax.set_yscale('log')
#    plt.savefig('Unbound_fraction_bymass%s.png')

plt.show()

#%%

for n in range(nlines):
    print (dflist[n].loc[(100,985),'mass'], dname[n])

#%%

print (dflist[18].loc[(slice(None),321),:])
print (dname[18])

#%% 

for n in range (nlines):    
    print (dname[n], HMUB_AllHM_fraction[n, 100])

#%%
n = 0
i=50

print (dname[n], HMUB_AllHM_fraction[n, i])
print (dflist[n].loc[i][(dflist[n].loc[i, 'mass']>= 8.) & (dflist[n].loc[i, 'Unbound']== True)])
print (dflist[n].loc[i][(dflist[n].loc[i, 'mass']>= 8.) & (dflist[n].loc[i, 'Unbound']== False)])



#%%

n=19
print (dflist[n].loc[100].nlargest(4, 'mass'))


#%%

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

nsnaps=101
n = 14

print (dflist[n].loc[0][(dflist[n].loc[0, 'mass']>= 8.)]['radx'])


fig, ax = plt.subplots(figsize=(8., 8.))

ax.set(xlim=(-1., 1.), ylim=(-1., 1.))
scat1 = ax.scatter((dflist[n].loc[0][(dflist[n].loc[0, 'mass']>= 8.)]['radx']), \
                   (dflist[n].loc[0][(dflist[n].loc[0, 'mass']>= 8.)]['rady']), s=2.0)

ax.set_xlabel('x [pc]')
ax.set_ylabel('y [pc]')
ax.legend(loc='upper right', frameon=False)

def animate(i):
    plotdata = dflist[n].loc[i][(dflist[n].loc[i, 'mass']>= 8.)]
    x_i = plotdata['radx']
    y_i = plotdata['rady']
    scat1.set_offsets(np.c_[x_i, y_i])

    ax.set_title('Cluster age %s Myr' %(np.round(dflist[n].loc[i].iloc[0]['time'],\
           decimals=2)))

anim = FuncAnimation(fig, animate, interval = 500, frames=nsnaps, repeat=False)

plt.draw()
plt.show()   


#%%
nsnaps=101
n = 1

fig, ax = plt.subplots(figsize=(8., 8.))

ax.set(xlim=(-1., 1.), ylim=(-1., 1.))
scat4 = ax.scatter((dflist[n].loc[0][(dflist[n].loc[0, 'mass']>= 8.)]['radx']), \
                   (dflist[n].loc[0][(dflist[n].loc[0, 'mass']>= 8.)]['rady']), s=2.0)
scat1 = ax.scatter(dflist[n].loc[(0,43),'radx'],dflist[n].loc[(0,43),'rady'], s=2.0, c='r')
scat2 = ax.scatter(dflist[n].loc[(0,490),'radx'],dflist[n].loc[(0,490),'rady'], s=2.0, c='r')
scat3 = ax.scatter(dflist[n].loc[(0,202),'radx'],dflist[n].loc[(0,202),'rady'], s=2.0, c='r')


ax.set_xlabel('x [pc]')
ax.set_ylabel('y [pc]')
ax.legend(loc='upper right', frameon=False)

def animate(i):
    plotdata = dflist[n].loc[i][(dflist[n].loc[i, 'mass']>= 8.)]
    x3_i = plotdata['radx']
    y3_i = plotdata['rady']    
    scat4.set_offsets(np.c_[x3_i, y3_i])
    x_i = dflist[n].loc[(i,43), 'radx']
    y_i = dflist[n].loc[(i,43), 'rady']
    scat1.set_offsets(np.c_[x_i, y_i])
    x1_i = dflist[n].loc[(i,490), 'radx']
    y1_i = dflist[n].loc[(i,490), 'rady']
    scat2.set_offsets(np.c_[x1_i, y1_i])
    x2_i = dflist[n].loc[(i,202), 'radx']
    y2_i = dflist[n].loc[(i,202), 'rady']
    scat3.set_offsets(np.c_[x2_i, y2_i])
    
    if i >60:
        ax.set(xlim=(-5., 5.), ylim=(-5., 5.))

    ax.set_title('Cluster age %s Myr' %(np.round(dflist[n].loc[i].iloc[0]['time'],\
           decimals=2)))

anim = FuncAnimation(fig, animate, interval = 500, frames=nsnaps, repeat=False)
