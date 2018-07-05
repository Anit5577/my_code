# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates the radial velocity dispersion for all snapshots of a set of simulation data. It then plots the virial velocity dispersion using the half-mass radius and the interquartile range


import pandas as pd
import numpy as np
import astropy.units as u
from astropy import constants as const
import statistics
import matplotlib.pyplot as plt
import F_COD_Radius_Nstars as CODRN
from function_file import virial_velocity_dispersion, velocity_dispersion, IQR_velocity_dispersion

fname = input('Choose data file to be read into array: ')
strucpar = 10
kms = u.km / u.s

df1 = pd.read_csv(fname, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velz':np.float64})

nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)

#The following bit passes the filename and the number of snaps and stars to the Fortran subroutine that calculates the COD and adjusts the radii by that COD.

nrad = CODRN.cod_radius(fname,nsnaps,nstars)


for ssnap in range(0,nsnaps):
    df1.loc[ssnap,'nradx'] = nrad[ssnap,0]
    df1.loc[ssnap,'nrady'] = nrad[ssnap,1]
    df1.loc[ssnap,'nradz'] = nrad[ssnap,2]


dflist=[df1]
dname= [fname]

#%% calculate velocity dispersion sigma

veldisp = []
for ssnap in range(0,nsnaps):
    veldisp.append(statistics.pstdev(df1.loc[ssnap,'velz']))
   
x = np.arange(0,10.1,0.1)
y = veldisp 

print (veldisp)


#%%

velzdisp = velocity_dispersion(dflist,dname,1)

print (velzdisp)

#%% virial sigma within Half-mass radius

#COD corrected half-mass radius:
radval = (np.sqrt(df1['nradx']**2+df1['nrady']**2+df1['nradz']**2))

virvelzdisp = []
for ssnap in range(0, nsnaps):
    summass=0
    hm=0
    cmass=0
    hmrad=0
    df2 = (df1.assign(rad=radval)).loc[ssnap].sort_values('rad')
    summass = df2['mass'].sum() *u.M_sun
    hm = (df2['mass'].sum())/2
    cmass = df2['mass'].cumsum()
    df3 = df2.assign(hmdif=np.abs(cmass-hm))
    hmrad = df3.loc[df3['hmdif'].idxmin(),'rad'] *u.pc
    virvelzdisp.append((np.sqrt((2*summass.to(u.kg)*const.G)/(strucpar*hmrad.to(u.m)))).to(kms))

print (virvelzdisp)

#%%

virveldisp = virial_velocity_dispersion(dflist,dname,1)
print (virveldisp)

#%% Interquartile range


halfsnap = int(nstars/2)

IQR = []
for ssnap in range(0,nsnaps):
    df1.reset_index(level=1)
    lowmedian = np.median(df1.loc[ssnap].sort_values('velz')[:halfsnap]['velz'])
    upmedian = np.median(df1.loc[ssnap].sort_values('velz')[halfsnap:nstars+1]['velz'])
    IQR.append(0.741*(upmedian-lowmedian))
    
print (IQR)    


#%%

IQR = IQR_velocity_dispersion(dflist,dname,1)

print (IQR)

#%% Plotting velocity dispersion values
        
f = plt.figure(figsize=(10,10)) 
ax = f.add_subplot(111)
ax.plot(x,y,linestyle='-',label=r'$\sigma$  all stars')
ax.plot(x,IQR,linestyle='--', label='IQR all stars')
ax.plot(x,virvelzdisp*kms,linestyle='-.',label=r'$\sigma_{vir}$ within $R_{hm}$')

ax.set_xlim(-0.1,10.1)
ax.set_ylim(0,3)

plt.setp(ax.get_xticklabels(),fontsize=10)
plt.setp(ax.get_yticklabels(),fontsize=10)

ax.set_xlabel('Time (Myr)',fontsize=12) 
ax.set_ylabel(r'$\sigma$ (km/s)',fontsize=12)

plt.legend(loc='upper left', frameon=False,title=fname)
plt.show
    

#%% Plotting cumulative distribution of radial velocities

star = np.arange(1,nstars+1,1)

f1 = plt.figure(figsize=(10,10))
ax1 = f1.add_subplot(111)

df0M = df1.loc[0].sort_values('velz')
df05M = df1.loc[5].sort_values('velz')
df10M = df1.loc[10].sort_values('velz')
df50M = df1.loc[50].sort_values('velz')

ax1.plot(df0M['velz'],star,linestyle='-',label='0 Myr')
ax1.plot(df05M['velz'],star,linestyle='--',label='0.5 Myr')
ax1.plot(df10M['velz'],star,linestyle='-.',label='1.0 Myr')
ax1.plot(df50M['velz'],star,linestyle=':', label='5.0 Myr')

