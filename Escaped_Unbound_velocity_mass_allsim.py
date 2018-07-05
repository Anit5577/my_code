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
dflist = stars_in_outside_2HMR(dflist,dname,nlines) # this calculates the half-mass radius based on centre of density corrected locations and then adds a column identifying if the stars are inside or outside 2*HMR


# different velocity distributions are calculated, e.g. 3D and PM for the original velocity data velx - velz and the velocities calculated by using the distance travelled between each snapshot. 
#both are expressed in km/s
#%% this cell produces dataframes for each simulation containing the unbound/escaped stars, 
# this cell also creates dataframes for each simulation containing the high-mass and low-mass unbound and escaped stars.


dflistUB = []
dflistESC = []
dflistHMUB = []
dflistHMESC = []
dflistHMall = []
dflistLMUB = []
dflistLMESC = []
dflistLMall =[]
dflistHMRESC = []

for n in range(nlines):
    dflistUB.append(dflist[n].loc[dflist[n]['Unbound'] == True])
    dflistESC.append(dflist[n].loc[dflist[n]['escaped'] == True]) #this creates 20 dataframes with the escaped star in each simulation
    dflistHMRESC.append(dflist[n].loc[dflist[n]['HMRescaped'] == True])     
    dflistHMUB.append(dflistUB[n].loc[dflistUB[n]['mass'] >= 8.])
    dflistHMESC.append(dflistESC[n].loc[dflistESC[n]['mass'] >= 8.])
    dflistHMall.append(dflist[n].loc[dflist[n]['mass'] >= 8.])
    dflistLMUB.append(dflistUB[n].loc[dflistUB[n]['mass'] < 2.5])
    dflistLMESC.append(dflistESC[n].loc[dflistESC[n]['mass'] < 2.5])
    dflistLMall.append(dflist[n].loc[dflist[n]['mass'] < 2.5])

UB =[]
ESC =[]
HMRESC = []
All =[]
HMall = []
HMUB = []
HMESC = []
LMall = []
LMUB = []
LMESC = []

for n in range(nlines):
    UB.append(dflistUB[n])
    ESC.append(dflistESC[n]) 
    HMRESC.append(dflistESC[n]) 
    All.append(dflist[n])
    HMUB.append(dflistHMUB[n])
    HMESC.append(dflistHMESC[n])    
    HMall.append(dflistHMall[n])
    LMUB.append(dflistLMUB[n])
    LMESC.append(dflistLMESC[n])    
    LMall.append(dflistLMall[n])
       
UB = pd.concat(UB)
ESC = pd.concat(ESC)
All = pd.concat(All)
HMUB = pd.concat(HMUB)
HMESC = pd.concat(HMESC)
HMall = pd.concat(HMall)
LMUB = pd.concat(LMUB)
LMESC = pd.concat(LMESC)
LMall = pd.concat(LMall)
 

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


fig3 = plt.gca()

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

x = np.arange(0,10.1,0.1)

nsnaps = 101

average_unbound=[]
average_escaped=[]
average_HMRescaped=[]
for ssnap in range(nsnaps):
    unboundnumb=[]
    escapednumb=[]
    hmrescapednumb=[]
    for n in range(nlines):      
        unboundnumb.append(sum(dflist[n].loc[ssnap,'Unbound']))      
        escapednumb.append(sum(dflist[n].loc[ssnap,'escaped'])) 
    average_unbound.append(np.mean(unboundnumb))
    average_escaped.append(np.mean(escapednumb))


plt.scatter(x,average_unbound,s=0.5, label = 'Energetically unbound stars')
plt.scatter(x,average_escaped,s=0.5, label = 'Location-based escaped stars')


fig3.set_title('Average number of unbound/escaped stars from 0-10 Myr: \n %s'%legend[0])
fig3.set_xlabel('Time (Myr)',fontsize=12.) 
fig3.set_ylabel('Average over %s simulations' %nlines,fontsize=12.)   

fig3.legend(frameon=False)  
fig3.xaxis.set_minor_locator(x_minor_locator)
fig3.yaxis.set_minor_locator(y_minor_locator)
#    i.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))

