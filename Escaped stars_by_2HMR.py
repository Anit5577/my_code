#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:46:56 2018

@author: php17cs
"""

#this is the original code 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from function_file import read_in_datafiles, stars_outside_2HMR, velocity_elements

dflist,d  = read_in_datafiles('file20.txt')

dname = sorted(d.values())

dflist = stars_outside_2HMR(dflist,dname)


#%% print the count the number of stars outside 2xHMR in a snapshot....

print (dname[5])
print (dflist[5].loc[10]['escaped'].value_counts())

#%%

dflist = velocity_elements(dflist,dname)

for n in range(20):
    dflist[n]['3D-vel'] = (np.sqrt(dflist[n]['velx']**2.+dflist[n]['vely']**2.+dflist[n]['velz']**2.))
    dflist[n]['3D-veldist'] = (np.sqrt(dflist[n]['xvel']**2.+dflist[n]['yvel']**2.+dflist[n]['zvel']**2.))
    dflist[n]['PM-vel'] = (np.sqrt(dflist[n]['velx']**2.+dflist[n]['vely']**2.))
    dflist[n]['PM-veldist'] = (np.sqrt(dflist[n]['xvel']**2.+dflist[n]['yvel']**2.))
    dflist[n].ESC = (dflist[n].loc[dflist[n]['escaped'] == True])  
    
ESClist = [dflist[0].ESC, dflist[1].ESC, dflist[2].ESC, dflist[3].ESC, dflist[4].ESC,dflist[5].ESC,dflist[6].ESC,dflist[7].ESC,dflist[8].ESC,dflist[9].ESC,dflist[10].ESC, \
          dflist[11].ESC, dflist[12].ESC, dflist[13].ESC, dflist[14].ESC, dflist[15].ESC, dflist[16].ESC, dflist[17].ESC, dflist[18].ESC,dflist[19].ESC]
 
ESC = pd.concat(ESClist)


#%% plots umulative velocity distribution for unbound stars at 5 Myr as PM-velocity and 3D-velocity

fnamelist = dname

ax = plt.gca()
x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

legend =[]

for fname in fnamelist: # to allow the filename of the simulations to dictate the labels
        
    if fname[21] == 'E':
       if fname[17] == 'X':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution, N=1000' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution, N=500' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution, N=2000' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, stellar evolution, N=1000')
       elif fname[5:7] == '2r':
           legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, stellar evolution, N=1000')

    if fname[21] == 'S':
       if fname[17] == 'X':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution, N=1000' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution, N=500' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution, N=2000' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, no evolution, N=1000')
       elif fname[5:7] == '2r':
           legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, no evolution, N=1000')
    legend.append(legendtitle)


ax.scatter(ESC.loc[50].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(ESC.loc[50]),1.0,len(ESC.loc[50])) ,s=1, label = 'PM-velocity from distance/snapshot')
#ax.scatter(ESC.loc[50].sort_values('PM-vel')['PM-vel'],np.linspace(1/len(ESC.loc[50]),1.0,len(ESC.loc[50])) ,s=1, label = 'PM-velocity from data')
ax.scatter(ESC.loc[50].sort_values('3D-veldist')['3D-veldist'],np.linspace(1/len(ESC.loc[50]),1.0,len(ESC.loc[50])) ,s=1, label = '3D-velocity from distance/snapshot')
#ax.scatter(ESC.loc[50].sort_values('3D-vel')['3D-vel'],np.linspace(1/len(ESC.loc[50]),1.0,len(ESC.loc[50])) ,s=1, label = '3D-velocity from data')

ax.legend(loc='lower right', frameon=False, title=legend[0])  

ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_xlabel('Velocity (km/s)',fontsize=12.) 
ax.set_ylabel('Cumulative distribution',fontsize=12.)
ax.set_title('Velocity distributions of stars outside 2xHMR at 5 Myr of 20 simulations')
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

plt.show()
