#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu May 17 13:40:00 2018

@author: php17cs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FormatStrFormatter
#from matplotlib.ticker import PercentFormatter
import seaborn as sns
import matplotlib.ticker as ticker

#%% reading in all files with 20 simulations All_read

from function_file import read_in_summary_datafiles

All_read, fname, nlines = read_in_summary_datafiles('file20.txt')

#%% plots unbound stars cumulative velocity distributions for a defined time n

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

fig, ax1 = plt.subplots()
#plt.tight_layout()
fig.set_size_inches(10., 10.)
#plt.subplots_adjust(top=0.9,bottom=0.09,left=0.06, right=0.965, hspace=0.3, wspace=0.55)

#fig.patch.set_facecolor('#002342')

#
#fig1, (ax3, ax4) = plt.subplots(nrows=1, ncols=2, sharex=True)
#fig1.set_size_inches(6.27, 14.69)
#plt.subplots_adjust(hspace=0.3, top=0.9, left=0.09, bottom=0.06)

#all_init_1_6 = [0, 1, 2, 3, 4]
#all_init_3_0 = [5, 6, 7, 8, 9]

violin_label = ['Clumpy, virial cluster', 'Smooth, subvirial cluster']
                        
all_init_1_6 = [0, 1]

n = 100      #snapshot number
velocity = 'PM-velxy'  #which velocity to plot

for i in range(2):

        ax1.scatter((All_read[i].loc[n][(All_read[i].loc[n, 'Unbound'] == True) & (All_read[i].loc[n, 'PM-velxy'] >=2.5)]).sort_values(velocity)[velocity], \
                     np.linspace(1/len(All_read[i].loc[n][(All_read[i].loc[n, 'Unbound'] == True) & (All_read[i].loc[n, 'PM-velxy'] >=2.5)]), \
                                       1.0, len(All_read[i].loc[n][(All_read[i].loc[n, 'Unbound'] == True) & (All_read[i].loc[n, 'PM-velxy'] >=2.5)])), \
                                       s=7.,label=violin_label[i]) 

#    ax1.scatter((All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == True) All_read[i].loc[n, 'PM-velxy'] >=2.5)]).sort_values(velocity)[velocity], \
#                 np.linspace(1/len(All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == True) All_read[i].loc[n, 'PM-velxy'] >=2.5)]), \
#                                   1.0, len(All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == True) All_read[i].loc[n, 'PM-velxy'] >=2.5)])), \
#                                   s=0.5, label=(r'$\alpha_{vir}=%s, N_{ub}$=%s'\
#                                                %(fname[i][15:18], \
#                                                  (len(All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == True) All_read[i].loc[n, 'PM-velxy'] >=2.5)])))))
#

#    ax2.scatter((All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == False]).sort_values(velocity)[velocity], \
#                 np.linspace(1/len(All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == False]), \
#                                   1.0, len(All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == False])), \
#                                   s=0.5, label=r'$alpha_{vir}=%s, N_{b}$=%s'\
#                                                %(fname[i][15:18], \
#                                                  (len(All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == False]))))

#        ax3.scatter((All_read[j].loc[n][All_read[j].loc[n, 'Unbound'] == True]).sort_values(velocity)[velocity], \
#                     np.linspace(1/len(All_read[j].loc[n][All_read[j].loc[n, 'Unbound'] == True]), \
#                                       1.0, len(All_read[j].loc[n][All_read[j].loc[n, 'Unbound'] == True])), \
#                                       s=3., label=violin_label[i])

#    ax4.scatter((All_read[j].loc[n][All_read[j].loc[n, 'Unbound'] == False]).sort_values(velocity)[velocity], \
#                 np.linspace(1/len(All_read[j].loc[n][All_read[j].loc[n, 'Unbound'] == False]), \
#                                   1.0, len(All_read[j].loc[n][All_read[j].loc[n, 'Unbound'] == False])), \
#                                   s=0.5, label=r'$alpha_{vir}=%s, N_{b}$=%s'\
#                                                %(fname[j][15:18], \
#                                                  (len(All_read[j].loc[n][All_read[j].loc[n, 'Unbound'] == False]))))


for ax in [ax1]:
#    ax.set_facecolor('#002342')
    plt.setp(ax.spines.values(), linewidth=4)
