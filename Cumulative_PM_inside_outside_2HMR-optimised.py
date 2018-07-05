# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import F_Transverse_Velocity_final as TV
import F_COD_Radius_Nstars as CODRN  #turn this on, if COD-correction is required.

f = open('file.txt')
lines = [line.rstrip('\n') for line in f]
f.close()

nlines = len(lines)

x=[]
fname=[]

for x in range(1,nlines+1,1):
    x = lines[x-1]
    fname.append(x)
    
df=[]
for y in range(1,nlines+1,1):
    y = 'df' + str(y)  
    df.append(y)    

for z in range(1,nlines+1,1):
    df[z] = pd.read_csv(fname[z-1], delim_whitespace=True, header=None,names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', \
                                 'velx', 'vely', 'velz', 'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', \
                                                                                                'mass', 'radx', 'rady', 'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64,\
                                'rady':np.float64, 'radz':np.float64})
  
    nsnaps = 101
    nstars = int((df[1].index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)

# Calculating CoD for file chosen in line 8 as filename and correcting for all radii for the shift in COD; results in an array cod(i,1:3) with i representing the snapshot and the 1:3 the three vector components -> to call the values for each dimension:
# x: cod[i,0], y: cod[i,1] and z: cod[i,2]

 
#for file 1
    nrad=0
    nrad = CODRN.cod_radius(fname[z-1],nsnaps,nstars)

    for ssnap in range(0,nsnaps):
        df[z].loc[ssnap,'nradx'] = nrad[ssnap,0]
        df[z].loc[ssnap,'nrady'] = nrad[ssnap,1]
        df[z].loc[ssnap,'nradz'] = nrad[ssnap,2]
    
    radval=(np.sqrt(df[z]['nradx']**2+df[z]['nrady']**2+df[z]['nradz']**2))
    
    hmrad =[]
    for ssnap in range(0, nsnaps):  
        summass=0
        hm=0
        cmass=0
        hmdif=0
        df12 = (df[z].assign(nrad=radval)).loc[ssnap].sort_values('nrad')
        summass = df12['mass'].sum()
        hm = (df12['mass'].sum())/2
        cmass = df12['mass'].cumsum()
        df13 = df12.assign(hmdif=np.abs(cmass-hm))
        hmrad.append(df13.loc[df13['hmdif'].idxmin(),'nrad'])      
    
    #Alternatively this can be calculated in Fortran and then imported to Python, which is faster
    
    transvel = 0        
    transvel = TV.transverse_velocity(fname[z-1],nsnaps,nstars)
    
    for ssnap in range(0,nsnaps):
        df[z].loc[0,'xdist'] = 0
        df[z].loc[0,'ydist'] = 0  
        df[z].loc[ssnap,'xdist'] = transvel[ssnap,0]
        df[z].loc[ssnap,'ydist'] = transvel[ssnap,1]  
        
    df[z]['PM-vel'] = (np.sqrt(df[z]['xdist']**2.+df[z]['ydist']**2.))


    df[z] = df[z].assign(nrad=radval).loc[50].sort_values('nrad')
    dfPMi = (df[z].loc[df[z]['nrad'] <= (hmrad[50]*2)])
    dfPMo = (df[z].loc[df[z]['nrad'] >= (hmrad[50]*2)])
      
    


#%% Plotting cumulative distribution of proper motion of stars located inside and outside of 2 x HMR for 4 snapshots
#
#from matplotlib.ticker import MaxNLocator
    
    f = plt.figure(figsize=(10,10)) 
    ax = f.add_subplot
             
    if fname[z][17] == 'X':
        legendtitle = (r'N=1000, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[z][7],fname[z][8],fname[z][22],fname[z][23],fname[z][12],fname[z][25:27]))
    elif fname[z][17] == '5':
        legendtitle = (r'N=500, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[z][7],fname[z][8],fname[z][22],fname[z][23],fname[z][12],fname[z][25:27]))
    elif fname[z][17] == '2':    
        legendtitle = (r'N=2000, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[z][7],fname[z][8],fname[z][22],fname[z][23],fname[z][12],fname[z][25:27]))
    elif fname[z][5:7] == '1r':
        legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, sim=%s' %fname[z][25:27])
    elif fname[z][5:7] == '2r':
        legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, sim=%s' %fname[z][25:27])
    
    
    
    ax.plot(141)
    ax.plot(df1PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df1PMi.index.size+1,1) ,c='b',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars' %df1PMi.index.size)
    ax1.plot(df1PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df1PMo.index.size+1,1) ,c='b',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars' %df1PMo.index.size)
    ax1.legend(loc='lower right', frameon=False, title=legend[0])  
    
    ax2.plot(142)
    ax2.plot(df2PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df2PMi.index.size+1,1) ,c='g',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars' %df2PMi.index.size)
    ax2.plot(df2PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df2PMo.index.size+1,1) ,c='g',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars' %df2PMo.index.size)
    ax2.legend(loc='lower right', frameon=False, title=legend[1])  
    
    ax3.plot(143)
    ax3.plot(df3PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df3PMi.index.size+1,1) ,c='r',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars' %df3PMi.index.size)
    ax3.plot(df3PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df3PMo.index.size+1,1) ,c='r',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars' %df3PMo.index.size)
    ax3.legend(loc='lower right', frameon=False, title=legend[2])  
    
    ax4.plot(144)
    ax4.plot(df4PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df4PMi.index.size+1,1) ,c='orange',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars' %df4PMi.index.size)
    ax4.plot(df4PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df4PMo.index.size+1,1) ,c='orange',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars' %df4PMo.index.size)
    ax4.legend(loc='lower right', frameon=False, title=legend[3])  
    
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
    
    plt.savefig('Cumulative velocity %s.png' %fname[z])

#%%