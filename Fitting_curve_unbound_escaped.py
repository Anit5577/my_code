# this code calculates and plots the cumulative PM and 3D velocity for all snaps in all simulations that are read in from an input text file


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
#import F_COD_Radius_Nstars as CODRN  #turn this on, if COD-correcion is required.
from function_file import read_in_any_datafiles, velocity_elements, energy_stars, stars_in_outside_2HMR

dflist,dname,nlines  = read_in_any_datafiles('file.txt') #this reads in the .dat files from an inputfile list

dflist = energy_stars(dflist,dname,nlines)       #this calculates the energy of each star in each snapshot an simulation and adds this in a column
dflist = velocity_elements(dflist,dname,nlines)  #this calculates the velocity by using the distance travelled between each snapshot and divides it by snapshot length - this is an alternative to the provided velocities from the simulation
dflist = stars_in_outside_2HMR(dflist,dname,nlines)  # this calculates the half-mass radius based on centre of density corrected locations and then adds a column identifying if the stars are inside or outside 2*HMR

# different velocity distributions are calculated, e.g. 3D and PM for the original velocity data velx - velz and the velocities calculated by using the distance travelled between each snapshot. 
#both are expressed in km/s
#%% plots cumulative velocity distribution for unbound stars at 5 Myr as PM-velocity and 3D-velocity

legend =[]

for fname in dname: # to allow the filename of the simulations to dictate the labels
        
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
    

#%% Plots average number of escaped stars for both unbound and escaped calculations


dflistUB = []
dflistESC = []
for n in range(nlines):
    dflistUB.append(dflist[n].loc[dflist[n]['Unbound'] == True])
    dflistESC.append(dflist[n].loc[dflist[n]['escaped'] == True]) #this creates 20 dataframes with the escaped star in each simulation

#%%

var = 1.0
nsnaps = 101

for n in range(nlines): 
    
    dflist[n]['radval']=(np.sqrt(dflist[n]['nradx']**2.+dflist[n]['nrady']**2.+dflist[n]['nradz']**2.))
    hmrad =[]
     
    for ssnap in range(0, nsnaps):  
        dflist_sorted =[]
        halfmass =0.
        cmass=0.
        hmrad=0.
        dflist_sorted = dflist[n].loc[ssnap].sort_values('radval')
        halfmass = (dflist[n].loc[ssnap]['mass'].sum()/2.)
        cmass = (dflist_sorted['mass'].cumsum())
        dflist_sorted['hmdif'] =  np.absolute(cmass.subtract(halfmass))
        hmrad = (dflist_sorted.loc[dflist_sorted['hmdif'].idxmin(),'radval'])
        varhmrad = var*hmrad
        dflist[n].loc[ssnap,'HMRescaped'] = np.where(dflist[n].loc[ssnap,'radval'] >= varhmrad,True,False)


dflistHMRESC = []

for n in range(nlines):
    dflistHMRESC.append(dflist[n].loc[dflist[n]['HMRescaped'] == True])     
    


#%%

nsnaps = 101

average_unbound=[]
average_escaped=[]
average_HMRescaped=[]
#unbound_error=[]
#escaped_error=[]
#HMRescaped_error=[]
for ssnap in range(nsnaps):
    unboundnumb=[]
    escapednumb=[]
    hmrescapednumb=[]
    for n in range(nlines):      
        unboundnumb.append(sum(dflist[n].loc[ssnap,'Unbound']))      
        escapednumb.append(sum(dflist[n].loc[ssnap,'escaped'])) 
        hmrescapednumb.append(sum(dflist[n].loc[ssnap,'HMRescaped'])) 
    average_unbound.append(np.mean(unboundnumb))
    average_escaped.append(np.mean(escapednumb))
    average_HMRescaped.append(np.mean(hmrescapednumb))
#    unbound_error.append((np.std(unboundnumb)/np.sqrt(n)))
#    escaped_error.append((np.std(escapednumb)/np.sqrt(n)))
#    HMRescaped_error.append((np.std(hmrescapednumb))/(np.sqrt(n)))


#%% Scatter plots of energy unbound vs. location unbound stars
fig3 = plt.gca()

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

x = np.arange(0,10.1,0.1)

#plt.errorbar(x,average_unbound,xerr=None, yerr=unbound_error, fmt='-x',markersize=3,elinewidth=0.5,capsize=1.5, label = 'Energetically unbound stars')
#plt.errorbar(x,average_escaped,xerr=None, yerr=escaped_error, label = 'Location-based escaped stars: 2HMR')
#plt.errorbar(x,average_HMRescaped,xerr=None, yerr=HMRescaped_error,fmt='-x',markersize=3,elinewidth=0.5,capsize=1.5, label = 'Location-based escaped stars: %s*HMR' %var)
plt.scatter(x,average_unbound, s=1,label = 'Energetically unbound stars')
plt.scatter(x,average_HMRescaped, s=1, label = 'Stars outside of %s*HMR' %var)
 

fig3.set_title('Average number of unbound/escaped stars from 0-10 Myr: \n %s' %legend[0])
fig3.set_xlabel('Time (Myr)',fontsize=12.) 
fig3.set_ylabel('Average over %s simulations' %nlines,fontsize=12.)   

fig3.legend(loc='upper left',frameon=False)  
fig3.xaxis.set_minor_locator(x_minor_locator)
fig3.yaxis.set_minor_locator(y_minor_locator)
#    i.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))

fig3.set_xlim(left=0.)
fig3.set_ylim(bottom=0.)

plt.show()

