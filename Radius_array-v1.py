# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# This is the original code to plot the positions of stars and calculate half-mass radii, no COD-correction is included here. This is done in HM-radius.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


fname = input('Choose data file to be read into array: ')

df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap', 'star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

# Define snapshot and number of massive stars to be plotted

nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)


ssnap1 = int(input('Which snapshot? '))


nmass = int(input('How many of most massive stars should be plotted? '))

#Locating the n most massive stars in snap shots
df2 = df1.loc[ssnap1].nlargest(nmass, 'mass')

# Calculate half-mass and hm-radius, by creating a sorted new dataframe with an added colum for value of radius vector

radval = (np.sqrt(df1['radx']**2+df1['rady']**2+df1['radz']**2))


df4 = (df1.assign(rad=radval)).loc[ssnap1].sort_values('rad')

hm = (df4['mass'].sum())/2
cmass = df4['mass'].cumsum()

df5 = df4.assign(hmdif=np.abs(cmass-hm))
hmrad = df5.loc[df5['hmdif'].idxmin(),'rad']
    
#%% Plotting positions of stars from n-snapshot with m-number of massive stars and half-mass radius in x-y direction

f = plt.figure(figsize=(7,7))
ax = f.add_subplot(111)
ax.scatter(df1.loc[ssnap1,'radx'],df1.loc[ssnap1,'rady'],s=2,c='black',marker='o',label='All stars in snapshot %d' %ssnap1)
ax.scatter(df2['radx'],df2['rady'],s=25,c='red',marker='^',label='%d most massive stars in snapshot %d' %(nmass,ssnap1))
circ = plt.Circle((0,0), radius=hmrad, color='g', fill=False, label='Half-mass radius: %s pc' %hmrad)
ax.add_patch(circ)

plt.setp(ax.get_xticklabels(),fontsize=14)
plt.setp(ax.get_yticklabels(),fontsize=14)

plt.axes().set_aspect('equal', adjustable='datalim')

if ssnap1 <=10:
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
elif ssnap1 <=25:
    ax.set_xlim(-8,8)
    ax.set_ylim(-8,8)
elif ssnap1 <=50:
    ax.set_xlim(-15,15)
    ax.set_ylim(-15,15)
else:
    ax.set_xlim(-25,25)
    ax.set_ylim(-25,25)


ax.set_xlabel('x/pc',fontsize=16) # What happens without the r at the start here?
ax.set_ylabel('y/pc',fontsize=16)

plt.legend(loc='upper left', title='Simulation: %s' %fname);

plt.show

#%% Plotting positions of stars from n-snapshot with m-number of massive stars and half-mass radius in x-y direction

f1 = plt.figure(figsize=(7,7))
ax1 = f1.add_subplot(111)
ax1.scatter(df1.loc[ssnap1,'radx'],df1.loc[ssnap1,'radz'],s=2,c='black',marker='o',label='All stars in snapshot %d' %ssnap1)
ax1.scatter(df2['radx'],df2['radz'],s=25,c='red',marker='^',label='%d most massive stars in snapshot %d' %(nmass,ssnap1))
circ1 = plt.Circle((0,0), radius=hmrad, color='g', fill=False, label='Half-mass radius: %s pc' %hmrad)
ax1.add_patch(circ1)

plt.setp(ax1.get_xticklabels(),fontsize=14)
plt.setp(ax1.get_yticklabels(),fontsize=14)

plt.axes().set_aspect('equal', adjustable='datalim')

if ssnap1 <=10:
    ax1.set_xlim(-2,2)
    ax1.set_ylim(-2,2)
elif ssnap1 <=25:
    ax1.set_xlim(-8,8)
    ax1.set_ylim(-8,8)
elif ssnap1 <=50:
    ax1.set_xlim(-15,15)
    ax1.set_ylim(-15,15)
else:
    ax1.set_xlim(-25,25)
    ax1.set_ylim(-25,25)


ax1.set_xlabel('x/pc',fontsize=16) # What happens without the r at the start here?
ax1.set_ylabel('z/pc',fontsize=16)

plt.legend(loc='upper left', title='Simulation: %s' %fname);

plt.show

#%% y-z dimension

f2 = plt.figure(figsize=(7,7))
ax2 = f2.add_subplot(111)
ax2.scatter(df1.loc[ssnap1,'rady'],df1.loc[ssnap1,'radz'],s=2,c='black',marker='o',label='All stars in snapshot %d' %ssnap1)
ax2.scatter(df2['rady'],df2['radz'],s=25,c='red',marker='^',label='%d most massive stars in snapshot %d' %(nmass,ssnap1))
circ2 = plt.Circle((0,0), radius=hmrad, color='g', fill=False, label='Half-mass radius: %s pc' %hmrad)
ax2.add_patch(circ2)

plt.setp(ax2.get_xticklabels(),fontsize=14)
plt.setp(ax2.get_yticklabels(),fontsize=14)

plt.axes().set_aspect('equal', adjustable='datalim')

if ssnap1 <=10:
    ax2.set_xlim(-2,2)
    ax2.set_ylim(-2,2)
elif ssnap1 <=25:
    ax2.set_xlim(-8,8)
    ax2.set_ylim(-8,8)
elif ssnap1 <=50:
    ax2.set_xlim(-15,15)
    ax2.set_ylim(-15,15)
else:
    ax2.set_xlim(-25,25)
    ax2.set_ylim(-25,25)


ax2.set_xlabel('y/pc',fontsize=16) # What happens without the r at the start here?
ax2.set_ylabel('z/pc',fontsize=16)

plt.legend(loc='upper left', title='Simulation: %s' %fname);

plt.show

