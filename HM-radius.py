# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code first calculates the COD of the cluster, corrects for star positions by any movements from the origin, it then calculates the hm-radius and finally plots all of the stars in the 3 dimensions.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import F_COD_Radius_Nstars as CODRN

fname = input('Choose data file to be read into array: ')

df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)

#%% Calculating CoD for file chosen in line 8 as filename and correcting for all radii for the shift in COD; results in an array cod(i,1:3) with i representing the snapshot and the 1:3 the three vector components -> to call the values for each dimension:
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


#%% Centre of Mass code to check the COD against the COD calculated above

#com = []
#for ssnap in range(0, nsnaps):
#    summass=0
#    mradx=0
#    mrady=0
#    mradz=0 
#    summass = df1.loc[ssnap,'mass'].sum()
#    mradx = (np.sum(df1.loc[ssnap,'radx']*df1.loc[ssnap,'mass']))/summass
#    mrady = (np.sum(df1.loc[ssnap,'rady']*df1.loc[ssnap,'mass']))/summass
#    mradz = (np.sum(df1.loc[ssnap,'radz']*df1.loc[ssnap,'mass']))/summass
#    com.append([ssnap,mradx,mrady,mradz])  
# 
    
#%% To plot a certain snapshot and n-number of massive stars, the following code uses user input

# Define snapshot and number of massive stars to be plotted

ssnap1 = int(input('Which snapshot should be plotted? '))

nmass = int(input('How many of the most massive stars should be plotted? '))

#Locating the n most massive stars in snap shots
df2 = df1.loc[ssnap1].nlargest(nmass, 'mass')

#%% Plotting positions of stars from n-snapshot with m-number of massive stars and half-mass radius in x-y direction

f = plt.figure(figsize=(7,7))
ax = f.add_subplot(111)
ax.scatter(df1.loc[ssnap1,'nradx'],df1.loc[ssnap1,'nrady'],s=2,c='black',marker='o',label='All stars in snapshot %d' %ssnap1)

#To plot the non COD-corrected star positions, use the following:
#ax.scatter(df1.loc[ssnap1,'radx'],df1.loc[ssnap1,'rady'],s=2,c='#999999',marker='o',label='nonCOD-stars %d' %ssnap1)
ax.scatter(df2['nradx'],df2['nrady'],s=25,c='red',marker='^',label='%d most massive stars in snapshot %d' %(nmass,ssnap1))
#ax.scatter(mradx,mrady,s=5,c='blue',marker='s',label='COM')
circ = plt.Circle((0,0), radius=hmrad[ssnap1], color='g', fill=False, label='Half-mass radius: %s pc' %round(hmrad[ssnap1],5))
circ = plt.Circle((0,0), radius=(2*hmrad[ssnap1]), color='b', fill=False, label='2*half-mass radius: %s pc' %round(2*hmrad[ssnap1],5))
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

plt.legend(loc='upper left', frameon=False, title='Simulation: %s' %fname);

plt.show

#%% Plotting positions of stars from n-snapshot with m-number of massive stars and half-mass radius in x-z direction

f1 = plt.figure(figsize=(7,7))
ax1 = f1.add_subplot(111)
ax1.scatter(df1.loc[ssnap1,'nradx'],df1.loc[ssnap1,'nradz'],s=2,c='black',marker='o',label='All stars in snapshot %d' %ssnap1)
ax1.scatter(df2['nradx'],df2['nradz'],s=25,c='red',marker='^',label='%d most massive stars in snapshot %d' %(nmass,ssnap1))
#To plot the non COD-corrected star positions, use the following:
#ax1.scatter(df1.loc[ssnap1,'radx'],df1.loc[ssnap1,'radz'],s=2,c='#999999',marker='o',label='nonCOD-stars %d' %ssnap1)
#ax1.scatter(mradx,mradz,s=5,c='blue',marker='s',label='COM')
circ1 = plt.Circle((0,0), radius=hmrad[ssnap1], color='g', fill=False, label='Half-mass radius: %s pc' %round(hmrad[ssnap1],5))
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

plt.legend(loc='upper left',frameon=False, title='Simulation: %s' %fname);

plt.show

#%% Plotting positions of stars from n-snapshot with m-number of massive stars and half-mass radius in y-z dimension

f2 = plt.figure(figsize=(7,7))
ax2 = f2.add_subplot(111)
ax2.scatter(df1.loc[ssnap1,'nrady'],df1.loc[ssnap1,'nradz'],s=2,c='black',marker='o',label='All stars in snapshot %d' %ssnap1)
ax2.scatter(df2['nrady'],df2['nradz'],s=25,c='red',marker='^',label='%d most massive stars in snapshot %d' %(nmass,ssnap1))
#To plot the non COD-corrected star positions, use the following:
#ax2.scatter(df1.loc[ssnap1,'rady'],df1.loc[ssnap1,'radz'],s=2,c='#999999',marker='o',label='nonCOD-stars %d' %ssnap1)
#ax2.scatter(mradx,mrady,s=5,c='blue',marker='s',label='COM')
circ2 = plt.Circle((0,0), radius=hmrad[ssnap1], color='g', fill=False, label='Half-mass radius: %s pc' %round(hmrad[ssnap1],5))
ax2.add_patch(circ2)

#To add scatter plots from a second snap shot:
#ax.scatter(df1.loc[ssnap2:ssnap2,'radx'],df1.loc[ssnap2:ssnap2,'rady'],s=5,c='green',marker='s',label='All stars in snapshot %d' %ssnap2)
#ax.scatter(df3['radx'],df3['rady'],s=25,c='purple',marker='^',label='5 most massive stars in snapshot %d' %ssnap2)

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

plt.legend(loc='upper left', frameon=False, title='Simulation: %s' %fname);

plt.show

