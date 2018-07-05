# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code plots a histogram of the radial velocities for snapshots 0,5,10 and 50

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


fname = input('Choose data file to be read into array: ')


df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velz':np.float64})

nsnaps = 101
nstars = len(df1.loc[0])

#%%
snaplist = [0,5,10,50]

f = plt.figure(figsize=(10,10))
ax = f.add_subplot(111)

plt.yscale('log', nonposy='clip') #this line of code required if y-axis is logarithmic.

ax.set_xlabel('Radial velocity (km/s)',fontsize=12) 
ax.set_ylabel('$N_{stars}$',fontsize=12)

for locsnap in snaplist:
    
    if locsnap == 0:
        edgecolourtype ='b'
        filltype=False
        hatchtype = 'o'
    elif locsnap == 5:
        edgecolourtype = 'g'
        filltype=False
        hatchtype = '//'
    elif locsnap == 10:
        edgecolourtype = 'r'
        filltype=False
        hatchtype = 'x'
    elif locsnap == 50:
        edgecolourtype = 'y'
        filltype=False
        hatchtype = '/'
    
    ax.hist(df1.loc[locsnap,'velz'],bins=[-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,-0,1,2,3,4,5,6,7,8,9,10],fill=filltype,edgecolor=edgecolourtype, hatch=hatchtype, label='%s Myr' %(locsnap/10))


plt.legend(loc='upper left',frameon=False,title=fname)

plt.show()
