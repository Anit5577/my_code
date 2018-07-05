# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import F_Transverse_Velocity_final as TV
import F_COD_Radius_Nstars as CODRN  #turn this on, if COD-correction is required.

f = open('file.txt')
lines = [line.rstrip('\n') for line in open('file.txt')]

nlines = len(lines)

d={}
for x in range (1,nlines+1,1):
    d['fname{0}'.format(x)]=lines[x-1]

f.close()      

df1 = pd.read_csv(d['fname1'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df2 = pd.read_csv(d['fname2'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df3 = pd.read_csv(d['fname3'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df4 = pd.read_csv(d['fname4'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)

# Calculating CoD for file chosen in line 8 as filename and correcting for all radii for the shift in COD; results in an array cod(i,1:3) with i representing the snapshot and the 1:3 the three vector components -> to call the values for each dimension:
# x: cod[i,0], y: cod[i,1] and z: cod[i,2]


#%%
 
#for file 1

nrad1 = CODRN.cod_radius(d['fname1'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[ssnap,'nradx'] = nrad1[ssnap,0]
    df1.loc[ssnap,'nrady'] = nrad1[ssnap,1]
    df1.loc[ssnap,'nradz'] = nrad1[ssnap,2]

radval=(np.sqrt(df1['nradx']**2+df1['nrady']**2+df1['nradz']**2))

hmrad1 =[]
for ssnap in range(0, nsnaps):  
    summass=0
    hm=0
    cmass=0
    hmdif=0
    df12 = (df1.assign(nrad=radval)).loc[ssnap].sort_values('nrad')
    summass = df12['mass'].sum()
    hm = (df12['mass'].sum())/2
    cmass = df12['mass'].cumsum()
    df13 = df12.assign(hmdif=np.abs(cmass-hm))
    hmrad1.append(df13.loc[df13['hmdif'].idxmin(),'nrad'])      

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel1 = TV.transverse_velocity(d['fname1'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[0,'xdist'] = 0
    df1.loc[0,'ydist'] = 0  
    df1.loc[ssnap,'xdist'] = transvel1[ssnap,0]
    df1.loc[ssnap,'ydist'] = transvel1[ssnap,1]  
    
df1['PM-vel'] = (np.sqrt(df1['xdist']**2.+df1['ydist']**2.))

# for file 2

nrad2 = CODRN.cod_radius(d['fname2'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df2.loc[ssnap,'nradx'] = nrad2[ssnap,0]
    df2.loc[ssnap,'nrady'] = nrad2[ssnap,1]
    df2.loc[ssnap,'nradz'] = nrad2[ssnap,2]

radval=(np.sqrt(df2['nradx']**2+df2['nrady']**2+df2['nradz']**2))

hmrad2 =[]
for ssnap in range(0, nsnaps):  
    summass=0
    hm=0
    cmass=0
    hmdif=0
    df22 = (df2.assign(nrad=radval)).loc[ssnap].sort_values('nrad')
    summass = df22['mass'].sum()
    hm = (df22['mass'].sum())/2
    cmass = df22['mass'].cumsum()
    df23 = df22.assign(hmdif=np.abs(cmass-hm))
    hmrad2.append(df23.loc[df23['hmdif'].idxmin(),'nrad'])      

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel2 = TV.transverse_velocity(d['fname2'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df2.loc[0,'xdist'] = 0
    df2.loc[0,'ydist'] = 0  
    df2.loc[ssnap,'xdist'] = transvel2[ssnap,0]
    df2.loc[ssnap,'ydist'] = transvel2[ssnap,1]  
    

df2['PM-vel'] = (np.sqrt(df2['xdist']**2.+df2['ydist']**2.))

#for file 3

nrad3 = CODRN.cod_radius(d['fname3'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df3.loc[ssnap,'nradx'] = nrad3[ssnap,0]
    df3.loc[ssnap,'nrady'] = nrad3[ssnap,1]
    df3.loc[ssnap,'nradz'] = nrad3[ssnap,2]

radval=(np.sqrt(df3['nradx']**2+df3['nrady']**2+df3['nradz']**2))

hmrad3 =[]
for ssnap in range(0, nsnaps):  
    summass=0
    hm=0
    cmass=0
    hmdif=0
    df32 = (df3.assign(nrad=radval)).loc[ssnap].sort_values('nrad')
    summass = df32['mass'].sum()
    hm = (df32['mass'].sum())/2
    cmass = df32['mass'].cumsum()
    df33 = df32.assign(hmdif=np.abs(cmass-hm))
    hmrad3.append(df33.loc[df33['hmdif'].idxmin(),'nrad'])      

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel3 = TV.transverse_velocity(d['fname3'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df3.loc[0,'xdist'] = 0
    df3.loc[0,'ydist'] = 0  
    df3.loc[ssnap,'xdist'] = transvel3[ssnap,0]
    df3.loc[ssnap,'ydist'] = transvel3[ssnap,1]  


df3['PM-vel'] = (np.sqrt(df3['xdist']**2.+df3['ydist']**2.))

# for file 4

nrad4 = CODRN.cod_radius(d['fname4'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df4.loc[ssnap,'nradx'] = nrad4[ssnap,0]
    df4.loc[ssnap,'nrady'] = nrad4[ssnap,1]
    df4.loc[ssnap,'nradz'] = nrad4[ssnap,2]

radval=(np.sqrt(df4['nradx']**2+df4['nrady']**2+df4['nradz']**2))

hmrad4 =[]
for ssnap in range(0, nsnaps):  
    summass=0
    hm=0
    cmass=0
    hmdif=0
    df42 = (df4.assign(nrad=radval)).loc[ssnap].sort_values('nrad')
    summass = df42['mass'].sum()
    hm = (df42['mass'].sum())/2
    cmass = df42['mass'].cumsum()
    df43 = df42.assign(hmdif=np.abs(cmass-hm))
    hmrad4.append(df43.loc[df43['hmdif'].idxmin(),'nrad'])      

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel4 = TV.transverse_velocity(d['fname4'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df4.loc[0,'xdist'] = 0
    df4.loc[0,'ydist'] = 0  
    df4.loc[ssnap,'xdist'] = transvel4[ssnap,0]
    df4.loc[ssnap,'ydist'] = transvel4[ssnap,1]

df4['PM-vel'] = (np.sqrt(df4['xdist']**2.+df3['ydist']**2.))

# all columns are extracted for values of nrad that are within/equal 2 times halfmass-radius or wihout/equal 2 times halfmass-radius

df1 = df1.assign(nrad=radval).loc[50].sort_values('nrad')
df1PMi = (df1.loc[df1['nrad'] <= (hmrad1[50]*2)])
df1PMo = (df1.loc[df1['nrad'] >= (hmrad1[50]*2)])

df2 = df2.assign(nrad=radval).loc[50].sort_values('nrad')
df2PMi = (df2.loc[df2['nrad'] <= (hmrad2[50]*2)])
df2PMo = (df2.loc[df2['nrad'] >= (hmrad2[50]*2)])

df3 = df3.assign(nrad=radval).loc[50].sort_values('nrad')
df3PMi = (df3.loc[df3['nrad'] <= (hmrad3[50]*2)])
df3PMo = (df3.loc[df3['nrad'] >= (hmrad3[50]*2)])

df4 = df4.assign(nrad=radval).loc[50].sort_values('nrad')
df4PMi = (df4.loc[df4['nrad'] <= (hmrad4[50]*2)])
df4PMo = (df4.loc[df4['nrad'] >= (hmrad4[50]*2)])
        
#%% Plotting cumulative distribution of proper motion of stars located inside and outside of 2 x HMR for 4 snapshots
#
#from matplotlib.ticker import MaxNLocator

fnamelist =[d['fname1'],d['fname2'],d['fname3'],d['fname4']]
    
fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(15.,15.))
plt.subplots_adjust(wspace=0.2)
x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

legend =[]

for fname in fnamelist:

    if fname[17] == 'X':
        legendtitle = (r'N=1000, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
    elif fname[17] == '5':
        legendtitle = (r'N=500, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
    elif fname[17] == '2':    
        legendtitle = (r'N=2000, D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
    elif fname[5:7] == '1r':
        legendtitle = (r'N=1000, D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, sim=%s' %fname[25:27])
    elif fname[5:7] == '2r':
        legendtitle = (r'N=1000, D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, sim=%s' %fname[25:27])

    legend.append(legendtitle)

ax1.plot(221)
ax1.plot(df1PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df1PMi.index.size+1,1) ,c='b',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars' %df1PMi.index.size)
ax1.plot(df1PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df1PMo.index.size+1,1) ,c='b',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars' %df1PMo.index.size)
ax1.legend(loc='lower right', frameon=False, title=legend[0])  

ax2.plot(222)
ax2.plot(df2PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df2PMi.index.size+1,1) ,c='g',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars' %df2PMi.index.size)
ax2.plot(df2PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df2PMo.index.size+1,1) ,c='g',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars' %df2PMo.index.size)
ax2.legend(loc='lower right', frameon=False, title=legend[1])  

ax3.plot(223)
ax3.plot(df3PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df3PMi.index.size+1,1) ,c='r',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars' %df3PMi.index.size)
ax3.plot(df3PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df3PMo.index.size+1,1) ,c='r',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars' %df3PMo.index.size)
ax3.legend(loc='lower right', frameon=False, title=legend[2])  

ax4.plot(224)
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

#plt.savefig('Cumulative velocity %s.png' %fname)

#%%

fnamelist =[d['fname1'],d['fname2'],d['fname3'],d['fname4']]
    
fig1, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15.,15.), sharex=True)
plt.subplots_adjust(wspace=0.2)
x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

legend =[]

for fname in fnamelist:

    if fname[17] == 'X':
        legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
    elif fname[17] == '5':
        legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
    elif fname[17] == '2':    
        legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
    elif fname[5:7] == '1r':
        legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc')
    elif fname[5:7] == '2r':
        legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc')

    legend.append(legendtitle)

ax1.plot(121)
ax1.plot(df1PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df1PMi.index.size+1,1) ,c='b',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars, sim: %s' %(df1PMi.index.size,d['fname1'][25:27]))
ax1.plot(df2PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df2PMi.index.size+1,1) ,c='g',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars, sim: %s' %(df2PMi.index.size,d['fname2'][25:27]))
ax1.plot(df3PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df3PMi.index.size+1,1) ,c='r',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars, sim: %s' %(df3PMi.index.size,d['fname3'][25:27]))
ax1.plot(df4PMi.sort_values('PM-vel')['PM-vel'],np.arange(1,df4PMi.index.size+1,1) ,c='orange',linestyle='-',label='Inside 2x HMR at 5 Myr: %s stars, sim: %s' %(df4PMi.index.size,d['fname4'][25:27]))
ax1.legend(loc='lower right', frameon=False, title=legend[0])  

ax2.plot(122)
ax2.plot(df1PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df1PMo.index.size+1,1) ,c='b',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars, sim: %s' %(df1PMi.index.size,d['fname1'][25:27]))
ax2.plot(df2PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df2PMo.index.size+1,1) ,c='g',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars, sim: %s' %(df2PMi.index.size,d['fname2'][25:27]))
ax2.plot(df3PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df3PMo.index.size+1,1) ,c='red',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars, sim: %s' %(df3PMi.index.size,d['fname3'][25:27]))
ax2.plot(df4PMo.sort_values('PM-vel')['PM-vel'],np.arange(1,df4PMo.index.size+1,1) ,c='orange',linestyle=':',label='Outside 2x HMR at 5 Myr: %s stars, sim: %s' %(df4PMi.index.size,d['fname4'][25:27]))
ax2.legend(loc='lower right', frameon=False, title=legend[1])  

axes = [ax1,ax2]

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

fnamelist =[d['fname1'],d['fname2'],d['fname3'],d['fname4']]
    
fig2, ((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8)) = plt.subplots(nrows=4, ncols=2, figsize=(15.,50.))
plt.subplots_adjust(wspace=0.2)
x_minor_locator = AutoMinorLocator(2)
#y_minor_locator = AutoMinorLocator(4)

legend =[]

for fname in fnamelist:

    if fname[17] == 'X':
        legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
    elif fname[17] == '5':
        legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
    elif fname[17] == '2':    
        legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
    elif fname[5:7] == '1r':
        legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc')
    elif fname[5:7] == '2r':
        legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc')

    legend.append(legendtitle)

ax1.plot(421)
ax1.scatter(df1PMi.sort_values('PM-vel')['PM-vel'],df1PMi.sort_values('PM-vel')['mass'],c='b',s=2,label='Inside 2x HMR at 5 Myr: %s stars, sim: %s' %(df1PMi.index.size,d['fname1'][25:27]))
ax1.legend(loc='bottom', title =legend[0])  

ax2.plot(422)
ax2.scatter(df1PMo.sort_values('PM-vel')['PM-vel'],df1PMo.sort_values('PM-vel')['mass'],c='b',s=2,label='Outside 2x HMR at 5 Myr: %s stars, sim: %s' %(df1PMo.index.size,d['fname1'][25:27]))
ax2.legend(loc='top right', title=legend[0])  

ax3.plot(423)
ax3.scatter(df2PMi.sort_values('PM-vel')['PM-vel'],df2PMi.sort_values('PM-vel')['mass'],c='g',s=2, label='Inside 2x HMR at 5 Myr: %s stars, sim: %s' %(df2PMi.index.size,d['fname2'][25:27]))
ax3.legend(loc='top right', title=legend[1])

ax4.plot(424)
ax4.scatter(df2PMo.sort_values('PM-vel')['PM-vel'],df2PMo.sort_values('PM-vel')['mass'],c='g',s=2,label='Outside 2x HMR at 5 Myr: %s stars, sim: %s' %(df2PMo.index.size,d['fname2'][25:27]))
ax4.legend(loc='top right', title=legend[1])

ax5.plot(425)
ax5.scatter(df3PMi.sort_values('PM-vel')['PM-vel'],df3PMi.sort_values('PM-vel')['mass'],c='r',s=2,label='Inside 2x HMR at 5 Myr: %s stars, sim: %s' %(df3PMi.index.size,d['fname3'][25:27]))
ax5.legend(loc='top right', title=legend[2])

ax6.plot(426)
ax6.scatter(df3PMo.sort_values('PM-vel')['PM-vel'],df3PMo.sort_values('PM-vel')['mass'],c='r',s=2,label='Outside 2x HMR at 5 Myr: %s stars, sim: %s' %(df3PMo.index.size,d['fname3'][25:27]))
ax6.legend(loc='top right', title=legend[2])  

ax7.plot(427)
ax7.scatter(df4PMi.sort_values('PM-vel')['PM-vel'],df4PMi.sort_values('PM-vel')['mass'],c='orange',s=2,label='Inside 2x HMR at 5 Myr: %s stars, sim: %s' %(df4PMi.index.size,d['fname4'][25:27]))
ax7.legend(loc='top right', title=legend[3])  

ax8.plot(428)
ax8.scatter(df4PMo.sort_values('PM-vel')['PM-vel'],df4PMo.sort_values('PM-vel')['mass'],c='orange',s=2,label='Outside 2x HMR at 5 Myr: %s stars, sim: %s' %(df4PMo.index.size,d['fname4'][25:27]))
ax8.legend(loc='top right', title=legend[3])  


axes = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]

for i in axes:
    i.xaxis.set_minor_locator(x_minor_locator)
    i.yaxis.set_minor_locator(y_minor_locator)
    i.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))
    i.set_xlim(left=0)
    i.set_ylim(0,40)

ax1.set_ylabel('Mass (in solar mass)',fontsize=10.) 
ax3.set_ylabel('Mass (in solar mass)',fontsize=10.)
ax5.set_ylabel('Mass (in solar mass)',fontsize=10.)
ax7.set_ylabel('Mass (in solar mass)',fontsize=10.)
ax7.set_xlabel('Proper motion (km/s)',fontsize=10.)
ax8.set_xlabel('Proper motion (km/s)',fontsize=10.)
    
plt.show()