plt.setp(ax1.get_xticklabels(),fontsize=10)
plt.setp(ax1.get_yticklabels(),fontsize=10)

ax1.set_xlabel('Radial velocity (km/s)',fontsize=12) 
ax1.set_ylabel(r'$N_{stars}$',fontsize=12)

plt.legend(loc='upper left',frameon=False,title=fname)

ax1.set_xlim(-5,5)
ax1.set_ylim(0,nstars)

plt.show

#%% Plotting histogram of radial velocities --

#f2 = plt.figure(figsize=(10,10))
#ax2 = f2.add_subplot(111)
#
#ax2.hist(df1.loc[0,'velz'],bins=[-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,-0,1,2,3,4,5,6,7,8,9,10],label='0 Myr')
#ax2.hist(df1.loc[5,'velz'],bins=[-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,-0,1,2,3,4,5,6,7,8,9,10],label='0.5 Myr')
#ax2.hist(df1.loc[10,'velz'],bins=[-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,-0,1,2,3,4,5,6,7,8,9,10],label='1 Myr')
#ax2.hist(df1.loc[50,'velz'],bins=[-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,-0,1,2,3,4,5,6,7,8,9,10],label='5 Myr')
#
#plt.yscale('log')
#
#ax2.set_xlabel('Radial velocity (km/s)',fontsize=12) 
#ax2.set_ylabel('$N_{stars}$',fontsize=12)
#
#plt.legend(loc='upper left',frameon=False,title=fname)


#%% velocity dispersion as a function of radius in bins of 100 stars with 10 bins
# this is a different code compared to the one found in 'Velocity dispersion by radius all snaps.py' and 
# only works for Nstars = 1000!!!!

dfradval = (df1.assign(rad=radval)).loc[0].sort_values('rad')

bins1 = statistics.pstdev(dfradval[:100]['velz'])
bins2 = statistics.pstdev(dfradval[100:200]['velz'])
bins3 = statistics.pstdev(dfradval[200:300]['velz'])
bins4 = statistics.pstdev(dfradval[300:400]['velz'])
bins5 = statistics.pstdev(dfradval[400:500]['velz'])
bins6 = statistics.pstdev(dfradval[500:600]['velz'])
bins7 = statistics.pstdev(dfradval[600:700]['velz'])
bins8 = statistics.pstdev(dfradval[700:800]['velz'])
bins9 = statistics.pstdev(dfradval[800:900]['velz'])
bins10 = statistics.pstdev(dfradval[900:1000]['velz'])


f3 = plt.figure(figsize=(10,10))
ax3 = f3.add_subplot(111)

ax3.scatter(dfradval[99:100]['rad'],bins1,c='b',marker='s', label='0 Myr')
ax3.scatter(dfradval[199:200]['rad'],bins2,c='b',marker='s')
ax3.scatter(dfradval[299:300]['rad'],bins3,c='b',marker='s')
ax3.scatter(dfradval[399:400]['rad'],bins4,c='b',marker='s')
ax3.scatter(dfradval[499:500]['rad'],bins5,c='b',marker='s')
ax3.scatter(dfradval[599:600]['rad'],bins6,c='b',marker='s')
ax3.scatter(dfradval[699:700]['rad'],bins7,c='b',marker='s')
ax3.scatter(dfradval[799:800]['rad'],bins8,c='b',marker='s')
ax3.scatter(dfradval[899:900]['rad'],bins9,c='b',marker='s')
ax3.scatter(dfradval[999:1000]['rad'],bins10,c='b',marker='s')

dfradval1 = (df1.assign(rad=radval)).loc[5].sort_values('rad')

bins11 = statistics.pstdev(dfradval1[:100]['velz'])
bins21 = statistics.pstdev(dfradval1[100:200]['velz'])
bins31 = statistics.pstdev(dfradval1[200:300]['velz'])
bins41 = statistics.pstdev(dfradval1[300:400]['velz'])
bins51 = statistics.pstdev(dfradval1[400:500]['velz'])
bins61 = statistics.pstdev(dfradval1[500:600]['velz'])
bins71 = statistics.pstdev(dfradval1[600:700]['velz'])
bins81 = statistics.pstdev(dfradval1[700:800]['velz'])
bins91 = statistics.pstdev(dfradval1[800:900]['velz'])
bins101 = statistics.pstdev(dfradval1[900:1000]['velz'])