#    ax.set_facecolor('#002342')
#    
#    ax.spines['bottom'].set_color('white')
#    ax.spines['top'].set_color('white')
#    ax.spines['left'].set_color('white')
#    ax.spines['right'].set_color('white')
#    ax.xaxis.label.set_color('white')
#    ax.yaxis.label.set_color('white')
#    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
#    
#    ax.tick_params(which='both', direction='in', length=5., width=1., colors='white', \
#                   labelsize=12.)
#
#    ax.xaxis.set_minor_locator(x_minor_locator)
#    ax.yaxis.set_minor_locator(y_minor_locator)
#    ax.tick_params(which='both', direction='in', top=True, right=True, labelbottom=True)
    ax.set_xlabel('Proper motion (km/s)', fontsize=16.)
    ax.set_ylabel('Cumulative distribution', fontsize=16.)
#    leg = ax.legend(loc='upper left', frameon=False, fontsize=14.)
#    for text in leg.get_texts():
#        text.set_color('white')
# #  ax.set_xlim(0.1, 10)
    ax.set_ylim(0., 1.03)
    ax.set_xscale('log')
#    
#i='new_1000_no limit'  
#plt.savefig('Cumvelplot_%s.png'%i, facecolor='#002342')
    ax.spines['bottom'].set_color('#002342')
    ax.spines['top'].set_color('#002342')
    ax.spines['left'].set_color('#002342')
    ax.spines['right'].set_color('#002342')
    ax.xaxis.label.set_color('#002342')
    ax.yaxis.label.set_color('#002342')

    ax.tick_params(which='both', direction='in', length=8., width=3., labelsize=12.)

    leg = ax.legend(loc='bottom right', frameon=False, fontsize=16.)    

    for text in leg.get_texts():
        text.set_color('#002342')
    
#    plt.savefig('Unbound_%s.png' %i, transparent=True, dpi=300 )            
            
    

#ax1.set_title('D=%s' %fname[all_init_1_6[0]][11:14], fontsize=12., color='white')
#ax2.set_title('D=%s' %fname[all_init_1_6[0]][11:14], fontsize=10.)
#ax3.set_title('D=%s' %fname[all_init_3_0[0]][11:14], fontsize=12., color='white')
#ax4.set_title('D=%s' %fname[all_init_3_0[0]][11:14], fontsize=10.)
#
#fig.suptitle('Cumulative %s-velocity distributions for unbound stars at %s Myr'\
#             %(velocity[0:2], np.round(All_read[all_init_1_6[0]].loc[n].iloc[1]['time'],\
#               decimals=2)), fontsize=12.)

#fig1.suptitle('Cumulative %s-velocity distributions for bound/unbound stars at %s Myr'\
#             %(velocity[0:2], np.round(All_read[all_init_3_0[0]].loc[n].iloc[1]['time'],\
#               decimals=2)), fontsize=12.)

plt.show()
plt.savefig('Cumulative_1.png', transparent=True, dpi=300 )

#%% plots cumulative distributions 1 defined set of initia conditions at 4 different times

fig4, ax = plt.subplots()

velocity = 'PM-velxy'          # add column name of velocity to plot
j = 0

ax.scatter((All_read[j].loc[1][All_read[j].loc[1, 'Unbound'] == True]).sort_values\
            (velocity)[velocity], np.linspace(1/len(All_read[j].loc[1][All_read[j].loc\
            [1, 'Unbound'] == True]), 1.0, len(All_read[j].loc[1][All_read[j].loc[1, \
            'Unbound'] == True])), s=0.5, label=('0.1 Myr'))
ax.scatter((All_read[j].loc[10][All_read[j].loc[10, 'Unbound'] == True]).sort_values\
            (velocity)[velocity], np.linspace(1/len(All_read[j].loc[10][All_read[j].loc\
            [10, 'Unbound'] == True]), 1.0, len(All_read[j].loc[10][All_read[j].loc[10, \
            'Unbound'] == True])), s=0.5, label=('1 Myr'))
