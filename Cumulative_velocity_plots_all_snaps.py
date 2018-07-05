# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import F_Transverse_Velocity_final as TV
#import F_COD_Radius_Nstars as CODRN  #turn this on, if COD-correction is required.

fname = input('Choose data file to be read into array: ')

df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})

nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)

##The following bit passes the filename and the number of snaps and stars to the Fortran subroutine that calculates the COD and adjusts the radii by that COD.

#nrad = CODRN.cod_radius(fname,nsnaps,nstars)
#
## The following cell uses the information for the new COD-corrected positions of the stars and calculates the x and y distances covered between each snapshot.
## This is not useful, when calculating changes of positions between snaps, as the COD is different in each snapshot, affecting the radii differently
#
#for ssnap in range(0,nsnaps):
#    df1.loc[ssnap,'nradx'] = nrad[ssnap,0]
#    df1.loc[ssnap,'nrady'] = nrad[ssnap,1]
##    df1.loc[ssnap,'nradz'] = nrad[ssnap,2]  
#
#    df2 = df1.sort_index()
#
#    df2.loc[0, 'xdist'] =  nrad[0,0] 
#    df2.loc[0, 'ydist'] =  nrad[0,1] 
#    
#    df2.loc[0, 'nradx'] =  nrad[0,0]   
#    df2.loc[0, 'nrady'] =  nrad[0,1] 
#        
#for ssnap in range (0,nsnaps-1):  
#    for stars in range(1,nstars+1):
#        df2.loc[ssnap+1,stars]['xdist'] = df2.loc[ssnap+1,stars]['nradx'] - df2.loc[ssnap,stars]['nradx']
#        df2.loc[ssnap+1,stars]['ydist'] = df2.loc[ssnap+1,stars]['nrady'] - df2.loc[ssnap,stars]['nrady']
#             
## To save to file: 
#df2.to_csv('transveltest %s' %fname)

# The following cell uses the uncorrected positions of stars to calcualte the 2D proper motion (distance covered between snapshots / duration of snapshot)

#df2 = df1.sort_index()
#   
#for ssnap in range(0,nsnaps-1):
#    for stars in range(1,nstars+1):
#        df2.loc[0,'xdist'] = df2.loc[0,'radx']
#        df2.loc[0,'ydist'] = df2.loc[0,'rady']  
#        df2.loc[ssnap+1,stars]['xdist'] = df2.loc[ssnap+1,stars]['radx'] - df2.loc[ssnap,stars]['radx']
#        df2.loc[ssnap+1,stars]['ydist'] = df2.loc[ssnap+1,stars]['rady'] - df2.loc[ssnap,stars]['rady']
        
#df2.to_csv('PM_velocity_%s' %fname)       

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel = TV.transverse_velocity(fname,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[0,'xdist'] = 0
    df1.loc[0,'ydist'] = 0 
    df1.loc[ssnap,'xdist'] = transvel[ssnap,0]
    df1.loc[ssnap,'ydist'] = transvel[ssnap,1]

# as the Fortran program uses the initial positions for the distance travelled in snapshot one, these should be set 0 before plotting    
  

print (df1)

        
#%% Plotting cumulative distribution of 2D-velocities of x and y component, proper motion velocities and 3D velocities on one plot

from matplotlib.ticker import MaxNLocator

snaplist = [0,5,10,50]
star = np.arange(1,nstars+1,1)

fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=1, ncols=4, figsize=(20.,10.),sharey=True)
plt.subplots_adjust(wspace=0.04)
#x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

