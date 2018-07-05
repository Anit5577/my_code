# this code calculates and plots the cumulative PM and 3D velocity for all snaps in all simulations that are read in from an input text file


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator
from function_file import read_in_any_datafiles, velocity_elements, energy_stars, stars_in_outside_2HMR 


dflist,dname,nlines  = read_in_any_datafiles('file_evolved.txt') #this reads in the .dat files from an inputfile list

#the functions below are not used for the simulations with stellar evolustion, as issue with Fortran concerning loss of stars in simulations is not yet solved
#dflist = energy_stars(dflist,dname,nlines)       #this calculates the energy of each star in each snapshot an simulation and adds this in a column
#dflist = velocity_elements(dflist,dname,nlines)  #this calculates the velocity by using the distance travelled between each snapshot and divides it by snapshot length - this is an alternative to the provided velocities from the simulation
#dflist = stars_in_outside_2HMR(dflist,dname,nlines)  # this calculates the half-mass radius based on centre of density corrected locations and then adds a column identifying if the stars are inside or outside 2*HMR


#%%

# This creates the filename for including the intial conditions by using filename[0]

filename = []

for fname in dname: # to allow the filename of the simulations to dictate the labels
        
    if fname[21] == 'E':
       if fname[17] == 'X':
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_1000' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_500' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_2000' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = ('%s_sim_1.6_0.3_1pc_E_1000'%nlines)
       elif fname[5:7] == '2r':
           legendtitle = ('%s_sim_3.0_0.5_1pc_E_1000'%nlines)

    if fname[21] == 'S':
       if fname[17] == 'X':
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_1000' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_500' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_2000' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = ('%s_sim_1.6_0.3_1pc_S_1000'%nlines)
       elif fname[5:7] == '2r':
           legendtitle = ('%s_sim_3.0_0.5_1pc_S_1000'%nlines)
    filename.append(legendtitle)


#%% this calculates the 3D and PM-velocity from the 1D-velocities that are part of the original data. This is used due to Fortran issues in losing stars in later snapshots
  
for n in range(nlines):    
        dflist[n]['3D-velxyz'] = (np.sqrt(dflist[n]['velx']**2.+dflist[n]['vely']**2.+dflist[n]['velz']**2.)) #3D-velocity from distance/snapshot length
        dflist[n]['PM-velxy'] = (np.sqrt(dflist[n]['velx']**2.+dflist[n]['vely']**2.))  #PM-velocity from 1D-velocities in file.

print (dflist[8])    


#%% This saves all 20 simulations for a set of initial conditions into 1 single file
All =[]

for n in range(nlines):
    All.append(dflist[n])

All = pd.concat(All)      

# saves the file with All n-simulations into one file, chosing 8 columns from a total of 26; chosing a smaller number of columns was done to reduce the total filesize.
All.to_csv('All_%s.csv' %filename[0],columns = ['snap','star','time','mass','PM-velxyz','3D-velxy'],index=['snap','star'])

    
#%% Plots the PM-velocity 20 simulations of all stars against each other in a cumulative distribution

legend =[]

for fname in dname: # to allow the filename of the simulations to dictate the labels
        
    if fname[21] == 'E':
       if fname[17] == 'X':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution, $N_{sim}$=1000' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution, $N_{sim}$=500' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution, $N_{sim}$=2000' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, stellar evolution, =$N_{sim}$=1000')
       elif fname[5:7] == '2r':
           legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, stellar evolution, $N_{sim}$=1000')

    if fname[21] == 'S':
       if fname[17] == 'X':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution, $N_{sim}$=1000' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution,$N_{sim}$=500' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution, $N_{sim}$=2000' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, no evolution, $N_{sim}$=1000')
       elif fname[5:7] == '2r':
           legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, no evolution,$N_{sim}$=1000')
    legend.append(legendtitle)

fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
plt.subplots_adjust(hspace=0.01,wspace=0.01)      
#fig1, ((ax1,ax2)) = plt.subplots(nrows=1, ncols=2, sharey=True)
plt.subplots_adjust(hspace=0.01,wspace=0.04)    
#fig2, ((ax3,ax4)) = plt.subplots(nrows=1, ncols=2, sharey=True)
plt.subplots_adjust(hspace=0.01,wspace=0.04)    
fig.set_size_inches(11.69,8.27)
fig1.set_size_inches(11.69,8.27)
fig2.set_size_inches(11.69,8.27)