ax.scatter((All_read[j].loc[50][All_read[j].loc[50, 'Unbound'] == True]).sort_values\
            (velocity)[velocity], np.linspace(1/len(All_read[j].loc[50][All_read[j].loc\
            [50, 'Unbound'] == True]), 1.0, len(All_read[j].loc[50][All_read[j].loc[50, \
            'Unbound'] == True])), s=0.5, label=('5 Myr'))
ax.scatter((All_read[j].loc[100][All_read[j].loc[100, 'Unbound'] == True]).sort_values\
            (velocity)[velocity], np.linspace(1/len(All_read[j].loc[100][All_read[j].loc\
            [100, 'Unbound'] == True]), 1.0, len(All_read[j].loc[100][All_read[j].loc[100, \
            'Unbound'] == True])), s=0.5, label=('10 Myr'))

ax.set_title('Cumulative PM-velocity for unbound stars at different times: \n D=%s, $alpha_{vir}=%s$'\
             %(fname[j][11:14], fname[j][15:18]), fontsize=12.)

ax.set_xlabel('Velocity (km/s)', fontsize=10.)
ax.set_ylabel('Cumulative distribution', fontsize=10.)
ax.legend(loc='lower right', frameon=False)
#ax.set_xlim(0.)
ax.set_ylim(0., 1.03)
ax.set_xscale('log')

plt.show()



#%% violin plots for all initial conditions in one plot at to be defined snapshots

#fig6, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
#plt.subplots_adjust(wspace=0.01)
#
#velocity = 'PM-velxy'
#time = (50) # define the snapshot needed to display
#age = time/10
#
#i = [0, 1, 2, 3, 4] #defines the datasets to display D=1.6
##i = [5,6,7,8,9] #defines the datasets to display D=3.0
#
#plot2_data = [(All_read[i[0]].loc[time][All_read[i[0]].loc[time, 'Unbound'] == True])[velocity],\
#              (All_read[i[1]].loc[time][All_read[i[1]].loc[time, 'Unbound'] == True])[velocity],\
#              (All_read[i[2]].loc[time][All_read[i[2]].loc[time, 'Unbound'] == True])[velocity],\
#              (All_read[i[3]].loc[time][All_read[i[3]].loc[time, 'Unbound'] == True])[velocity],\
#              (All_read[i[4]].loc[time][All_read[i[4]].loc[time, 'Unbound'] == True])[velocity]]
#
#
#plot1_data = [All_read[i[0]].loc[time][velocity], All_read[i[1]].loc[time][velocity],\
#              All_read[i[2]].loc[time][velocity], All_read[i[3]].loc[time][velocity],\
#              All_read[i[4]].loc[time][velocity]]
#
#plot_label = [r'$\alpha_{vir}$=%s'%fname[i[0]][15:18], r'$\alpha_{vir}$=%s'%fname[i[1]][15:18], \
#              r'$\alpha_{vir}$=%s'%fname[i[2]][15:18], r'$\alpha_{vir}$=%s'%fname[i[3]][15:18], \
#              r'$\alpha_{vir}$=%s'%fname[i[4]][15:18]]
#
#a = ax1.violinplot(plot1_data, showmeans=True, showmedians=True, showextrema=False)
#b = ax2.violinplot(plot2_data, showmeans=True, showmedians=True, showextrema=False)
#
#a['cmeans'].set_color('seagreen')
#b['cmeans'].set_color('seagreen')
#
##a=ax1.violinplot(plot1_data, showmeans=True, showmedians=False, showextrema=False)
##b=ax2.violinplot(plot2_data, showmeans=True, showmedians=False, showextrema=False)
#
#pos = np.arange(len(plot_label))
#
#for ax in [ax1, ax2]:
#    ax.get_xaxis().set_tick_params(direction='in')
#    ax.get_yaxis().set_tick_params(direction='in', right='on')
#    ax.set_xticks(pos+1)
#    ax.set_yscale('log')
#    ax.set_xticklabels(plot_label)
#
#ax1.set_xlabel('All stars', fontsize=12.)
#ax2.set_xlabel('Unbound', fontsize=12.)
#ax1.set_ylabel('%s-velocity (km/s)'%velocity[0:2], fontsize=12.)
#ax2.get_yaxis().set_tick_params(labelright=True)
#fig6.suptitle('%s-velocity distributions for all stars vs. unbound stars at %s Myr with D=%s'\
#              %(velocity[0:2], age, fname[i[0]][11:14]))
#
#
#plt.show()

