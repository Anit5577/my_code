#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:14:58 2018

@author: php17cs
"""

#this code calculates and plots the cumulative PM and 3D velocity for all
#snaps in all simulations that are read in from an input text file

#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import PercentFormatter
from scipy import stats
import seaborn as sns

#%%

from function_file import read_in_any_datafiles, velocity_elements,\
energy_stars, plots_legend, concat_simulations, COD_corrected_location

#reads in the .dat files from an inputfile list
dflist, dname, nlines = read_in_any_datafiles('file.txt')

#%%

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

#%%This saves all 20 simulations for a set of initial conditions into 1 file
#defines a filename based on the intial conditions

All, filename = concat_simulations(dflist, dname, nlines)

#saves the file with All n-simulations into one file, chosing 8 columns from
#a total of 26; chosing less columns to reduce the total filesize.

#All.to_csv('All_%s.csv' %filename[0], columns=['time', \
#           'mass', 'PM-velxy', '3D-velxyz', \
#           'Unbound'], index=True, index_label=['snap', 'star'])

All.to_csv('All_%s.csv' %filename[0], columns=['time', \
           'mass', 'radval', 'PM-velxy', '3D-velxyz', \
           'Unbound'], index=True, index_label=['snap', 'star'])

#%% creates cumulative velocity plots at 3 times showing all
#20 simulations of the currently loaded list in file.txt

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharey=True)
plt.tight_layout()
plt.subplots_adjust(hspace=0.01, wspace=0.01, top=0.92, bottom=0.07)
fig.set_size_inches(11.69, 8.27)

#fig1, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, sharey=True)
#plt.subplots_adjust(hspace=0.01, wspace=0.04)
#fig2, ((ax3, ax4)) = plt.subplots(nrows=1, ncols=2, sharey=True)
#plt.subplots_adjust(hspace=0.01, wspace=0.04)
#
#fig1.set_size_inches(11.69, 8.27)
#fig2.set_size_inches(11.69, 8.27)

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

velocity = 'PM-velxy' #defined type of velocity to plot
snaps = [0, 10, 50, 100]   # 4 defined times

for n in range(nlines):
    ax1.scatter(dflist[n].loc[snaps[0]].sort_values(velocity)[velocity], \
                np.linspace(1/len(dflist[n].loc[snaps[0]]), 1.0, len(dflist[n].loc[snaps[0]])), s=0.5)
    ax2.scatter(dflist[n].loc[snaps[1]].sort_values(velocity)[velocity], \
                np.linspace(1/len(dflist[n].loc[snaps[1]]), 1.0, len(dflist[n].loc[snaps[1]])), s=0.5)
    ax3.scatter(dflist[n].loc[snaps[2]].sort_values(velocity)[velocity], \
                np.linspace(1/len(dflist[n].loc[snaps[2]]), 1.0, len(dflist[n].loc[snaps[2]])), s=0.5)
    ax4.scatter(dflist[n].loc[snaps[3]].sort_values(velocity)[velocity], \
                np.linspace(1/len(dflist[n].loc[snaps[3]]), 1.0, len(dflist[n].loc[snaps[3]])), s=0.5)
      

#ax1.legend(loc='lower right', frameon=False, title='Cluster age: 0.1 Myr')
#ax2.legend(loc='lower right', frameon=False, title='Cluster age: 1.0 Myr')
#ax3.legend(loc='lower right', frameon=False, title='Cluster age: 5.0 Myr')
#ax4.legend(loc='lower right', frameon=False, title='Cluster age: 10.0 Myr')

ax1.legend(loc='upper left', frameon=False, title='Cluster age: 0.1 Myr')
ax2.legend(loc='upper left', frameon=False, title='Cluster age: 1.0 Myr')
ax3.legend(loc='upper left', frameon=False, title='Cluster age: 5.0 Myr')
ax4.legend(loc='upper left', frameon=False, title='Cluster age: 10.0 Myr')

#fig2.suptitle('Proper motion distributions of %s simulations with initial conditions: \n %s'\
# %(nlines, legend[0]), fontsize=12.)
#fig1.suptitle('Proper motion distributions of %s simulations with initial conditions: \n %s'\
# %(nlines, legend[0]), fontsize=12.)
fig.suptitle('%s-velocity distributions of %s simulations with initial conditions: \n %s'\
             %(velocity[0:2],nlines, legend[0]), fontsize=12.)

ax1.set_xlabel('Velocity (km/s)', fontsize=10.)
ax2.set_xlabel('Velocity (km/s)', fontsize=10.)
ax3.set_xlabel('Velocity (km/s)', fontsize=10.)
ax4.set_xlabel('Velocity (km/s)', fontsize=10.)
ax1.set_ylabel('Cumulative distribution', fontsize=10.)
ax3.set_ylabel('Cumulative distribution', fontsize=10.)


for ax in [ax1, ax2, ax3, ax4]:
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)
    ax.tick_params(which='both', direction='in', top='on', right='on')
    ax.set_xscale('log')
#    ax.set_ylim(0., 1.03)
    
#ax1.set_xlim(0.)
#ax2.set_xlim(0.)
#ax3.set_xlim(0.)
#ax4.set_xlim(0.)


#plt.savefig('Scatter_%s.png' %filename[0])
  
    
#%% this plots a set of 20 single initial condition curves in the background (grey) and then adds the averages of a defined set of multiple initial conditions.   
#
from function_file import read_in_any_datafiles

dflist, fname, nlines = read_in_any_datafiles('file.txt')
dflist = velocity_elements(dflist, dname, nlines)
    
j = 50    
    
fig1, ax = plt.subplots()
plt.tight_layout()
plt.subplots_adjust(hspace=0.01, wspace=0.01, top=0.92, bottom=0.07)
fig1.set_size_inches(11.69, 8.27)
 
x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

velocity = 'PM-velxy' #defined type of velocity to plot

for n in range(nlines):
   
   ax.scatter(dflist[n].loc[j].sort_values(velocity)[velocity], \
                np.linspace(1/len(dflist[n].loc[j]), 1.0, len(dflist[n].loc[j])), s=0.5, color='grey')
#    ax.scatter(All_read[n].loc[j].sort_values(velocity)[velocity], \
#                np.linspace(1/len(All_read[n].loc[j]), 1.0, len(All_read[n].loc[j])), s=0.5, color='grey')    


import pandas as pd   
f = open('fileMean.txt')
lines = [line.rstrip('\n') for line in f]

nlines = len(lines)

A = {}
for x in range(1, nlines+1, 1):
    A['fname{0}'.format(x)] = lines[x-1]

f.close()

fname = sorted(A.values())

Mean_PM_list = []

for n in range(nlines):
    Mean_PM_list.append(n)
    Mean_PM_list[n] = pd.read_csv(fname[n], header=None)     

for n in [5,6,7,8,9]:    
    ax.scatter(Mean_PM_list[n], np.linspace(1/len(Mean_PM_list[n]), 1.0, len(Mean_PM_list[n])), \
               s=0.5, label=r'D=%s, $\alpha_{vir}$=%s' %(fname[n][15:18], fname[n][19:22]))
  
ax.legend(loc='upper left', frameon=False, title='Cluster age: 5.0 Myr')
ax.set_xlabel('Velocity (km/s)', fontsize=10.)
ax.set_ylabel('Cumulative distribution', fontsize=10.)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which='both', direction='in', top='on', right='on')
ax.set_xscale('log')
ax.set_xlim(0.01, 10)
#
#fig1.suptitle('%s-velocity distributions of %s simulations with initial conditions: \n %s'\
#             %(velocity[0:2],nlines, legend[0]), fontsize=12.)
#
#fig1.suptitle('Mean %s-velocity distributions of different initial conditions'\
#              %(velocity[0:2]), fontsize=12.)

plt.show()

#%% pp plots of sumulations of the same initial conditions in separate plots

#time = [1,10,50,100]
velocity = 'PM-velxy' #defined type of velocity to plot

for i in range(nlines-1):

    fig5, ax = plt.subplots()

    data1 = dflist[i].loc[100].sort_values(velocity)[velocity]
    data2 = dflist[i+1].loc[100].sort_values(velocity)[velocity]
    data3 = dflist[i].loc[50].sort_values(velocity)[velocity]
    data4 = dflist[i+1].loc[50].sort_values(velocity)[velocity]
    data5 = dflist[i].loc[10].sort_values(velocity)[velocity]
    data6 = dflist[i+1].loc[10].sort_values(velocity)[velocity]
    data7 = dflist[i].loc[1].sort_values(velocity)[velocity]
    data8 = dflist[i+1].loc[1].sort_values(velocity)[velocity]

    ax.scatter(data1, data2, s=0.5, label='%d Myr'\
               %(np.round(dflist[i].loc[100].iloc[1]['time'], decimals=4)))
    ax.scatter(data3, data4, s=0.5, label='%d Myr'\
               %(np.round(dflist[i].loc[50].iloc[1]['time'], decimals=4)))
    ax.scatter(data5, data6, s=0.5, label='%d Myr'\
               %(np.round(dflist[i].loc[10].iloc[1]['time'], decimals=4)))
    ax.scatter(data7, data8, s=0.5, label='%s Myr'\
               %(np.round(dflist[i].loc[1].iloc[1]['time'], decimals=4)))

    ax.set_xlabel('%s (km/s), sim-%s'%(velocity, dname[i][25:27]))
    ax.set_ylabel('%s (km/s), sim-%s'%(velocity, dname[i+1][25:27]))
    ax.legend(loc='upper left', frameon=False)
    data1max = np.max(data1)
    data2max = np.max(data2)

    if data1max < data2max:
        ax.plot(data2, data2, color='red', linewidth=0.5, label='Equal distribution')
    else:
        ax.plot(data1, data1, color='red', linewidth=0.5, label='Equal distribution')

    axismax = max(data1max, data2max)
    ax.set_xlim(0., axismax)
    ax.set_ylim(0., axismax)
    fig5.suptitle('PP-plot of cumulative velocity distributions', fontsize=12.)
    ax.set_title(legend[0])

    plt.show()

    plt.savefig('PP-plot_%s_vs_%s_3.0_1.5.png' %(dname[i][25:27], dname[i+1][25:27]))

#%% Kolmogorov-Smirnof 2 sample test to dobuble-check how similar two
#distribustions are to each other (applies to the combined 20 simulations)

i = (8) #All_read initial condition dataset x
j = (9) #All_read initial condition dataset y

velocity = 'PM-velxy' #defined type of velocity to calculate

data1 = dflist[i].loc[100].sort_values(velocity)[velocity]
data2 = dflist[j].loc[100].sort_values(velocity)[velocity]
data3 = dflist[i].loc[50].sort_values(velocity)[velocity]
data4 = dflist[j].loc[50].sort_values(velocity)[velocity]
data5 = dflist[i].loc[10].sort_values(velocity)[velocity]
data6 = dflist[j].loc[10].sort_values(velocity)[velocity]
data7 = dflist[i].loc[1].sort_values(velocity)[velocity]
data8 = dflist[j].loc[1].sort_values(velocity)[velocity]
k = []
l = []
pvalue1 = []
pvalue2 = []
pvalue3 = []
pvalue4 = []

step = 50 # arbitrary choice of steps size, number of stars compared in each step

#use zip with two different value i and j that are used pairwise
for k, l in zip(range(0, 1001-step, step), range(step, 1001, step)):

    pvalue1.append((stats.ks_2samp(data1[k:l], data2[k:l])[1])*100)
    pvalue2.append((stats.ks_2samp(data3[k:l], data4[k:l])[1])*100)
    pvalue3.append((stats.ks_2samp(data5[k:l], data6[k:l])[1])*100)
    pvalue4.append((stats.ks_2samp(data7[k:l], data8[k:l])[1])*100)

x = np.arange(1, 1001, step)

fig6, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
plt.subplots_adjust(hspace=0.1, wspace=0.1)

ax4.scatter(x, pvalue1, s=1.0, \
            label=('%s Myr'%(np.round(dflist[i].loc[100].iloc[1]['time'], decimals=4))))
ax3.scatter(x, pvalue2, s=1.0, \
            label=('%s Myr'%(np.round(dflist[i].loc[50].iloc[1]['time'], decimals=4))))
ax2.scatter(x, pvalue3, s=1.0, \
            label=('%s Myr'%(np.round(dflist[i].loc[10].iloc[1]['time'], decimals=4))))
ax1.scatter(x, pvalue4, s=1.0, \
            label=('%s Myr'%(np.round(dflist[i].loc[1].iloc[1]['time'], decimals=4))))

ax1.set_ylabel('P-value')
ax3.set_ylabel('P-value')
ax3.set_xlabel('N-stars')
ax4.set_xlabel('N-stars')
#fig6.suptitle(r'Two-sample Kolmogorov-Smirnoff: D=%s with $\alpha_{vir}$=%s vs $\alpha_{vir}$=%s'\
#              %(dname[i][11:14], dname[i][15:18], dname[j][15:18]))
fig6.suptitle('Two-sample Kolmogorov-Smirnoff: \n %s vs %s'%(dname[i], dname[j]))

axes = [ax1, ax2, ax3, ax4]

for ax in axes:
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)
    ax.tick_params(which='both', direction='in', top='on', right='on')
    ax.axhline(5, label=('5% significance level'), lw=1.0, c='red')
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.legend(frameon=False, fontsize=8.)
    ax.set_ylim(0., 100.)
    ax.set_xlim(0., 1000.)

plt.show()

#%%

for n in range(nlines):
    dflist[n]['violin'] = ('Simulation %d'%(n+1))

#%% 20 violinplots shwoing each simulation
    
j = 50
velocity = 'PM-velxy'

fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12), \
      (ax13, ax14, ax15, ax16), (ax17, ax18, ax19, ax20)) = plt.subplots(nrows=5, ncols=4, sharey=True, sharex=True)
fig.set_size_inches(10.69, 8.27)
plt.tight_layout()
plt.subplots_adjust(hspace=0.2, wspace=0.16, top=0.92, bottom=0.05, left=0.06)

axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20]

for n in range(nlines):
     
    sns.violinplot(x='violin', y=velocity, data=(dflist[n].loc[j]), inner='box', palette='Greens', ax = axes[n])

for ax, n in zip(axes, range(nlines)):
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xlabel('Simulation %d'%(n+1), fontsize=10.)
    ax.set_yscale('log')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, ['Bound', 'Unbound'], loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.3))
    ax.legend('')
    ax.tick_params(axis='x', bottom=False, labelbottom=False)
    ax.tick_params(axis='y', which='both', direction='in', right=True, labelright=True)

for ax in [ax1, ax5, ax9, ax13, ax17]:
    ax.set_ylabel('Velocity (km/s)', fontsize=10.)

ax4.legend(handles, ['Bound', 'Unbound'], loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.3))
fig.suptitle('%s-velocity distributions of %s simulations with initial conditions: \n %s'\
             %(velocity[0:2],nlines, legend[0]), fontsize=12.)

#%% 20 violinplots showing each simulation split in bound/unbound

j = 50
velocity = 'PM-velxy'

fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12), \
      (ax13, ax14, ax15, ax16), (ax17, ax18, ax19, ax20)) = plt.subplots(nrows=5, ncols=4, sharey=True, sharex=True)
fig.set_size_inches(10.69, 8.27)
plt.tight_layout()
plt.subplots_adjust(hspace=0.2, wspace=0.16, top=0.92, right=0.96, bottom=0.05, left=0.06)

axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20]

for n in range(nlines):
     
    sns.violinplot(x='violin', y=velocity, data=(dflist[n].loc[j]), hue='Unbound', split=True, \
                                                 inner='quartile', scale='count', palette='Greens', ax = axes[n])

for ax, n in zip(axes, range(nlines)):
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xlabel('Simulation %d'%(n+1), fontsize=10.)
    ax.set_yscale('log')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, ['Bound', 'Unbound'], loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.3))
    ax.legend('')
    ax.tick_params(axis='x', bottom=False, labelbottom=False)
    ax.tick_params(axis='y', which='both', direction='in', right=True, labelright=True)

for ax in [ax1, ax5, ax9, ax13, ax17]:
    ax.set_ylabel('Velocity (km/s)', fontsize=10.)

ax4.legend(handles, ['Bound', 'Unbound'], loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.3))
fig.suptitle('%s-velocity distributions at %s Myr with initial conditions: \n %s'\
             %(velocity[0:2], j/10, legend[0]), fontsize=12.)