if fname[17] == 'X':
    legendtitle = (r'N=1000, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
elif fname[17] == '5':
    legendtitle = (r'N=500, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
elif fname[17] == '2':    
    legendtitle = (r'N=2000, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
else:
    legendtitle = fname
    
for locsnap in snaplist:
    
    if locsnap == 0:
        linecolour ='b'
        line1='-'
    elif locsnap == 5:
        linecolour = 'g'
        line1='--'
    elif locsnap == 10:
        linecolour = 'r'
        line1='-.'
    elif locsnap == 50:
        linecolour = 'y'
        line1=':'
        
    df1.loc[locsnap,'transvel'] = (np.sqrt(df1['velx']**2.+df1['vely']**2.))
    dftransvel = df1.loc[locsnap].sort_values('transvel')
    
    df1.loc[locsnap,'2D-PM-vel'] = (np.sqrt(df1['xdist']**2. + df1['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df2Dvel = df1.loc[locsnap].sort_values('2D-PM-vel')

    df1.loc[locsnap,'3Dvel'] = (np.sqrt(df1['velx']**2.+df1['vely']**2.+df1['velz']**2.))
    df3Dvel = df1.loc[locsnap].sort_values('3Dvel')
    
    df1.loc[locsnap,'radvel'] = (np.sqrt(df1['velz']**2.))
    dfradvel = df1.loc[locsnap].sort_values('radvel')
    
    ax1.plot(141)
    ax1.plot(df2Dvel['2D-PM-vel'],star,c=linecolour,linestyle=line1,label='Proper motion: %s Myr' %(locsnap/10))
        
    ax2.plot(142)
    ax2.plot(dftransvel['transvel'],star,c=linecolour,linestyle=line1,label='2D velocity: %s Myr' %(locsnap/10))
    
    ax3.plot(143)
    ax3.plot(df3Dvel['3Dvel'],star,c=linecolour,linestyle=line1,label='3D velocity: %s Myr' %(locsnap/10))
    
    ax4.plot(144)
    ax4.plot(dfradvel['radvel'],star,c=linecolour,linestyle=line1,label='Radial velocity: %s Myr' %(locsnap/10))

ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
ax1.yaxis.set_minor_locator(y_minor_locator)
ax1.tick_params(which='both',direction='in',top='on',right='on')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

ax1.set_xlabel('Proper motion (km/s)',fontsize=12.) 
ax1.set_ylabel(r'$N_{stars}$',fontsize=12.)

ax1.legend(loc='lower right', frameon=False,title=legendtitle)

ax2.xaxis.set_minor_locator(AutoMinorLocator(2))
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which='both',direction='in',top='on',right='on')
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

ax2.set_xlabel('2D velocity (km/s)',fontsize=12.) 
#ax2.set_ylabel(r'$N_{stars}$',fontsize=12)

ax2.legend(loc='lower right', frameon=False,title=legendtitle)

ax3.xaxis.set_minor_locator(AutoMinorLocator(2))
ax3.yaxis.set_minor_locator(y_minor_locator)
ax3.tick_params(which='both',direction='in',top='on',right='on')
ax3.xaxis.set_major_locator(MaxNLocator(integer=True))

ax3.set_xlabel('3D velocity (km/s)',fontsize=12.) 
#ax3.set_ylabel(r'$N_{stars}$',fontsize=12)

ax3.legend(loc='lower right', frameon=False,title=legendtitle)

ax4.xaxis.set_minor_locator(AutoMinorLocator(2))
ax4.yaxis.set_minor_locator(y_minor_locator)
ax4.tick_params(which='both',direction='in',top='on',right='on',labelright='on')
ax4.xaxis.set_major_locator(MaxNLocator(integer=True))

ax4.set_xlabel('Radial velocity (km/s)',fontsize=12.) 
#ax4.set_ylabel(r'$N_{stars}$',fontsize=12)

ax4.legend(loc='lower right', frameon=False,title=legendtitle)

ax1.set_xlim(left=0)
ax1.set_ylim(0,nstars)

ax2.set_xlim(left=0)
ax2.set_ylim(0,nstars)

ax3.set_xlim(left=0)
ax3.set_ylim(0,nstars)

ax4.set_xlim(left=0)
ax4.set_ylim(0,nstars)

plt.show()

#plt.savefig('Cumulative velocity %s.png' %fname)