#%% violin plots for a set of initial conditions showing 4 different snapshots together of all stars vs unbound
#
#fig6, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
#plt.subplots_adjust(wspace=0.01)
#
#velocity = 'PM-velxy'
#i = (8) # define dataset to plot
#
#plot2_data = [(All_read[i].loc[1][All_read[i].loc[1, 'Unbound'] == True])[velocity],\
#              (All_read[i].loc[10][All_read[i].loc[10, 'Unbound'] == True])[velocity],\
#              (All_read[i].loc[50][All_read[i].loc[50, 'Unbound'] == True])[velocity],\
#              (All_read[i].loc[100][All_read[i].loc[100, 'Unbound'] == True])[velocity]]
#
#plot1_data = [All_read[i].loc[1][velocity], All_read[i].loc[10][velocity],\
#              All_read[i].loc[50][velocity], All_read[i].loc[100][velocity]]
#
#plot_label = ['0.1 Myr', '1 Myr', '5 Myr', '10 Myr']
#
#
#ax1.violinplot(plot1_data, showmeans=True, showmedians=False, showextrema=False)
#ax2.violinplot(plot2_data, showmeans=True, showmedians=False, showextrema=False)
#
#pos = np.arange(len(plot_label))
#
#for ax in [ax1, ax2]:
#    ax.get_xaxis().set_tick_params(direction='in')
#    ax.get_yaxis().set_tick_params(direction='in', right='on')
#    ax.set_xticks(pos+1)
#    ax.set_ylim(-1., 10.) # axis limit set to allow focus on the shape of the distribution,
#    ax.set_xticklabels(plot_label)
#
#ax1.set_xlabel(r'D=%s, $\alpha_{vir}$=%s'%(fname[i][11:14], fname[i][15:18]))
#ax2.set_xlabel(r'D=%s, $\alpha_{vir}$=%s'%(fname[i][11:14], fname[i][15:18]))
#ax1.set_ylabel('%s-velocity (km/s)'%velocity[0:2])
#ax2.get_yaxis().set_tick_params(labelright=True)
#
#fig6.suptitle('%s-velocity distributions at different cluster ages all stars vs unbound'%velocity[0:2])
#ax1.set_title('All stars')
#ax2.set_title('Unbound')
#
#plt.show()

#%% creates additional columns in All-read
#-containing the initial conditions for each dataset
#-mass classification


for n in [0, 1]:
    All_read[n]['violin'] = ('%s'%violin_label[n])
    
#for n in [2, 3]:
#    All_read[n]['violin'] = ('%s'%violin_label[n-3])    

for n in range(nlines):
#    All_read[n]['violin'] = (r'D=%s, $\alpha_{vir}$=%s'%(\
#                      fname[n][11:14], fname[n][15:18]))
    All_read[n]['mass-class'] = np.where(All_read[n]['mass'] >= 8., 'high-mass', 'low-mass')
    All_read[n]['PM-Runaway'] = np.where(All_read[n]['PM-velxy'] >= 30, True, False)
    All_read[n]['3D-Runaway'] = np.where(All_read[n]['3D-velxyz'] >= 30, True, False)




#%% combining all data into one set for violinplots

#init_together = pd.concat(All_read)

init_1_6 = pd.concat((All_read[0], All_read[1]))
#init_3_0 = pd.concat((All_read[2], All_read[3]))


#%%

fig, ax = plt.subplots()
fig.set_size_inches(8, 8)
#plt.subplots_adjust(top=0.925, bottom=0.11, left=0.115, right=0.93,)


plt.setp(ax.spines.values(), linewidth=4)

ax.spines['bottom'].set_color('#002342')
ax.spines['top'].set_color('#002342')
ax.spines['left'].set_color('#002342')
ax.spines['right'].set_color('#002342')
ax.xaxis.label.set_color('#002342')
ax.yaxis.label.set_color('#002342')

velocity = 'PM-velxy'
#plotdata = init_together
plotdata = init_1_6
#plotdata = init_3_0

j = 100



#sns.violinplot(x='violin', y=velocity, data=(plotdata.loc[j][(plotdata.loc[j,'Unbound']==True) & (plotdata.loc[j,'PM-velxy']>=2.5)]), bw=0.2, \
#                                            inner='quartile', scale='count', ax=ax, width=0.8, linewidth=1., palette='Greens')

