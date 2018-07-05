# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import F_COD_Radius_Nstars as CODRN

fname = input('Choose data file to be read into array: ')
strucpar = 10

df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velz':np.float64})

nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)


#The following bit passes the filename and the number of snaps and stars to the Fortran subroutine that calculates the COD and adjusts the radii by that COD.
#for cumulative velocity distribution plots, this is not necessary, but included for completion.

#nrad = CODRN.cod_radius(fname,nsnaps,nstars)
#
#for ssnap in range(0,nsnaps):
#    df1.loc[ssnap,'nradx'] = nrad[ssnap,0]
#    df1.loc[ssnap,'nrady'] = nrad[ssnap,1]
#    df1.loc[ssnap,'nradz'] = nrad[ssnap,2]



#%% Plotting cumulative distribution of radial velocities
snaplist = [0,5,10,50]

star = np.arange(1,nstars+1,1)

f = plt.figure(figsize=(10,10))
ax = f.add_subplot(111)

for locsnap in snaplist:
    
    if locsnap == 0:
        scattercolour ='b'
        line='-'
    elif locsnap == 5:
        scattercolour = 'g'
        line='--'
    elif locsnap == 10:
        scattercolour = 'r'
        line='-.'
    elif locsnap == 50:
        scattercolour = 'y'
        line=':' 
    
    dfvelz = df1.loc[locsnap].sort_values('velz')

    ax.plot(dfvelz['velz'],star,linestyle=line,label='%s Myr' %(locsnap/10))

plt.setp(ax.get_xticklabels(),fontsize=10)
plt.setp(ax.get_yticklabels(),fontsize=10)

ax.set_xlabel('Radial velocity (km/s)',fontsize=12) 
ax.set_ylabel(r'$N_{stars}$',fontsize=12)

plt.legend(loc='upper left',frameon=False,title=fname)

ax.set_xlim(-5,5)
ax.set_ylim(0,nstars)

plt.show