ax3.scatter(dfradval1[99:100]['rad'],bins11,c='g',marker='^', label='0.5 Myr')
ax3.scatter(dfradval1[199:200]['rad'],bins21,c='g',marker='^')
ax3.scatter(dfradval1[299:300]['rad'],bins31,c='g',marker='^')
ax3.scatter(dfradval1[399:400]['rad'],bins41,c='g',marker='^')
ax3.scatter(dfradval1[499:500]['rad'],bins51,c='g',marker='^')
ax3.scatter(dfradval1[599:600]['rad'],bins61,c='g',marker='^')
ax3.scatter(dfradval1[699:700]['rad'],bins71,c='g',marker='^')
ax3.scatter(dfradval1[799:800]['rad'],bins81,c='g',marker='^')
ax3.scatter(dfradval1[899:900]['rad'],bins91,c='g',marker='^')
ax3.scatter(dfradval1[999:1000]['rad'],bins101,c='g',marker='^')


dfradval11 = (df1.assign(rad=radval)).loc[10].sort_values('rad')

bins111 = statistics.pstdev(dfradval11[:100]['velz'])
bins211 = statistics.pstdev(dfradval11[100:200]['velz'])
bins311 = statistics.pstdev(dfradval11[200:300]['velz'])
bins411 = statistics.pstdev(dfradval11[300:400]['velz'])
bins511 = statistics.pstdev(dfradval11[400:500]['velz'])
bins611 = statistics.pstdev(dfradval11[500:600]['velz'])
bins711 = statistics.pstdev(dfradval11[600:700]['velz'])
bins811 = statistics.pstdev(dfradval11[700:800]['velz'])
bins911 = statistics.pstdev(dfradval11[800:900]['velz'])
bins1011 = statistics.pstdev(dfradval11[900:1000]['velz'])


ax3.scatter(dfradval11[99:100]['rad'],bins111,c='r',marker='o', label ='1 Myr')
ax3.scatter(dfradval11[199:200]['rad'],bins211,c='r',marker='o')
ax3.scatter(dfradval11[299:300]['rad'],bins311,c='r',marker='o')
ax3.scatter(dfradval11[399:400]['rad'],bins411,c='r',marker='o')
ax3.scatter(dfradval11[499:500]['rad'],bins511,c='r',marker='o')
ax3.scatter(dfradval11[599:600]['rad'],bins611,c='r',marker='o')
ax3.scatter(dfradval11[699:700]['rad'],bins711,c='r',marker='o')
ax3.scatter(dfradval11[799:800]['rad'],bins811,c='r',marker='o')
ax3.scatter(dfradval11[899:900]['rad'],bins911,c='r',marker='o')
ax3.scatter(dfradval11[999:1000]['rad'],bins1011,c='r',marker='o')


dfradval111 = (df1.assign(rad=radval)).loc[50].sort_values('rad')

bins1111 = statistics.pstdev(dfradval111[:100]['velz'])
bins2111 = statistics.pstdev(dfradval111[100:200]['velz'])
bins3111 = statistics.pstdev(dfradval111[200:300]['velz'])
bins4111 = statistics.pstdev(dfradval111[300:400]['velz'])
bins5111 = statistics.pstdev(dfradval111[400:500]['velz'])
bins6111 = statistics.pstdev(dfradval111[500:600]['velz'])
bins7111 = statistics.pstdev(dfradval111[600:700]['velz'])
bins8111 = statistics.pstdev(dfradval111[700:800]['velz'])
bins9111 = statistics.pstdev(dfradval111[800:900]['velz'])
bins10111 = statistics.pstdev(dfradval111[900:1000]['velz'])


ax3.scatter(dfradval111[99:100]['rad'],bins1111,c='y',marker='x', label ='5 Myr')
ax3.scatter(dfradval111[199:200]['rad'],bins2111,c='y',marker='x')
ax3.scatter(dfradval111[299:300]['rad'],bins3111,c='y',marker='x')
ax3.scatter(dfradval111[399:400]['rad'],bins4111,c='y',marker='x')
ax3.scatter(dfradval111[499:500]['rad'],bins5111,c='y',marker='x')
ax3.scatter(dfradval111[599:600]['rad'],bins6111,c='y',marker='x')
ax3.scatter(dfradval111[699:700]['rad'],bins7111,c='y',marker='x')
ax3.scatter(dfradval111[799:800]['rad'],bins8111,c='y',marker='x')
ax3.scatter(dfradval111[899:900]['rad'],bins9111,c='y',marker='x')
ax3.scatter(dfradval111[999:1000]['rad'],bins10111,c='y',marker='x')


ax3.set_ylim(0,3)

plt.xscale('log')

ax3.set_ylabel(r'$\sigma$ (km/s)',fontsize=12) 
ax3.set_xlabel('Distance from centre (pc)',fontsize=12)

#plt.legend(loc='upper left',frameon=False,title='no COD-correction %s' %fname)
plt.legend(loc='upper left',frameon=False,title='COD-correction %s' %fname)

plt.show