x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)


for n in range(nlines):
    ax1.scatter(dflist[n].loc[1].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(dflist[n].loc[1]),1.0,len(dflist[n].loc[1])) ,s=0.5)
    ax2.scatter(dflist[n].loc[10].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(dflist[n].loc[10]),1.0,len(dflist[n].loc[10])) ,s=0.5)
    ax3.scatter(dflist[n].loc[50].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(dflist[n].loc[50]),1.0,len(dflist[n].loc[50])) ,s=0.5)
    ax4.scatter(dflist[n].loc[100].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(dflist[n].loc[100]),1.0,len(dflist[n].loc[100])) ,s=0.5)

ax1.legend (loc='lower right',frameon=False, title='Cluster age: 0.1 Myr')
ax2.legend (loc='lower right',frameon=False, title='Cluster age: 1.0 Myr')
ax3.legend (loc='lower right',frameon=False, title='Cluster age: 5.0 Myr')
ax4.legend (loc='lower right',frameon=False, title='Cluster age: 10.0 Myr')


fig2.suptitle('Proper motion distributions of %s simulations with initial conditions: \n %s' %(nlines,legend[0]),fontsize=12.)
fig1.suptitle('Proper motion distributions of %s simulations with initial conditions: \n %s' %(nlines,legend[0]),fontsize=12.)
fig.suptitle('Proper motion distributions of %s simulations with initial conditions: \n %s' %(nlines,legend[0]),fontsize=12.)
ax1.set_xlabel('Velocity (km/s)',fontsize=10.)
ax2.set_xlabel('Velocity (km/s)',fontsize=10.)
ax3.set_xlabel('Velocity (km/s)',fontsize=10.)
ax4.set_xlabel('Velocity (km/s)',fontsize=10.)
ax1.set_ylabel('Cumulative distribution',fontsize=10.)
ax3.set_ylabel('Cumulative distribution',fontsize=10.)

axes = [ax1,ax2,ax3,ax4]

for ax in axes:
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)
    ax.tick_params(which='both',direction='in',top='on',right='on')
#    ax.set_xscale('log')
    ax.set_ylim(0.,1.03)
ax1.set_xlim(0.)
ax2.set_xlim(0.)
ax3.set_xlim(0.)
ax4.set_xlim(0.)
plt.show()

#plt.savefig('Scatter_%s.png' %filename[0])


#%% reading in all files with 20 simulations All_read

import pandas as pd

f = open('file20.txt')
lines = [line.rstrip('\n') for line in f]

nlines = len(lines)

A={}
for x in range (1,nlines+1,1):
    A['fname{0}'.format(x)]=lines[x-1]

f.close()      

fname = sorted(A.values())

All_read=[]
for n in range(nlines):
    All_read.append(n) 
    All_read[n] = pd.read_csv(fname[n],index_col=['snap','star'],usecols=['snap','star','time','mass','PM-veldist','3D-veldist','Unbound','escaped'])



#%%
    
fig3, ax = plt.subplots()

#time = [1,10,50,100]
time =[100]

for n in time:
    
    ax.scatter(All_read[0].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[0].loc[n]),1.0,len(All_read[0].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[0][11:14],fname[0][15:18])))
    ax.scatter(All_read[1].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[1].loc[n]),1.0,len(All_read[1].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[1][11:14],fname[1][15:18])))
    ax.scatter(All_read[2].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[2].loc[n]),1.0,len(All_read[2].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[2][11:14],fname[2][15:18])))
    ax.scatter(All_read[3].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[3].loc[n]),1.0,len(All_read[3].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[3][11:14],fname[3][15:18])))
    ax.scatter(All_read[4].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[4].loc[n]),1.0,len(All_read[4].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[4][11:14],fname[4][15:18])))
    ax.scatter(All_read[5].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[5].loc[n]),1.0,len(All_read[5].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[5][11:14],fname[5][15:18])))
    ax.scatter(All_read[6].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[6].loc[n]),1.0,len(All_read[6].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[6][11:14],fname[6][15:18])))
    ax.scatter(All_read[7].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[7].loc[n]),1.0,len(All_read[7].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[7][11:14],fname[7][15:18])))
    ax.scatter(All_read[8].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[8].loc[n]),1.0,len(All_read[8].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[8][11:14],fname[8][15:18])))
    ax.scatter(All_read[9].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[9].loc[n]),1.0,len(All_read[9].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[9][11:14],fname[9][15:18])))

