# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# This code calculates the radial velocity dispersion as a function of radius and focuses on the half-mass radius and 2x half-mass radius.


import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
import F_COD_Radius_Nstars as CODRN

fname = input('Choose data file to be read into array: ')

df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velz':np.float64})

# number of snaps is fixed for simulations, number of stars is calculated by dividing the total number of rows by the number of snaps, this will make it easier to react to different number of stars, but needs to be tested, when differen Nstars are used.

nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)
strucpar = 10

#The following bit passes the filename and the number of snaps and stars to the Fortran subroutine that calculates the COD and adjusts the radii by that COD.

nrad = CODRN.cod_radius(fname,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[ssnap,'nradx'] = nrad[ssnap,0]
    df1.loc[ssnap,'nrady'] = nrad[ssnap,1]
    df1.loc[ssnap,'nradz'] = nrad[ssnap,2]


#original half-mass radius:
#radval = (np.sqrt(df1['radx']**2+df1['rady']**2+df1['radz']**2))

#calculating the COD-corrected half-mass radius using the scalar of the radius.
    
radval = (np.sqrt(df1['nradx']**2+df1['nrady']**2+df1['nradz']**2))

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

#%% velocity dispersion as a function of radius in bins of 100 stars with 10 bins

snaplist = [0,5,10,50]

f = plt.figure(figsize=(10,10))
ax = f.add_subplot(111)
   
ax.set_ylabel(r'Radial velocity $\sigma$ (km/s)',fontsize=12) 
ax.set_xlabel('Distance from centre (pc)',fontsize=12)

ax.set_ylim(0,3) 
plt.xscale('log')

for locsnap in snaplist:
    
    if locsnap == 0:
        scattercolour ='b'
        markertype ='.'
        hmradmarker = 's'
        dhmradmarker = 'D'
    elif locsnap == 5:
        scattercolour = 'g'
        markertype ='+'
        hmradmarker = 's'
        dhmradmarker = 'D'
    elif locsnap == 10:
        scattercolour = 'r'
        markertype ='*'
        hmradmarker = 's'
        dhmradmarker = 'D'
    elif locsnap == 50:
        scattercolour = 'y'
        markertype ='x' 
        hmradmarker = 's'
        dhmradmarker = 'D'
    
    dfradval = (df1.assign(rad=radval)).loc[locsnap].sort_values('rad')
        
    
# finding the star id, where the hmrad equals dfradval.    
    hmstar = dfradval.loc[dfradval['rad'] == hmrad[locsnap]].index[0]    
    
    dhm = hmrad[locsnap] + hmrad[locsnap]
     
    dhmvelz = dfradval.loc[dfradval['rad'] <= dhm]['velz']
    
# To calculate the velocity dispersion of the radial velocity up to the half-mass radius     
    hmvelzdisp = statistics.pstdev(dfradval.loc[:hmstar]['velz'])
    
# To calculate the velocity dispersion of the radial velocity up to double the half-mass radius
    dhmvelzdisp= statistics.pstdev(dhmvelz)    
    
#%%    
    
    bins1 = statistics.pstdev(dfradval[:int(nstars*0.1)]['velz'])
    bins2 = statistics.pstdev(dfradval[int(nstars*0.1):int(nstars*0.2)]['velz'])
    bins3 = statistics.pstdev(dfradval[int(nstars*0.2):int(nstars*0.3)]['velz'])
    bins4 = statistics.pstdev(dfradval[int(nstars*0.3):int(nstars*0.4)]['velz'])
    bins5 = statistics.pstdev(dfradval[int(nstars*0.4):int(nstars*0.5)]['velz'])
    bins6 = statistics.pstdev(dfradval[int(nstars*0.5):int(nstars*0.6)]['velz'])
    bins7 = statistics.pstdev(dfradval[int(nstars*0.6):int(nstars*0.7)]['velz'])
    bins8 = statistics.pstdev(dfradval[int(nstars*0.7):int(nstars*0.8)]['velz'])
    bins9 = statistics.pstdev(dfradval[int(nstars*0.8):int(nstars*0.9)]['velz'])
        
    ax.scatter(dfradval[int(nstars*0.1-1):int(nstars*0.1)]['rad'],bins1,c=scattercolour, marker=markertype, label='%s Myr' %(locsnap/10))
    ax.scatter(dfradval[int(nstars*0.2-1):int(nstars*0.2)]['rad'],bins2,c=scattercolour, marker=markertype)
    ax.scatter(dfradval[int(nstars*0.3-1):int(nstars*0.3)]['rad'],bins3,c=scattercolour, marker=markertype)
    ax.scatter(dfradval[int(nstars*0.4-1):int(nstars*0.4)]['rad'],bins4,c=scattercolour, marker=markertype)
    ax.scatter(dfradval[int(nstars*0.5-1):int(nstars*0.5)]['rad'],bins5,c=scattercolour, marker=markertype)
    ax.scatter(dfradval[int(nstars*0.6-1):int(nstars*0.6)]['rad'],bins6,c=scattercolour, marker=markertype)
    ax.scatter(dfradval[int(nstars*0.7-1):int(nstars*0.7)]['rad'],bins7,c=scattercolour, marker=markertype)
    ax.scatter(dfradval[int(nstars*0.8-1):int(nstars*0.8)]['rad'],bins8,c=scattercolour, marker=markertype)
    ax.scatter(dfradval[int(nstars*0.9-1):int(nstars*0.9)]['rad'],bins9,c=scattercolour, marker=markertype)
    
# this last 2 lines plots a point each for the velocity dispersion of the velocities within the halfmass radius and double half-mass radius     
    ax.scatter(hmrad[locsnap],hmvelzdisp,c=scattercolour, marker=hmradmarker, label='at $R_{hm}$')
    ax.scatter(dhm,dhmvelzdisp,c=scattercolour, marker=dhmradmarker, label='at 2x $R_{hm}$')
    
#plt.legend(loc='upper left',frameon=False,title='no COD-correction %s' %fname)
plt.legend(loc='upper left',frameon=False, ncol=2, title='%s' %(fname))

plt.show()

#plt.savefig('Velocity_dispersion_radius_%s.png' %fname)