#sns.violinplot(x='violin', y=velocity, data=(plotdata.loc[j]), split=True, hue='Unbound', cut=0., bw=0.1,\
#                                          inner='quartile', scale='count', palette='RdPu', ax=ax(plotdata.loc[j,'Unbound']==True), width=0.8, linewidth=2.)


sns.violinplot(x='violin', y=velocity, data=(plotdata.loc[j][(plotdata.loc[j,'Unbound']==True) & (plotdata.loc[j,'PM-velxy']>=2.5)]), \
               hue='mass-class',  bw=0.2, \
               hue_order=['low-mass', 'high-mass'], split=True, inner='quartile', scale='width', \
               palette={'low-mass':'darkred', 'high-mass':'goldenrod'}, ax=ax, width=0.8, linewidth=2.)


ax.set_xlabel('')
ax.set_ylabel('Proper motion (km/s)', fontsize=16.)
ax.set_yscale('log')
ax.set_ylim(top=100.)

handles, labels = ax.get_legend_handles_labels()
ax.legend('')
ax.tick_params(axis='x', bottom=False)
ax.tick_params(axis='y', which='both', direction='in', right=True)

ax.tick_params(which='both', direction='in', length=8., width=3., colors='#002342', \
                  labelsize=16.)
#leg = ax.legend(handles, ['Bound', 'Unbound'], loc='upper center', frameon=False, ncol=2, fontsize=12.)
leg = ax.legend(handles, ['Low-mass', 'High-mass'], loc='upper center', frameon=False, ncol=2, fontsize=14.)

for text in leg.get_texts():
    text.set_color('#002342')


i='Poster_unbound_mass'

plt.savefig('Violinplots_%s.png'%i, transparent=True, dpi=600)

plt.show()


#%% violinplots separated into bound and unbound stars showing their Proper Motion at 4 different times

sns.set_style('ticks')
fig7, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, sharex=True, sharey=True)
fig7.set_size_inches(11.69, 8.27)

plt.subplots_adjust(top=0.89, bottom=0.085, left=0.06, right=0.96, hspace=0.05)

velocity = 'PM-velxy'
#plotdata = init_together
#plotdata = init_1_6
plotdata = init_3_0

j = [0, 10, 50, 100]

sns.violinplot(x='violin', y=velocity, data=(plotdata.loc[j[0]]), hue='Unbound', split=True, \
                                             inner='quartile', scale='count', palette='Greens', ax=ax1)
sns.violinplot(x='violin', y=velocity, data=(plotdata.loc[j[1]]), hue='Unbound', split=True, \
                                             inner='quartile', scale='count', palette='Greens', ax=ax2)
sns.violinplot(x='violin', y=velocity, data=(plotdata.loc[j[2]]), hue='Unbound', split=True, \
                                             inner='quartile', scale='count', palette='Greens', ax=ax3)
sns.violinplot(x='violin', y=velocity, data=(plotdata.loc[j[3]]), hue='Unbound', split=True, \
                                             inner='quartile', scale='count', palette='Greens', ax=ax4)

for ax in [ax1, ax2, ax3, ax4]:
    ax.set_xlabel('')
    ax.set_ylabel('Proper motion (km/s)')
 #   ax.set_yscale('log')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend('')
    ax.tick_params(axis='x', bottom=False)
    ax.tick_params(axis='y', which='both', direction='in', right=True)
    ax.axvline(x=(nlines-1)/2, color='black')

ymax = np.max(plotdata.loc[100][velocity])

ax1.tick_params(axis='x', top=True, labeltop=True, labelrotation=10)
ax4.tick_params(axis='x', bottom=True, labelbottom=True, labelrotation=10)
ax1.legend(handles, ['Bound', 'Unbound'], loc='upper center', frameon=False, ncol=2, bbox_to_anchor=(0.5, 1.7))
ax1.annotate('%d Myr'%(j[0]/10), xy=(4.25, ymax), xycoords='data',verticalalignment='top')
ax2.annotate('%d Myr'%(j[1]/10), xy=(4.25, ymax), xycoords='data',verticalalignment='top')
ax3.annotate('%d Myr'%(j[2]/10), xy=(4.25, ymax), xycoords='data',verticalalignment='top')
ax4.annotate('%d Myr'%(j[3]/10), xy=(4.25, ymax), xycoords='data',verticalalignment='top')

