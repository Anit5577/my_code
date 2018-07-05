# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import F_Transverse_Velocity_final as TV
import F_COD_Radius_Nstars as CODRN  #turn this on, if COD-correction is required.

fname = input('Choose data file to be read into array: ')

df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

nsnaps = 101
nstars = (df1.loc[0].index.size)  #test with different number of stars from future simulations (count_stars.py)

# Calculating CoD for file chosen in line 8 as filename and correcting for all radii for the shift in COD; results in an array cod(i,1:3) with i representing the snapshot and the 1:3 the three vector components -> to call the values for each dimension:
# x: cod[i,0], y: cod[i,1] and z: cod[i,2]


nrad = CODRN.cod_radius(fname,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[ssnap,'nradx'] = nrad[ssnap,0]
    df1.loc[ssnap,'nrady'] = nrad[ssnap,1]
    df1.loc[ssnap,'nradz'] = nrad[ssnap,2]

# with the COD-corrected radii, the Half-mass radius is calculated for each snapshot
# Calculate half-mass and hm-radius, by creating a sorted new dataframe with an added colum for value of radius vector

radval=(np.sqrt(df1['nradx']**2+df1['nrady']**2+df1['nradz']**2))

hmrad =[]
for ssnap in range(0, nsnaps):  
    summass=0
    hm=0
    cmass=0
    hmdif=0
    df2 = (df1.assign(nrad=radval)).loc[ssnap].sort_values('nrad')
    summass = df2['mass'].sum()
    hm = (df2['mass'].sum())/2
    cmass = df2['mass'].cumsum()
    df3 = df2.assign(hmdif=np.abs(cmass-hm))
    hmrad.append(df3.loc[df3['hmdif'].idxmin(),'nrad'])      
    print (df3['hmdif'].min())    

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel = TV.transverse_velocity(fname,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[0,'xdist'] = 0
    df1.loc[0,'ydist'] = 0  
    df1.loc[ssnap,'xdist'] = transvel[ssnap,0]
    df1.loc[ssnap,'ydist'] = transvel[ssnap,1]  

#Proper motion velocity column is added to all snapshots:
    
df1['PM-vel'] = (np.sqrt(df1['xdist']**2.+df1['ydist']**2.))

# for snapshot 1,5,10 and 50 the all columns are extracted for values of nrad that are within/equal 2 times halfmass-radius or wihout/equal 2 times halfmass-radius

df2 = df1.assign(nrad=radval).loc[1].sort_values('nrad')
df1PMi = (df2.loc[df2['nrad'] <= (hmrad[1]*2)])
df1PMo = (df2.loc[df2['nrad'] >= (hmrad[1]*2)])

df5 = df1.assign(nrad=radval).loc[5].sort_values('nrad')
df5PMi = (df5.loc[df5['nrad'] <= (hmrad[5]*2)])
df5PMo = (df5.loc[df5['nrad'] >= (hmrad[5]*2)])

df10 = df1.assign(nrad=radval).loc[10].sort_values('nrad')
df10PMi = (df10.loc[df10['nrad'] <= (hmrad[10]*2)])
df10PMo = (df10.loc[df10['nrad'] >= (hmrad[10]*2)])

df50 = df1.assign(nrad=radval).loc[50].sort_values('nrad')
df50PMi = (df50.loc[df50['nrad'] <= (hmrad[50]*2)])
df50PMo = (df50.loc[df50['nrad'] >= (hmrad[50]*2)])
        
#%% Plotting cumulative distribution of proper motion of stars located inside and outside of 2 x HMR for 4 snapshots
#
#from matplotlib.ticker import MaxNLocator
    
fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(15.,15.))
plt.subplots_adjust(wspace=0.2)
x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

if fname[17] == 'X':
    legendtitle = (r'N=1000, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
elif fname[17] == '5':
    legendtitle = (r'N=500, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
elif fname[17] == '2':    
    legendtitle = (r'N=2000, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
elif fname[5:7] == '1r':
    legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, sim=%s' %fname[25:27])
elif fname[5:7] == '2r':
    legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, sim=%s' %fname[25:27])


ax1.plot(141)
ax1.plot(df1PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df1PMi.index.size+1,1) ,c='b',linestyle='-',label='Inside 2x HMR at 0.1 Myr: %s stars' %df1PMi.index.size)
ax1.plot(df1PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df1PMo.index.size+1,1) ,c='b',linestyle=':',label='Outside 2x HMR at 0.1 Myr: %s stars' %df1PMo.index.size)
ax1.legend(loc='lower right', frameon=False, title=legendtitle)  

ax2.plot(142)
ax2.plot(df5PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df5PMi.index.size+1,1) ,c='g',linestyle='-',label='Inside 2x HMR at 0.5 Myr: %s stars' %df5PMi.index.size)
ax2.plot(df5PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df5PMo.index.size+1,1) ,c='g',linestyle=':',label='Outside 2x HMR at 0.5 Myr: %s stars' %df5PMo.index.size)
ax2.legend(loc='lower right', frameon=False, title=legendtitle)  

ax3.plot(143)
ax3.plot(df10PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df10PMi.index.size+1,1) ,c='r',linestyle='-',label='Inside 2x HMR at 1 Myr: %s stars' %df10PMi.index.size)
ax3.plot(df10PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df10PMo.index.size+1,1) ,c='r',linestyle=':',label='Outside 2x HMR at 1 Myr: %s stars' %df10PMo.index.size)
ax3.legend(loc='lower right', frameon=False, title=legendtitle)  

ax4.plot(144)
ax4.plot(df50PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df50PMi.index.size+1,1) ,c='orange',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars' %df50PMi.index.size)
ax4.plot(df50PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df50PMo.index.size+1,1) ,c='orange',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars' %df50PMo.index.size)
ax4.legend(loc='lower right', frameon=False, title=legendtitle)  

axes = [ax1,ax2,ax3,ax4]

for i in axes:
    i.xaxis.set_minor_locator(x_minor_locator)
    i.yaxis.set_minor_locator(y_minor_locator)
    i.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))
    i.set_xlabel('Proper motion (km/s)',fontsize=12.) 
    i.set_ylabel(r'$N_{stars}$',fontsize=12.)
    i.set_xlim(left=0)
    i.set_ylim(0,nstars)

plt.show()

#plt.savefig('Cumulative velocity %s.png' %fname)

#%%