fig3.set_xlim(left=0.)
fig3.set_ylim(bottom=0.)

plt.show()


#%% plots histogram of the masses of escaped and unbound stars

fig2 = plt.gca()

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)


plt.hist(ESC.loc[50]['mass'],bins=np.arange(min(ESC.loc[50]['mass']), max(ESC.loc[50]['mass']) + 1, 1),alpha=0.5, label = 'Location-based escaped stars')
plt.hist(UB.loc[50]['mass'],bins=np.arange(min(UB.loc[50]['mass']), max(UB.loc[50]['mass']) + 1, 1),alpha=0.5, label = 'Energetically unbound stars')

fig2.set_title('Histogram of masses of unbound/escaped stars at 5 Myr - %s simulations' %nlines)
fig2.set_xlabel('Mass (in solar mass)',fontsize=12.) 

fig2.legend(loc='upper right', frameon=False, title=legend[0])  
fig2.xaxis.set_minor_locator(x_minor_locator)
fig2.yaxis.set_minor_locator(y_minor_locator)

fig2.set_xlim(left=0.)

plt.show()

#%% plots 3D-velocity against mass for unbound and escaped stars.

fig4 = plt.gca()

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)


plt.scatter(ESC.loc[50]['3D-veldist'],ESC.loc[50]['mass'], s=1, label = 'Location-based escaped stars')
plt.scatter(UB.loc[50]['3D-veldist'],UB.loc[50]['mass'],s=1,alpha=0.5,label = 'Energetically unbound stars')

fig4.set_title('3D-velocity and masses of unbound/escaped stars at 5 Myr - %s simulations' %nlines)
fig4.set_ylabel('Mass (in solar mass)',fontsize=12.) 
fig4.set_xlabel('3D-velocity (in km/s)',fontsize=12.) 

fig4.legend(loc='upper right', frameon=False, title=legend[0])  
fig4.xaxis.set_minor_locator(x_minor_locator)
fig4.yaxis.set_minor_locator(y_minor_locator)

fig4.set_xlim(left=0.)
fig4.set_ylim(bottom=0.)

plt.show()

#%% Calculates the unbound and escaped mass fractions for high-mass (above 8 solarmass) and low-mass (below 2.5 solar mass)


totalUBfraction = (UB.loc[50].index.size)/(All.loc[50].index.size)
totalESCfraction = (ESC.loc[50].index.size)/(All.loc[50].index.size)

HMUBfraction = (HMUB.loc[50].index.size)/(HMall.loc[50].index.size)
HMESCfraction = (HMESC.loc[50].index.size)/(HMall.loc[50].index.size)
LMUBfraction = (LMUB.loc[50].index.size)/(LMall.loc[50].index.size) 
LMESCfraction = (LMESC.loc[50].index.size)/(LMall.loc[50].index.size) 

print ('Total unbound: %.5f' %totalUBfraction)
print ('Total escaped: %.5f' %totalESCfraction) 
print ('High-mass unbound: %.5f' %HMUBfraction)
print ('High-mass escaped: %.5f' %HMESCfraction)   
print ('Low-mass unbound: %.5f' %LMUBfraction)
print ('Low-mass escaped: %.5f' %LMESCfraction)


#%%

fig4 = plt.gca()

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)


plt.scatter(HMESC.loc[50]['3D-veldist'],HMESC.loc[50]['mass'], marker='+', label = 'Location-based escaped stars')
plt.scatter(HMUB.loc[50]['3D-veldist'],HMUB.loc[50]['mass'],marker='x',alpha=0.5,label = 'Energetically unbound stars')

fig4.set_title('3D-velocity and masses of high-mass unbound/escaped stars at 5 Myr - %s simulations' %nlines)
fig4.set_ylabel('Mass (in solar mass)',fontsize=12.) 
fig4.set_xlabel('3D-velocity (in km/s)',fontsize=12.) 

fig4.legend(loc='lower right', frameon=False, title=legend[0])  
fig4.xaxis.set_minor_locator(x_minor_locator)
fig4.yaxis.set_minor_locator(y_minor_locator)

fig4.set_xlim(left=0.)
fig4.set_ylim(bottom=0.)

plt.show()