plt.show()


#%%

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=False, sharey=True)
fig.set_size_inches(8.27, 6.69)
plt.tight_layout()
plt.subplots_adjust(top=0.89, bottom=0.085, left=0.1, right=0.96, hspace=0.05)


#plotdata_UB = init_together.loc[init_together['Unbound'] == True]
plotdata_UB = init_1_6_1000.loc[init_1_6_1000['Unbound'] == True]
plotdata1_UB = init_1_6_2000.loc[init_1_6_2000['Unbound'] == True]
#plotdata_UB = init_3_0.loc[init_3_0['Unbound'] == True]

velocity = 'PM-velxy'
#velocity = '3D-velxyz'

j = [100]

#order = [r'D=1.6, $\alpha_{vir}$=0.1', r'D=1.6, $\alpha_{vir}$=0.3', r'D=1.6, $\alpha_{vir}$=0.5', \
#             r'D=1.6, $\alpha_{vir}$=1.0', r'D=1.6, $\alpha_{vir}$=1.5']

#order = [r'D=3.0, $\alpha_{vir}$=0.1', r'D=3.0, $\alpha_{vir}$=0.3', r'D=3.0, $\alpha_{vir}$=0.5', \
#             r'D=3.0, $\alpha_{vir}$=1.0', r'D=3.0, $\alpha_{vir}$=1.5']

sns.violinplot(x='violin', y=velocity, data=(plotdata_UB.loc[100]), hue='mass-class', \
                                             hue_order=['low-mass', 'high-mass'], split=True, inner='quartile', \
                                             scale_hue=True, scale='width', palette='Blues', ax=ax1)

sns.violinplot(x='violin', y=velocity, data=(plotdata1_UB.loc[100]), hue='mass-class', \
                                             hue_order=['low-mass', 'high-mass'], split=True, inner='quartile', \
                                             scale_hue=True, scale='width', palette='Blues', ax=ax2)


for ax in [ax1, ax2]:
    ax.set_xlabel('')
    ax.set_ylabel('Proper motion [km/s]')
    ax.set_yscale('log')
    ax.set_ylim(0.1, 100)
    ax.legend('')
    ax.tick_params(axis='y', which='both', direction='in', right=True, labelright=False)
    ax.tick_params(axis='x', bottom=True, labelbottom=True, labelrotation=0.)

ymax = np.max(plotdata_UB.loc[100][velocity])

#fig.suptitle('%s-Velocity of unbound stars of different masses at different initial conditions and times'%velocity[0:2])
ax1.tick_params(axis='x', top=False, labeltop=False, labelrotation=0.)
ax2.tick_params(axis='x', bottom=True, labelbottom=True, labelrotation=0.)
ax1.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.5))


plt.show()


#%% Unbound stars with runaway PM-velocities over time

#fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=False, sharey=False)

fig, ax1 = plt.subplots()
#fig, ax2 = plt.subplots()
#fig, ax3 = plt.subplots()

fig.set_size_inches(8., 8.)
#plt.subplots_adjust(top=0.80, hspace=0.3)

clist = ['seagreen', 'steelblue'] 

velocity='PM-velxy'

ymax= []

for n in [0,1]:
    plotdata_PM_RS = All_read[n].loc[(All_read[n]['Unbound'] == True) &  (All_read[n][velocity] >= 10.)]
    ymax.append(np.max(All_read[n]['mass']))
    if not plotdata_PM_RS.empty:
#        ax1.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=1.0, label=(r'D=%s, $alpha_{vir}$=%s, $N_{sim}$=%s'%(\
#                      fname[n][11:14], fname[n][15:18], fname[n][25:29])))
#        ax2.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=1.0, label=(r'D=%s, $alpha_{vir}$=%s, $N_{sim}$=%s'%(\
#                      fname[n][11:14], fname[n][15:18], fname[n][25:29])))
#        ax3.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=1.0, label=(r'D=%s, $alpha_{vir}$=%s, $N_{sim}$=%s'%(\
#                      fname[n][11:14], fname[n][15:18], fname[n][25:29])))

        ax1.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=7.0, c=clist[n], label='%s'%violin_label[n])
