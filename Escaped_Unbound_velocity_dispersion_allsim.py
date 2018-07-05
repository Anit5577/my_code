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

for n in range(nlines):
    dflistUB.append(dflist[n].loc[dflist[n]['Unbound'] == True])
    dflistESC.append(dflist[n].loc[dflist[n]['escaped'] == True]) #this creates 20 dataframes with the escaped star in each simulation
    
    dflistHMUB.append(dflistUB[n].loc[dflistUB[n]['mass'] >= 8.])
    dflistHMESC.append(dflistESC[n].loc[dflistESC[n]['mass'] >= 8.])
    dflistHMall.append(dflist[n].loc[dflist[n]['mass'] >= 8.])
    dflistLMUB.append(dflistUB[n].loc[dflistUB[n]['mass'] < 2.5])
    dflistLMESC.append(dflistESC[n].loc[dflistESC[n]['mass'] < 2.5])
    dflistLMall.append(dflist[n].loc[dflist[n]['mass'] < 2.5])

UB =[]
ESC =[]
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
 
    
##%% calling functions to calculate dispersion separately for different 
#
#from function_file import virial_radvelocity_dispersion,IQR_radvelocity_dispersion
#
#dflist[n].vir_radveldisp = virial_radvelocity_dispersion(dflist,dname,nlines)
#dflist[n].zvelIQR = IQR_radvelocity_dispersion(dflist,dname,nlines)
    
      

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

    
#%% Plots the PM-velocity and 3D-velocity of 20 simulations of unbound and escaped stars against each other.


fig1, (ax1,ax2) = plt.subplots(nrows=2, ncols=1,sharex=True)
fig1.set_size_inches(8.27,11.69)
plt.subplots_adjust(hspace=0)

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)


ax1.scatter(UB.loc[50].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(UB.loc[50]),1.0,len(UB.loc[50])) ,s=0.5, label = 'PM-velocity: energetically unbound stars (distance/snapshot)')
#ax1.scatter(UB.loc[50].sort_values('PM-vel')['PM-vel'],np.linspace(1/len(UB.loc[50]),1.0,len(UB.loc[50])) ,s=1, label = 'PM-velocity: energetically unbound stars from data')
ax2.scatter(UB.loc[50].sort_values('3D-veldist')['3D-veldist'],np.linspace(1/len(UB.loc[50]),1.0,len(UB.loc[50])) ,s=0.5, label = '3D-velocity: energetically unbound stars  (distance/snapshot)')
#ax2.scatter(UB.loc[50].sort_values('3D-vel')['3D-vel'],np.linspace(1/len(UB.loc[50]),1.0,len(UB.loc[50])) ,s=1, label = '3D-velocity: energetically unbound stars from data')

ax1.scatter(ESC.loc[50].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(ESC.loc[50]),1.0,len(ESC.loc[50])) ,s=0.5, label = 'PM-velocity: location-based escaped stars  (distance/snapshot)')
#ax1.scatter(ESC.loc[50].sort_values('PM-vel')['PM-vel'],np.linspace(1/len(ESC.loc[50]),1.0,len(ESC.loc[50])) ,s=1, label = 'PM-velocity: location-based escaped stars from data')
ax2.scatter(ESC.loc[50].sort_values('3D-veldist')['3D-veldist'],np.linspace(1/len(ESC.loc[50]),1.0,len(ESC.loc[50])) ,s=0.5, label = '3D-velocity: location-based escaped stars (distance/snapshot)')
#ax2.scatter(ESC.loc[50].sort_values('3D-vel')['3D-vel'],np.linspace(1/len(ESC.loc[50]),1.0,len(ESC.loc[50])) ,s=1, label = '3D-velocity: location-based escaped stars from data')


axes =[ax1,ax2]
ax1.set_title('Velocity distributions of unbound/escaped stars at 5 Myr of %s simulations' %nlines)
ax2.set_xlabel('Velocity (km/s)',fontsize=12.) 

for i in axes:
    i.legend(loc='lower right', frameon=False, title=legend[0])  
    i.xaxis.set_minor_locator(x_minor_locator)
    i.yaxis.set_minor_locator(y_minor_locator)
    i.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))
    i.set_ylabel('Cumulative distribution',fontsize=12.)
    i.set_xlim(left=0.)
    i.set_ylim(bottom=0.)

plt.show()


#%% radial, proper motion and space velocity dispersion separated by simulation for each snapshot for all dataframes listed in all_list
#radial velocity dispersion separated by simulation for each snapshot. 
#
#nsnaps=101
#
#star_list = [dflistHMUB]
#
#for i in star_list:
#    for n in range(nlines):
#        i[n].zveldisp = []
##        i[n].pmveldisp = []
##        i[n].spaceveldisp = []
#        
#        for ssnap in range(0,nsnaps):
#            
#            if (len(i[n].loc[ssnap])==0):  #this adds zero as the value of the dispersion for any snapshot without velocities
#                i[n].zveldisp.append(None)
##                i[n].pmveldisp.append(0.)
##                i[n].spaceveldisp.append(0.)
#                
#            else:    
#                i[n].zveldisp.append(statistics.pstdev(i[n].loc[ssnap,'zvel']))
##                i[n].pmveldisp.append(statistics.pstdev(i[n].loc[ssnap,'PM-veldist']))
##                i[n].spaceveldisp.append(statistics.pstdev(i[n].loc[ssnap,'3D-veldist']))
#
#
#print (dflistHMUB[8].zveldisp)

#%%

from function_file import radvelocity_dispersion, dispersion_median_minmax