ax.set_xlabel('Velocity (log(km/s))',fontsize=10.)
ax.set_ylabel('Cumulative distribution',fontsize=10.)
ax.legend (loc='lower right',frameon=False,title=('Cluster age %s Myr' %(time[0]/10)))
ax.set_xlim(0.,10.)
ax.set_ylim(0.,1.03)
ax.set_title('Cumulative PM-velocity distributions for different initial conditions',fontsize=12.)
#ax.set_xscale('log')

plt.show()





#%% Kolmogorov-Smirnof 2 sample test:

from scipy import stats
from matplotlib.ticker import PercentFormatter
ax.yaxis.set_major_formatter(PercentFormatter())

i = (8) #All_read initial condition dataset x
j = (9) #All_read initial condition dataset y

data1 = All_read[i].loc[100].sort_values('PM-veldist')['PM-veldist']
data2 = All_read[j].loc[100].sort_values('PM-veldist')['PM-veldist']
data3 = All_read[i].loc[50].sort_values('PM-veldist')['PM-veldist']
data4 = All_read[j].loc[50].sort_values('PM-veldist')['PM-veldist']
data5 = All_read[i].loc[10].sort_values('PM-veldist')['PM-veldist']
data6 = All_read[j].loc[10].sort_values('PM-veldist')['PM-veldist']
data7 = All_read[i].loc[1].sort_values('PM-veldist')['PM-veldist']
data8 = All_read[j].loc[1].sort_values('PM-veldist')['PM-veldist']

k=[]
l=[]
pvalue1 =[]
pvalue2 =[]
pvalue3 =[]
pvalue4 =[]

step = 50

for k,l in zip(range(0,20001-step,step), range(step,20001,step)): #use this when to construct for loops with two different value i and j that are used pairwise, e,g i[0]j[0],i[1]j[1]
#    print (i,j)
    #    print(stats.ks_2samp(data1[i:j], data2[i:j]))  
    pvalue1.append((stats.ks_2samp(data1[k:l], data2[k:l])[1])*100) 
    pvalue2.append((stats.ks_2samp(data3[k:l], data4[k:l])[1])*100) 
    pvalue3.append((stats.ks_2samp(data5[k:l], data6[k:l])[1])*100) 
    pvalue4.append((stats.ks_2samp(data7[k:l], data8[k:l])[1])*100)  

        
x= np.arange(1,20001,step)

fig6, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2,sharex=True,sharey=True)
plt.subplots_adjust(hspace=0.1,wspace=0.1) 

ax4.scatter(x,pvalue1,s=1.0, label=('10 Myr'))  
ax3.scatter(x,pvalue2,s=1.0, label=('5 Myr'))      
ax2.scatter(x,pvalue3,s=1.0, label=('1 Myr'))    
ax1.scatter(x,pvalue4,s=1.0, label=('0.1 Myr'))    
ax1.set_ylabel('P-value')
ax3.set_ylabel('P-value')
ax3.set_xlabel('N-stars')
ax4.set_xlabel('N-stars')
fig6.suptitle(r'Two-sample Kolmogorov-Smirnoff: D=%s with $\alpha_{vir}$=%s vs $\alpha_{vir}$=%s'%(fname[i][11:14],fname[i][15:18],fname[j][15:18]))

axes = [ax1,ax2,ax3,ax4]

for ax in axes:
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)
    ax.tick_params(which='both',direction='in',top='on',right='on')
    ax.axhline(5, label=('5% significance level'),lw=1.0,c='red')
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.legend(frameon=False,fontsize=8.)
    ax.set_ylim(0.,100.)
    ax.set_xlim(0.,20000.)


plt.show()

#%%

fig4, ax = plt.subplots()

time = [1,10,20,30,40,50,60,70,80,90,100]
init_cond =[9]

for j in init_cond:
    
    ax.scatter(All_read[j].loc[1].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[1]),1.0,len(All_read[j].loc[1])) ,s=0.5,label=('%s Myr' %(time[0]/10)))
    ax.scatter(All_read[j].loc[10].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[10]),1.0,len(All_read[j].loc[10])) ,s=0.5,label=('%s Myr' %(time[1]/10)))