#        ax2.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=2.0, label='Substructured, %s'%violin_label[n])
#        ax3.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=2.0, label='Substructured, %s'%violin_label[n])
#
#for n in [3,4,5]:
#    plotdata_PM_RS = All_read[n].loc[(All_read[n]['Unbound'] == True) &  (All_read[n][velocity] >= 13.)]
#    ymax.append(np.max(All_read[n]['mass']))
#    if not plotdata_PM_RS.empty:
#        ax1.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=1.0, label=(r'D=%s, $alpha_{vir}$=%s, $N_{sim}$=%s'%(\
#                      fname[n][11:14], fname[n][15:18], fname[n][25:29])))
#        ax2.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=1.0, label=(r'D=%s, $alpha_{vir}$=%s, $N_{sim}$=%s'%(\
#                      fname[n][11:14], fname[n][15:18], fname[n][25:29])))
#        ax3.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=1.0, label=(r'D=%s, $alpha_{vir}$=%s, $N_{sim}$=%s'%(\
#                      fname[n][11:14], fname[n][15:18], fname[n][25:29])))
#
#        ax1.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=1.0, label='Smooth, %s'%violin_label[n-3])
#        ax2.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=1.0, label='Smooth, %s'%violin_label[n-3])
#        ax3.scatter(plotdata_PM_RS['time'], plotdata_PM_RS['mass'], s=2.0, label='Smooth, %s'%violin_label[n-3])



#ax2.set_ylim(2.5, 8.0)
#ax1.set_ylim(7.9, np.max(ymax))

for ax in [ax1]:
#    fig.patch.set_facecolor('#002342')
    plt.setp(ax.spines.values(), linewidth=4)   
#    ax.set_facecolor('#002342')

    ax.spines['bottom'].set_color('#002342')
    ax.spines['top'].set_color('#002342')
    ax.spines['left'].set_color('#002342')
    ax.spines['right'].set_color('#002342')
    ax.xaxis.label.set_color('#002342')
    ax.yaxis.label.set_color('#002342')
    
#    ax.tick_params(axis='y', which='both', direction='in', labelsize=12., colors='#002342',)
                   
    ax.tick_params(which='both', direction='in', length=8., width=3., colors='#002342', \
                  labelsize=16.)               
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.xaxis.set_ticks(np.arange(0., 10.1, 1.))
    ax1.set_ylim(0., 2.0)
    ax1.set_xlim(0, 10.1)
#    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
#    ax.yaxis.set_minor_locator(AutoMajorLocator(2))
    ax.set_ylabel('Mass (M$_\odot$)', color='#002342', fontsize=16.)
#    ax.tick_params(axis='x', which='both', direction='in', labelsize=12., colors='#002342')
    ax.set_xlabel('Cluster age (Myr)',  fontsize=16., color='#002342')
    leg = ax.legend(loc='upper center', frameon=False, ncol=2, bbox_to_anchor=(0.5, 1.1), fontsize=16.)
    for text in leg.get_texts():
        text.set_color('#002342')

#handles, labels = ax1.get_legend_handles_labels()
#ax1.legend('')
#leg = ax1.legend(handles, ['Substructured, %s'%violin_label[0]], loc='upper center', bbox_to_anchor=(0.5, 1.1), frameon=False, fontsize=10.)
#for text in leg.get_texts():
#    text.set_color('white')
#    
#fig.suptitle('Masses of runaway stars)

plt.show()

i='WS_HM'

plt.savefig('Scatter%s.png'%i, transparent=True, dpi=600)

#%% Unbound stars with runaway space-velocities over time

fig, ax = plt.subplots()

for n in range(nlines):
    plotdata_RS = All_read[n].loc[(All_read[n]['3D-Runaway'] == True) & (All_read[n]['Unbound'] == True)]
    if not plotdata_RS.empty:
        ax.scatter(plotdata_RS['time'], plotdata_RS['mass'], s=2.0, label=r'D=%s, $\alpha_{vir}$=%s'%(fname[n][11:14], fname[n][15:18]))

