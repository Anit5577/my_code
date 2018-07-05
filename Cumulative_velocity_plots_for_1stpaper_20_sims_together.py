#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:14:58 2018

@author: php17cs
"""

import pandas as pd
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import PercentFormatter
from scipy import stats
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#%% reading in all files with 20 simulations All_read

from function_file import read_in_summary_datafiles

All_read, fname, nlines = read_in_summary_datafiles('file20.txt')

#%% to compare the same length of simulations with different initial conditions

fig3, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
fig3.set_size_inches(12.69, 7.27)
plt.tight_layout()
plt.subplots_adjust(top=0.92, bottom=0.083, left=0.052, right=0.981, hspace=0.2, wspace=0.4)

n = 50
#all_init = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#
all_init_1_6 = [2, 12]
all_init_3_0 = [3, 13]


velocity = 'PM-velxy'          # add column name of velocity to plot

for i, j in zip(all_init_1_6, all_init_3_0):

    ax1.scatter(All_read[i].loc[n].sort_values(velocity)[velocity], \
               np.linspace(1/len(All_read[i].loc[n]), 1.0, len(All_read[i].loc[n])), s=0.5, \
               label=(r'D=%s, $alpha_{vir}$=%s, $N_{sim}$=%s'%(\
                      fname[i][11:14], fname[i][15:18], fname[i][25:29])))
#
#    ax2.scatter(np.sort(random.choice(All_read[i].loc[n,velocity], 2000)), \
#               np.linspace(1/2000, 1.0, 2000), s=0.5, \
#               label=(r'%s-velocity D=%s, $alpha_{vir}$=%s'%(velocity[0:2], \
#                      fname[i][11:14], fname[i][15:18])))


    ax2.scatter(All_read[j].loc[n].sort_values(velocity)[velocity], \
               np.linspace(1/len(All_read[j].loc[n]), 1.0, len(All_read[j].loc[n])), s=0.5, \
               label=(r'D=%s, $alpha_{vir}$=%s, $N_{sim}$=%s'%(\
                      fname[j][11:14], fname[j][15:18], fname[j][25:29])))
    
## chosing 2,000 stars at random 
#    ax2.scatter(np.sort(random.choice(All_read[j].loc[n, velocity], 2000)), \
#               np.linspace(1/2000, 1.0, 2000), s=0.5, \
#               label=(r'%s-velocity D=%s, $alpha_{vir}$=%s'%(velocity[0:2], \
#                      fname[j][11:14], fname[j][15:18])))

for ax in [ax1, ax2]:

    ax.set_ylabel('Cumulative distribution', fontsize=10.)
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax.tick_params(which='both', direction='in', top=True, right=True, labelbottom=True)
    ax.set_xlim(0.1, 10.)
    ax.set_ylim(0., 1.03)
#    ax.legend(loc='lower right', frameon=False, fontsize=8.)
    ax.set_xscale('log')
    ax.legend(title='Cluster age %s Myr'\
              %(np.round(All_read[0].loc[n].iloc[0]['time'], decimals=1)),\
              loc='upper left', frameon=False, fontsize=8.)


    ax.set_xlabel('Proper motion [km/s]', fontsize=10.)
#ax1.set_title('N = 20,000 stars (1,000 stars from 20 simulations)', fontsize=10.)

#ax2.set_title('N = 2,000 stars randomly chosen from total', fontsize=10.)

#fig3.suptitle('Cluster age %s Myr'\
#              %(np.round(All_read[0].loc[n].iloc[0]['time'], decimals=1)), fontsize=12.)
#
plt.show()

#%% to compare two different sets of data with different length
#
#fig3, ax = plt.subplots()
#
#n = 1
#file_1 = [2]
#
#file_2 = [3]
#
#velocity = 'PM-velxy'          # add column name of velocity to plot
#velocity_alt = '3D-velxyz'
#
#for i, j in zip(file_1, file_2):
#
#    ax.scatter(All_read[i].loc[n].sort_values(velocity)[velocity], \
#               np.linspace(1/len(All_read[i].loc[n]), 1.0, len(All_read[i].loc[n])), s=0.5, \
#               label=(r'%s-velocity, D=%s, $alpha_{vir}$=%s'%(velocity[0:2], \
#                      fname[i][11:14], fname[i][15:18])))
#    ax.scatter(All_read[i].loc[n].sort_values(velocity_alt)[velocity_alt], \
#               np.linspace(1/len(All_read[i].loc[n]), 1.0, len(All_read[i].loc[n])), s=0.5, \
#               label=(r'%s-velocity, D=%s, $alpha_{vir}$=%s'%(velocity_alt[0:2], \
#                      fname[i][11:14], fname[i][15:18])))
#
#    ax.legend(loc='lower right', frameon=False, \
#               title=('Cluster age %s Myr'\
#                      %(np.round(All_read[i].loc[n].iloc[1]['time'], decimals=2))), fontsize=8.)
#
##    ax.legend(loc='upper left', frameon=False, \
##               title=('Cluster age %s Myr'\
##                      %(np.round(All_read[i].loc[n].iloc[1]['time'], decimals=2))), fontsize=8.)
#
#ax.set_xlabel('%s velocity (km/s)'%velocity[0:2], fontsize=10.)
#ax.set_ylabel('Cumulative distribution', fontsize=10.)
#
#ax.set_xlim(0., 10.)
#ax.set_ylim(0., 1.03)
#ax.set_title('Cumulative %s Velocity distributions'\
#             %velocity[0:2], fontsize=12.)
##ax.set_xscale('log')
#
#plt.show()

#%% Kolmogorov-Smirnof 2 sample test to dobuble-check how similar two
#distribustions are to each other (applies to the combined 20 simulations)

i = (8) #All_read initial condition dataset x
j = (9) #All_read initial condition dataset y

data1 = All_read[i].loc[100].sort_values(velocity)[velocity]
data2 = All_read[j].loc[100].sort_values(velocity)[velocity]
data3 = All_read[i].loc[50].sort_values(velocity)[velocity]
data4 = All_read[j].loc[50].sort_values(velocity)[velocity]
data5 = All_read[i].loc[10].sort_values(velocity)[velocity]
data6 = All_read[j].loc[10].sort_values(velocity)[velocity]
data7 = All_read[i].loc[1].sort_values(velocity)[velocity]
data8 = All_read[j].loc[1].sort_values(velocity)[velocity]

k = []
l = []
pvalue1 = []
pvalue2 = []
pvalue3 = []
pvalue4 = []

step = 50 # arbitrary choice of steps size, number of stars compared in each step

for k, l in zip(range(0, 20001-step, step), range(step, 20001, step)):
#    print (i,j)
    #    print(stats.ks_2samp(data1[i:j], data2[i:j]))
    pvalue1.append((stats.ks_2samp(data1[k:l], data2[k:l])[1])*100)
    pvalue2.append((stats.ks_2samp(data3[k:l], data4[k:l])[1])*100)
    pvalue3.append((stats.ks_2samp(data5[k:l], data6[k:l])[1])*100)
    pvalue4.append((stats.ks_2samp(data7[k:l], data8[k:l])[1])*100)

x = np.arange(1, 20001, step)

fig6, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
plt.subplots_adjust(hspace=0.1, wspace=0.1)

ax4.scatter(x, pvalue1, s=1.0, label=('10 Myr'))
ax3.scatter(x, pvalue2, s=1.0, label=('5 Myr'))
ax2.scatter(x, pvalue3, s=1.0, label=('1 Myr'))
ax1.scatter(x, pvalue4, s=1.0, label=('0.1 Myr'))
ax1.set_ylabel('P-value')
ax3.set_ylabel('P-value')
ax3.set_xlabel('N-stars')
ax4.set_xlabel('N-stars')
fig6.suptitle(r'Two-sample Kolmogorov-Smirnoff: D=%s with $\alpha_{vir}$=%s vs $\alpha_{vir}$=%s'\
              %(fname[i][11:14], fname[i][15:18], fname[j][15:18]))

axes = [ax1, ax2, ax3, ax4]
x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

for ax in axes:
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)
    ax.tick_params(which='both', direction='in', top='on', right='on')
    ax.axhline(5, label=('5% significance level'), lw=1.0, c='red')
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.legend(frameon=False, fontsize=8.)
    ax.set_ylim(0., 100.)
    ax.set_xlim(0., 20000.)

plt.show()

#%% plots cumulative distribution of a defined initial condition set at 4 different ages.

fig4, ax = plt.subplots()

velocity = 'PM-velxy'

init_cond = [0] # define initial condition set, based on position in file20.txt

for j in init_cond:

    ax.scatter(All_read[j].loc[1].sort_values(velocity)[velocity], \
               np.linspace(1/len(All_read[j].loc[1]), 1.0, len(All_read[j].loc[1])), s=0.5, \
               label=('%s Myr'%(np.round(All_read[j].loc[1].iloc[1]['time'], decimals=2))))
    ax.scatter(All_read[j].loc[10].sort_values(velocity)[velocity], \
               np.linspace(1/len(All_read[j].loc[10]), 1.0, len(All_read[j].loc[10])), s=0.5, \
               label=('%s Myr'%(np.round(All_read[j].loc[10].iloc[1]['time'], decimals=2))))
    ax.scatter(All_read[j].loc[50].sort_values(velocity)[velocity], \
               np.linspace(1/len(All_read[j].loc[50]), 1.0, len(All_read[j].loc[50])), s=0.5, \
               label=('%s Myr'%(np.round(All_read[j].loc[50].iloc[1]['time'], decimals=2))))
    ax.scatter(All_read[j].loc[100].sort_values(velocity)[velocity], \
               np.linspace(1/len(All_read[j].loc[100]), 1.0, len(All_read[j].loc[100])), s=0.5, \
               label=('%s Myr'%(np.round(All_read[j].loc[100].iloc[1]['time'], decimals=2))))

    ax.set_title('Cumulative PM-velocity distributions at different times: \n D=%s, $alpha_{vir}=%s$'\
                 %(fname[j][11:14], fname[j][15:18]), fontsize=12.)

ax.set_xlabel('Velocity (log(km/s))', fontsize=10.)
ax.set_ylabel('Cumulative distribution', fontsize=10.)
ax.legend(loc='lower right', frameon=False, title=('Cluster age:'))
ax.set_xlim(0., 10.)
ax.set_ylim(0., 1.03)
#ax.set_xscale('log')

plt.show()

#%% PP-plot checking similarity of distributions

fig5, ax = plt.subplots()

#time = [1,10,50,100]
i = (0)  # dataset 1 to compare
j = (2)  # dataset 2 to compare

data1 = All_read[i].loc[100].sort_values(velocity)[velocity]
data2 = All_read[j].loc[100].sort_values(velocity)[velocity]
data3 = All_read[i].loc[50].sort_values(velocity)[velocity]
data4 = All_read[j].loc[50].sort_values(velocity)[velocity]
data5 = All_read[i].loc[10].sort_values(velocity)[velocity]
data6 = All_read[j].loc[10].sort_values(velocity)[velocity]
data7 = All_read[i].loc[1].sort_values(velocity)[velocity]
data8 = All_read[j].loc[1].sort_values(velocity)[velocity]


ax.scatter(data1, data2, s=0.5, label='%d Myr'%(100/10))
ax.scatter(data3, data4, s=0.5, label='%d Myr' %(50/10))
ax.scatter(data5, data6, s=0.5, label='%d Myr' %(10/10))
ax.scatter(data7, data8, s=0.5, label='%s Myr' %(1./10.))
ax.plot(data1, data1, color='red', linewidth=0.5, label='Equal distribution')
ax.set_xlabel(r'PM-velocity (km/s): D=%s, $\alpha_{vir}$=%s'\
              %(fname[i][11:14], fname[i][15:18]), fontsize=10.)
ax.set_ylabel(r'PM-velocity (km/s): D=%s, $\alpha_{vir}$=%s'\
              %(fname[j][11:14], fname[j][15:18]), fontsize=10.)
ax.legend(loc='upper left', frameon=False)
ax.set_xlim(0., 5.)
#ax.set_xticklabels(tick_labels.astype(int))
ax.set_ylim(0., 5.)
ax.set_title('PP-plot of cumulative velocity distributions', fontsize=12.)
#ax.set_xscale('log')

plt.show()

#%% violin plots for all initial conditions showing them together at defined snapshots

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
plt.subplots_adjust(wspace=0.01)

n = 50
#all_init_1_6 = [0, 1, 2, 3, 4]
#all_init_3_0 = [5, 6, 7, 8, 9]

velocity = 'PM-velxy'          # add column name of velocity to plot
    
ax1.violinplot([(All_read[i].loc[n][velocity]) for i in all_init_1_6], showmeans=False, showmedians=True, showextrema=True)
ax2.violinplot([(All_read[j].loc[n][velocity]) for j in all_init_3_0], showmeans=False, showmedians=True, showextrema=True)

pos = np.arange(len(all_init_1_6))

for ax in [ax1, ax2]:
    ax.get_xaxis().set_tick_params(direction='in')
    ax.get_yaxis().set_tick_params(which='both', direction='in', right=True)
    ax.set_xticks(pos+1)
    ax.set_yscale('log')

ax1.set_xlabel('D=%s'%fname[0][11:14])
ax2.set_xlabel('D=%s'%fname[5][11:14])
ax1.set_ylabel('PM-velocity (km/s)')

ax1.set_xticklabels([(r'$\alpha_{vir}$=%s'%fname[i][15:18]) for i in all_init_1_6], fontsize=10.)
ax2.set_xticklabels([(r'$\alpha_{vir}$=%s'%fname[j][15:18]) for j in all_init_3_0], fontsize=10.)
ax2.get_yaxis().set_tick_params(labelright=True)

fig.suptitle('Violinplots of %s-velocity distribution at %s Myr'%(velocity[0:2],np.round(All_read[0].loc[n].iloc[1]['time'], decimals=1)))

ax1.set_xticklabels([(r'$\alpha_{vir}$=%s'%fname[i][15:18]) for i in all_init_1_6], fontsize=10.)
ax2.set_xticklabels([(r'$\alpha_{vir}$=%s'%fname[j][15:18]) for j in all_init_3_0], fontsize=10.)

plt.show()

#%% violin plots for a set of initial conditions showing 4 different snapshots together

fig6, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
plt.subplots_adjust(wspace=0.01)

i = (8) # define dataset to plot
j = (9) # define dataset to plot

plot1_data = [All_read[i].loc[1][velocity], All_read[i].loc[10][velocity], \
              All_read[i].loc[50][velocity], All_read[i].loc[100][velocity]]
plot_label = ['0.1 Myr', '1 Myr', '5 Myr', '10 Myr']
plot2_data = [All_read[j].loc[1][velocity], All_read[j].loc[10][velocity], \
              All_read[j].loc[50][velocity], All_read[j].loc[100][velocity]]

ax1.violinplot(plot1_data, showmeans=False, showmedians=False, showextrema=False)
ax2.violinplot(plot2_data, showmeans=False, showmedians=False, showextrema=False)

pos = np.arange(len(plot_label))

for ax in [ax1, ax2]:
    ax.get_xaxis().set_tick_params(direction='in')
    ax.get_yaxis().set_tick_params(direction='in', right='on')
    ax.set_xticks(pos+1)
    ax.set_ylim(-1., 10.) # axis limit set to allow focus on the shape of the distribution,
    ax.set_xticklabels(plot_label)

ax1.set_xlabel(r'D=%s, $\alpha_{vir}$=%s'%(fname[i][11:14], fname[i][15:18]))
ax2.set_xlabel(r'D=%s, $\alpha_{vir}$=%s'%(fname[j][11:14], fname[j][15:18]))
ax1.set_ylabel('PM-velocity (km/s)')
ax2.get_yaxis().set_tick_params(labelright=True)

fig6.suptitle('PM-velocity distributions at different cluster ages \
              \n 20 simulations combined with 20,000 stars total')

plt.show()