#    ax.scatter(All_read[j].loc[20].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[20]),1.0,len(All_read[j].loc[20])) ,s=0.5,label=('%s Myr' %(time[2]/10)))
#    ax.scatter(All_read[j].loc[30].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[30]),1.0,len(All_read[j].loc[30])) ,s=0.5,label=('%s Myr' %(time[3]/10)))
#    ax.scatter(All_read[j].loc[40].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[40]),1.0,len(All_read[j].loc[40])) ,s=0.5,label=('%s Myr' %(time[4]/10)))
    ax.scatter(All_read[j].loc[50].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[50]),1.0,len(All_read[j].loc[50])) ,s=0.5,label=('%s Myr' %(time[5]/10)))
#    ax.scatter(All_read[j].loc[60].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[60]),1.0,len(All_read[j].loc[60])) ,s=0.5,label=('%s Myr' %(time[6]/10)))
#    ax.scatter(All_read[j].loc[70].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[70]),1.0,len(All_read[j].loc[70])) ,s=0.5,label=('%s Myr' %(time[7]/10)))
#    ax.scatter(All_read[j].loc[80].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[80]),1.0,len(All_read[j].loc[80])) ,s=0.5,label=('%s Myr' %(time[8]/10)))
#    ax.scatter(All_read[j].loc[90].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[90]),1.0,len(All_read[j].loc[90])) ,s=0.5,label=('%s Myr' %(time[9]/10)))
    ax.scatter(All_read[j].loc[100].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[j].loc[100]),1.0,len(All_read[j].loc[100])) ,s=0.5,label=('%s Myr' %(time[10]/10)))
    ax.set_title('Cumulative PM-velocity distributions at different times: \n D=%s, $alpha_{vir}=%s$'%(fname[j][11:14],fname[j][15:18]),fontsize=12.)

ax.set_xlabel('Velocity (log(km/s))',fontsize=10.)
ax.set_ylabel('Cumulative distribution',fontsize=10.)
ax.legend (loc='lower right',frameon=False,title=('Cluster age:'))
ax.set_xlim(0.,10.)
ax.set_ylim(0.,1.03)
#ax.set_xscale('log')

plt.show()

#%% QQ-plot checking similarity of distributions

fig5, ax = plt.subplots()

#time = [1,10,50,100]
i = (8)
j = (9)

data1 = All_read[i].loc[100].sort_values('PM-veldist')['PM-veldist']
data2 = All_read[j].loc[100].sort_values('PM-veldist')['PM-veldist']
data3 = All_read[i].loc[50].sort_values('PM-veldist')['PM-veldist']
data4 = All_read[j].loc[50].sort_values('PM-veldist')['PM-veldist']
data5 = All_read[i].loc[10].sort_values('PM-veldist')['PM-veldist']
data6 = All_read[j].loc[10].sort_values('PM-veldist')['PM-veldist']
data7 = All_read[i].loc[1].sort_values('PM-veldist')['PM-veldist']
data8 = All_read[j].loc[1].sort_values('PM-veldist')['PM-veldist']


ax.scatter(data1,data2,s=0.5,label='%d Myr' %(100/10))
ax.scatter(data3,data4,s=0.5,label='%d Myr' %(50/10))
ax.scatter(data5,data6,s=0.5,label='%d Myr' %(10/10))
ax.scatter(data7,data8,s=0.5,label='%s Myr' %(1./10.))
ax.plot(data1,data1,color='red',linewidth=0.5, label='Equal distribution')
#    ax.scatter(All_read[i].loc[n].sort_values('PM-veldist')['PM-veldist'],np.linspace(1/len(All_read[1].loc[n]),1.0,len(All_read[1].loc[n])) ,s=0.5,label=(r'D=%s, $\alpha_{vir}$=%s'%(fname[1][11:14],fname[1][15:18])))
#ax.scatter(x) 
ax.set_xlabel(r'PM-velocity (km/s): D=%s, $\alpha_{vir}$=%s'%(fname[i][11:14],fname[i][15:18]),fontsize=10.)
ax.set_ylabel(r'PM-velocity (km/s): D=%s, $\alpha_{vir}$=%s'%(fname[j][11:14],fname[j][15:18]),fontsize=10.)
ax.legend(loc='upper left',frameon=False)
ax.set_xlim(0,5)
#ax.set_xticklabels(tick_labels.astype(int))
ax.set_ylim(0,5)
ax.set_title('QQ-plot of cumulative velocity distributions',fontsize=12.)
#ax.set_xscale('log')

plt.show()
