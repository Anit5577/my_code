#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 16:46:27 2018

@author: php17cs
"""

#Animation for Modest-18 conference to show cluster evolution in x-y plane

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation




filename = input('Choose data file to be read into array: ')

#'data_1rBC0p3F1p61pXXXS10_10.dat'

dflist = pd.read_csv(filename, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                         'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap', 'star'],\
                         usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                  'radz', 'velx', 'vely', 'velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, \
                                'mass': np.float64, 'radx':np.float64, 'rady':np.float64, \
                                'radz':np.float64, 'velx':np.float64, 'vely':np.float64, \
                                'velz':np.float64})

plt.rcParams.update(plt.rcParamsDefault)

#data_4D16p3F1p61pXXXnS01_10.dat

#%%




# ['seaborn-pastel', 'seaborn-paper', 'fast', 'seaborn-white', 'tableau-colorblind10', 'classic', 'seaborn-dark', \
#               'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-ticks', 'Solarize_Light2', 'seaborn-notebook', 'ggplot', \
#               'seaborn-bright', 'seaborn-colorblind', 'dark_background', '_classic_test', 'grayscale', 'seaborn-deep', 'seaborn', \
#               'seaborn-muted', 'fivethirtyeight', 'seaborn-whitegrid', 'seaborn-talk', 'seaborn-poster', 'bmh']

plt.style.use('seaborn-poster')

fig, ax = plt.subplots(figsize=(8., 8.))
#ax.set(xlim=(-20., 20.), ylim=(-20., 20.))

#fig.set_facecolor('#002342')
plt.setp(ax.spines.values(), linewidth=4)
#ax.set_facecolor('#002342')

ax.spines['bottom'].set_color('#002342')
ax.spines['top'].set_color('#002342')
ax.spines['left'].set_color('#002342')
ax.spines['right'].set_color('#002342')
ax.xaxis.label.set_color('#002342')
ax.yaxis.label.set_color('#002342')


ax.set_xlabel('x (pc)', fontsize=16.)
ax.set_ylabel('y (pc)', fontsize=16.)
ax.set(xlim=(-60., 60.), ylim=(-60., 60.))

ax.scatter(dflist[0].loc[100,'radx'],dflist[0].loc[100,'rady'], s=10.0, label='Cluster stars')
#ax.scatter(dflist.loc[0,'radx'],dflist.loc[0,'rady'], s=10.0, label='Cluster age %s Myr' %(np.round(dflist.loc[0].iloc[0]['time'],\
#       decimals=1)))
ax.scatter(dflist[0].loc[100,'radx'][(dflist[0].loc[100,'Unbound']== True) & (dflist[0].loc[100,'PM-velxy'] > 2.5)],dflist[0].loc[100,'rady']\
           [(dflist[0].loc[100,'Unbound']== True) & (dflist[0].loc[100,'PM-velxy'] > 2.5)], s=15.0, c='goldenrod', label='Ejected stars') 


ax.tick_params(which='both', direction='in', top=True, right=True, length=8., width=3., labelsize=12., colors='#002342')
plt.show()

#ax.set_title('Cluster age %s Myr' %(np.round(dflist[0].loc[100].iloc[0]['time'],\
#       decimals=1)), fontsize=16., color='#002342')

leg = ax.legend(loc='upper right', frameon=False, fontsize=16.)    

for text in leg.get_texts():
    text.set_color('#002342')
    
plt.show()
plt.savefig('Poster_image__1.png', transparent=True, dpi=600 )

#%%

nsnaps = 101

fig, ax = plt.subplots(figsize=(7., 7.))
plt.subplots_adjust(top=0.941, bottom=0.105, left=0.127, right=0.96)
fig.set_facecolor('#002342')
plt.setp(ax.spines.values(), linewidth=2)
ax.set_facecolor('#002342')

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
            
                 
ax.set_xlabel('x (pc)', fontsize=16.)
ax.set_ylabel('y (pc)', fontsize=16.)
ax.set(xlim=(-2., 2.), ylim=(-2., 2.))
ax.tick_params(which='both', direction='in', top=True, right=True, length=8., \
               width=2., labelsize=12., colors='white')
#ax.tick_params(which='both', direction='in', top=True, right=True, length=8., width=2., labelsize=12.)
scat = ax.scatter(dflist.loc[0,'radx'],dflist.loc[0,'rady'], s=2.0, c='powderblue')
scatM = ax.scatter(dflist.loc[0][dflist.loc[0, 'mass'] >= 8.]['radx'], dflist.loc[0][dflist.loc[0, 'mass'] >= 8.]['rady'] , c='r', s=15.0)

#scat = ax.scatter(dflist.loc[0,'radx'],dflist.loc[0,'rady'], s=3.0)

def animate(i):
    x_i = dflist.loc[i, 'radx']
    y_i = dflist.loc[i, 'rady']
    scat.set_offsets(np.c_[x_i, y_i])
    xM_i = dflist.loc[i][dflist.loc[i, 'mass'] >= 8.]['radx']
    yM_i = dflist.loc[i][dflist.loc[i, 'mass'] >= 8.]['rady']
    scatM.set_offsets(np.c_[xM_i, yM_i])
#    ax.set_title('Cluster age %s Myr' %(np.round(dflist.loc[i].iloc[1]['time'],\
#               decimals=1)), color='white')
    ax.set_title('Cluster age %s Myr' %(np.round(dflist.loc[i].iloc[1]['time'],\
           decimals=2)), fontsize=12., color='white')
    ax.set(xlim=(-2., 2.), ylim=(-2., 2.))
    if i > 200:
        ax.set(xlim=(-10., 10.), ylim=(-10., 10.))
#    if i > 15:
#        max_i = np.max(dflist.loc[15, 'rady'])
#        ax.set(xlim=(-max_i, max_i), ylim=(-max_i, max_i))

#def animate1(i):
#    x_i = dflist.loc[i+25, 'radx']
#    y_i = dflist.loc[i+25, 'rady']
#    scat.set_offsets(np.c_[x_i, y_i])
##    ax.set_title('Cluster age %s Myr' %(np.round(dflist.loc[i+25].iloc[1]['time'],\
##               decimals=1)), color='white')
#    ax.set_title('Cluster age %s Myr' %(np.round(dflist.loc[i+25].iloc[1]['time'],\
#           decimals=1)))
#    max_i = np.max(dflist.loc[25, 'rady'])
#    ax.set(xlim=(-max_i, max_i), ylim=(-max_i, max_i))
#    if i > 25:
#        max_i = np.max(dflist.loc[50, 'rady'])
#        ax.set(xlim=(-max_i, max_i), ylim=(-max_i, max_i))
#    if i > 50:
#        max_i = np.max(dflist.loc[75, 'rady'])
#        ax.set(xlim=(-max_i, max_i), ylim=(-max_i, max_i))

for n in range(nsnaps):
    anim = FuncAnimation(fig, animate, interval = 800, frames=nsnaps, repeat=False)

plt.draw()
plt.show()

#%%

anim.save('Modest_faster_massive_%s.mp4' %filename, fps=4, extra_args=['-vcodec', 'libx264'], \
          savefig_kwargs={'facecolor':'#002342'})

#%%

filename = input('Choose data file to be read into array: ')

#'data_1rBC0p3F1p61pXXXS10_10.dat'

dflist = pd.read_csv(filename, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                         'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap', 'star'],\
                         usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                  'radz', 'velx', 'vely', 'velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, \
                                'mass': np.float64, 'radx':np.float64, 'rady':np.float64, \
                                'radz':np.float64, 'velx':np.float64, 'vely':np.float64, \
                                'velz':np.float64})

nsnaps = 101

#%%

nsnaps = 101

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8., 8.), sharex=True, sharey=True)

ax1.plot(221)
ax2.plot(222)
ax3.plot(223)
ax4.plot(223)

ax1.set(xlim=(-2., 2.), ylim=(-2., 2.))
scat = ax1.scatter(dflist.loc[0,'radx'],dflist.loc[0,'rady'], s=2.0, c='grey')
scat1 = ax2.scatter(dflist.loc[0,'radx'],dflist.loc[0,'radz'], s=2.0, c='grey')
scat2 = ax3.scatter(dflist.loc[0,'rady'],dflist.loc[0,'radz'], s=2.0, c='grey')
#scatM = ax.scatter(dflist.loc[0][dflist.loc[0, 'mass'] >= 8.]['radx'], dflist.loc[0][dflist.loc[0, 'mass'] >= 8.]['rady'] , c='r', s=5.0)

#for ax in [ax1, ax2, ax3, ax4]:
#    ax.set_xlabel('x [pc]')
#    ax.set_ylabel('y [pc]')
#    ax.set_zlabel('z [pc]')

def animate(i):
    x_i = dflist.loc[i, 'radx']
    y_i = dflist.loc[i, 'rady']
    z_i = dflist.loc[i, 'radz']
    scat.set_offsets(np.c_[x_i, y_i])
    scat1.set_offsets(np.c_[x_i, z_i])
    scat2.set_offsets(np.c_[y_i, z_i])
#    xM_i = dflist.loc[i][dflist.loc[i, 'mass'] >= 8.]['radx']
#    yM_i = dflist.loc[i][dflist.loc[i, 'mass'] >= 8.]['rady']
#    scatM.set_offsets(np.c_[xM_i, yM_i])
    ax.set_title('Cluster age %s Myr' %(np.round(dflist.loc[i].iloc[0]['time'],\
           decimals=2)))

anim = FuncAnimation(fig, animate, interval = 300, frames=nsnaps, repeat=False)

plt.draw()
plt.show()


#anim.save('Modest_ani%s.mp4' %filename, fps=3, extra_args=['-vcodec', 'libx264'])

#%% 3D- animation

#plt.style.use('seaborn-dark-palette')

nsnaps = 101

import mpl_toolkits.mplot3d.axes3d as p3

fig = plt.figure()
ax = p3.Axes3D(fig)

ax.set_xlabel('x [pc]')
ax.set_ylabel('y [pc]')
ax.set_zlabel('z [pc]')

scatM = ax.scatter(dflist.loc[0][dflist.loc[0, 'mass'] >= 8.]['radx'], dflist.loc[0][dflist.loc[0, 'mass'] >= 8.]['rady'], \
                   dflist.loc[0][dflist.loc[0, 'mass'] >= 8.]['radz'], c='r', s=5.0)
scat = ax.scatter(dflist.loc[0, 'radx'],  dflist.loc[0, 'rady'], dflist.loc[0, 'radz'] , s=1.0, c='grey')

ax.view_init(35, 135)
#ax.set(xlim=(-5., 5.), ylim=(-5., 5.), zlim=(-5., 5.))
ax.set(xlim=(-2., 2.), ylim=(-2., 2.), zlim=(-2., 2.))
ax.grid(False)

def in3D_animate(i):
    if i > 200:
        ax.set(xlim=(-5., 5.), ylim=(-5., 5.), zlim=(-5., 5.))
    if i > 500:
        ax.view_init(30, 135) 
        ax.set(xlim=(-20., 20.), ylim=(-20., 20.), zlim=(-20., 20.))
    xM_i = dflist.loc[i][dflist.loc[i, 'mass'] >= 8.]['radx']
    yM_i = dflist.loc[i][dflist.loc[i, 'mass'] >= 8.]['rady']
    zM_i = dflist.loc[i][dflist.loc[i, 'mass'] >= 8.]['radz']
    scatM._offsets3d = (xM_i, yM_i, zM_i)
    x_i = dflist.loc[i, 'radx']
    y_i = dflist.loc[i, 'rady']
    z_i = dflist.loc[i, 'radz']
    scat._offsets3d = (x_i, y_i, z_i)
    
    fig.suptitle('Cluster age %s Myr' %(np.round(dflist.loc[i].iloc[0]['time'],\
           decimals=2)))
    
    

in3D_ani = FuncAnimation(fig, in3D_animate, interval=200, frames=nsnaps, repeat=False)

plt.draw()
plt.show()

#data_1rBC0p3F1p1MpXXXS10_02.dat good for initial collapse

#%%

in3D_ani.save('Modest_3D_ani%s.mp4' %filename, fps=3, dpi=300, extra_args=['-vcodec', 'libx264'])


#%%


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

nsnaps=101
n = 6

fig, ax = plt.subplots(figsize=(8., 8.))

ax.set(xlim=(-5., 5.), ylim=(-5., 5.))
scat4 = ax.scatter(dflist[n].loc[(0),'radx'],dflist[n].loc[(0),'rady'], s=2.0, c='grey', alpha=0.5)
scat1 = ax.scatter(dflist[n].loc[(0,653),'radx'],dflist[n].loc[(0,653),'rady'], s=5.0, c='b', label='HM')
scat2 = ax.scatter(dflist[n].loc[(0,764),'radx'],dflist[n].loc[(0,764),'rady'], s=5.0, c='r', label='HM')
scat3 = ax.scatter(dflist[n].loc[(0,175),'radx'],dflist[n].loc[(0,175),'rady'], s=2.0, c='g', label='VLM')


ax.set_xlabel('x [pc]')
ax.set_ylabel('y [pc]')
ax.legend(loc='upper right', frameon=False)

def animate(i):
    x3_i = dflist[n].loc[(i), 'radx']
    y3_i = dflist[n].loc[(i), 'rady']
    scat4.set_offsets(np.c_[x3_i, y3_i])
    x_i = dflist[n].loc[(i,653), 'radx']
    y_i = dflist[n].loc[(i,653), 'rady']
    scat1.set_offsets(np.c_[x_i, y_i])
    x1_i = dflist[n].loc[(i,764), 'radx']
    y1_i = dflist[n].loc[(i,764), 'rady']
    scat2.set_offsets(np.c_[x1_i, y1_i])
    x2_i = dflist[n].loc[(i,175), 'radx']
    y2_i = dflist[n].loc[(i,175), 'rady']
    scat3.set_offsets(np.c_[x2_i, y2_i])

    ax.set_title('Cluster age %s Myr' %(np.round(dflist[n].loc[i].iloc[0]['time'],\
           decimals=2)))

anim = FuncAnimation(fig, animate, interval = 200, frames=nsnaps, repeat=False)

plt.draw()
plt.show()   
 
#%%

anim.save('Binary_check_data_1D30p3F1p61pXXXnS03_07.mp4', fps=3, extra_args=['-vcodec', 'libx264'])   