ax.set_xlabel('Cluster age [Myr]')
ax.set_ylabel('Mass [M$_\odot$]')
ax.tick_params(axis='x', which='both', direction='in', labelsize=10.)
ax.tick_params(axis='y', which='both', direction='in', right=True, labelsize=10.)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax.xaxis.set_ticks(np.arange(0., 11., 1.))
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))
ax.legend(loc='upper center', frameon=False,bbox_to_anchor=(0.5, 1.07), ncol=n, fontsize=8.)

ax.set_ylim(0.)
    
fig.suptitle('Masses of runaway stars (3D-velocity >= 30km/s) at different cluster ages')

plt.show()

#%%



fig, ax = plt.subplots()

for n in range(nlines):
    plotdata_RS = All_read[n].loc[(All_read[n]['3D-Runaway'] == True) & (All_read[n]['Unbound'] == True)]
    if not plotdata_RS.empty:
        ax.scatter(plotdata_RS['time'], plotdata_RS['mass'], s=2.0, label=r'D=%s, $\alpha_{vir}$=%s'%(fname[n][11:14], fname[n][15:18]))

ax.set_xlabel('Cluster age [Myr]')
ax.set_ylabel('Mass [M$_\odot$]')
ax.tick_params(axis='x', which='both', direction='in', labelsize=10.)
ax.tick_params(axis='y', which='both', direction='in', right=True, labelsize=10.)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax.xaxis.set_ticks(np.arange(0., 11., 1.))
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))
ax.legend(loc='upper center', frameon=False,bbox_to_anchor=(0.5, 1.07), ncol=n, fontsize=8.)

ax.set_ylim(0.)
    
fig.suptitle('Masses of runaway stars (3D-velocity >= 30km/s) at different cluster ages')

plt.show()

#%%

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=False)
fig.set_size_inches(7.27, 9.69)
plt.subplots_adjust(top=0.90, hspace=0.1)

#All_read[n]['PM-Walkaway'] = np.where((All_read[n]['PM-velxy'] >= 5) & (All_read[n]['PM-velxy'] < 30), True, False)
#All_read[n]['3D-Walkaway'] = np.where((All_read[n]['3D-velxyz'] >= 5)& (All_read[n]['3D-velxyz'] < 30), True, False)    

ymax= []

for n in range(nlines):
    plotdata_PM_WS = All_read[n].loc[(All_read[n]['Unbound'] == True) &  (All_read[n]['PM-velxy'] >= 5.) & (All_read[n]['PM-velxy'] < 30.)]
    if not plotdata_PM_WS.empty:
        ax1.scatter(plotdata_PM_WS['time'], plotdata_PM_WS['mass'], s=1.0, label=r'D=%s, $\alpha_{vir}$=%s'%(fname[n][11:14], fname[n][15:18]))
        ax2.scatter(plotdata_PM_WS['time'], plotdata_PM_WS['mass'], s=1.0)
        ax3.scatter(plotdata_PM_WS['time'], plotdata_PM_WS['mass'], s=1.0)
    ymax.append(np.max(All_read[n]['mass']))

ax3.set_xlabel('Cluster age [Myr]')
ax3.tick_params(axis='x', which='both', direction='in', labelsize=10.)
ax1.legend(loc='upper center', frameon=False,bbox_to_anchor=(0.5, 1.2), ncol=5, fontsize=8.)

ax3.set_ylim(0., 2.5)
ax2.set_ylim(2.5, 8.0)
ax1.set_ylim(7.9, np.max(ymax))

for ax in [ax1, ax2, ax3]:    
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)
    
    ax.tick_params(axis='y', which='both', direction='in', right=True, labelsize=10.)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.xaxis.set_ticks(np.arange(0., 11., 1.))
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax.set_ylabel('Mass [M$_\odot$]')
    ax.set_xlim(0., 5.)

    
fig.suptitle('Masses of walkaway stars at different cluster ages')

plt.show()

#%%

j=50

for n in range(nlines):
    fig, ax = plt.subplots()
    sns.violinplot(dflist[n].loc[j, 'PM-velxy'][dflist[n].loc[j,'Unbound']==True], cut=0., bw=0.1, \
                                            scale='count', ax=ax, width=0.8, linewidth=1.)
    
    
    
    plt.show()