UBzveldisp = radvelocity_dispersion(dflistUB,nlines)
ESCzveldisp = radvelocity_dispersion(dflistESC,nlines)
HMUBzveldisp = radvelocity_dispersion(dflistHMUB,nlines)
HMESCzveldisp = radvelocity_dispersion(dflistHMESC,nlines)

UBmediandisp,UBmindisp,UBmaxdisp = dispersion_median_minmax(UBzveldisp,nlines)
ESCmediandisp,ESCmindisp,ESCmaxdisp = dispersion_median_minmax(ESCzveldisp,nlines)
HMUBmediandisp,HMUBmindisp,HMUBmaxdisp = dispersion_median_minmax(HMUBzveldisp,nlines)
HMESCmediandisp,HMESCmindisp,HMESCmaxdisp = dispersion_median_minmax(HMESCzveldisp,nlines)

        
#%%

#plotting the median, min and max velocity dispersions for radial, PM and 


i = HMESCmediandisp
j = HMESCmaxdisp
k = HMESCmindisp


nsnaps=101

fig2 = plt.gca() 
#plt.subplots(nrows=1, ncols=3,sharey=True)

x = np.arange(0,10.1,0.1)

yerr_low_rv=[]
yerr_high_rv=[]
for ssnap in range(nsnaps):
    yerr_low_rv.append(i[ssnap]-k[ssnap])
    yerr_high_rv.append(j[ssnap]-i[ssnap])
plt.errorbar(x,i,yerr=[yerr_low_rv,yerr_high_rv], fmt='-x',markersize=3,elinewidth=0.5,capsize=1.5, label='Radial velocity')


#for n in range(nlines):
#    plt.scatter(x,dflist[n].zveldisp,s=2)  #velocity dispersion values separate for each simulation
#for n in range(nlines):
#    plt.scatter(x,dflist[n].spaceveldisp,s=2)  #velocity dispersion values separate for each simulation
fig2.set_title(legend[0],fontsize=10.)
plt.suptitle('Velocity dispersion')
fig2.set_xlabel('Time (Myr)',fontsize=12.) 
fig2.set_ylabel(r'$\sigma$ (in km/s)',fontsize=12.)   
fig2.set_xlim(left=0.,right=10.1)
fig2.set_ylim(bottom=0.)
fig2.legend(loc='lower right', frameon=False)  

plt.show()



    
#%% plot should be saved as 3 scenarios radial velocity dispersion
            
            
fig3, (ax1,ax2,ax3) = plt.subplots(nrows=1, ncols=3,sharey=True)
fig3.set_size_inches(11.69,8.27)
plt.subplots_adjust(wspace=0.02)

x = np.arange(0,10.1,0.1)

ax1.scatter(x,dflistUB.mediandisp_rv,s=3,label='All stars')
ax2.scatter(x,ESC.zveldisp,s=3,label='All stars')
ax3.scatter(x,All.zveldisp,s=3, label='All stars')
#ax3.scatter(x,mediandisp,s=3, label='All stars median velocity dispersion')

ax1.scatter(x,HMUB.zveldisp,s=3,label='High-mass stars')
ax2.scatter(x,HMESC.zveldisp,s=3,label='High-mass stars')
ax3.scatter(x,HMall.zveldisp,s=3, label='High-mass stars')

fig3.suptitle('Radial velocity dispersion for all snaps in 20 simulations: %s' %legend[0],fontsize=12.)
ax1.set_ylabel(r'$\sigma$ (in km/s)',fontsize=10.)   
ax1.legend(loc='lower right', frameon=False)  
axes = [ax1,ax2,ax3]
ax1.set_title('Energetically unbound',fontsize=10.)
ax2.set_title('Location-based escaped',fontsize=10.)
ax3.set_title('Full cluster',fontsize=10.)

for i in axes:
    i.legend(loc='lower center', frameon=False, fontsize=8.) 
    i.xaxis.set_minor_locator(x_minor_locator)
    i.yaxis.set_minor_locator(y_minor_locator)
    i.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))
    i.set_xlabel('Time (Myr)',fontsize=12.)
    i.set_xlim(left=0.,right=10.3)
    i.set_ylim(bottom=0.)


plt.show()


#%%

fig4, (ax1,ax2,ax3) = plt.subplots(nrows=1, ncols=3,sharey=True)
fig4.set_size_inches(11.69,8.27)
plt.subplots_adjust(wspace=0.02)

x = np.arange(0,10.1,0.1)

ax1.scatter(x,UB.spaceveldisp,s=3,label='All stars')
ax2.scatter(x,ESC.spaceveldisp,s=3,label='All stars')
ax3.scatter(x,All.spaceveldisp,s=3, label='All stars')

ax1.scatter(x,HMUB.spaceveldisp,s=3,label='High-mass stars')
ax2.scatter(x,HMESC.spaceveldisp,s=3,label='High-mass stars')
ax3.scatter(x,HMall.spaceveldisp,s=3, label='High-mass stars')

fig4.suptitle('3D-velocity dispersion for all snaps in 20 simulations: %s' %legend[0],fontsize=12.)
ax1.set_ylabel(r'$\sigma$ (in km/s)',fontsize=10.)   
ax1.legend(loc='lower right', frameon=False)  
axes = [ax1,ax2,ax3]
ax1.set_title('Energetically unbound',fontsize=10.)
ax2.set_title('Location-based escaped',fontsize=10.)
ax3.set_title('Full cluster',fontsize=10.)

for i in axes:
    i.legend(loc='lower center', frameon=False, fontsize=8.) 
    i.xaxis.set_minor_locator(x_minor_locator)
    i.yaxis.set_minor_locator(y_minor_locator)
    i.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))
    i.set_xlabel('Time (Myr)',fontsize=12.)
    i.set_xlim(left=0.,right=10.3)
    i.set_ylim(bottom=0.)


plt.show()