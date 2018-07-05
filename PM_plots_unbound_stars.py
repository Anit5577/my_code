# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.ticker import AutoMinorLocator
import F_Transverse_Velocity_final as TV
#import F_COD_Radius_Nstars as CODRN #turn this on, if COD-correction is required.
import F_BUS_ENERGY as BUS 

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



 
#for file 1

#nrad1 = CODRN.cod_radius(d['fname1'],nsnaps,nstars)
#
#for ssnap in range(0,nsnaps):
#    df1.loc[ssnap,'nradx'] = nrad1[ssnap,0]
#    df1.loc[ssnap,'nrady'] = nrad1[ssnap,1]
#    df1.loc[ssnap,'nradz'] = nrad1[ssnap,2]
#
#radval1=(np.sqrt(df1['nradx']**2+df1['nrady']**2+df1['nradz']**2))
#
#hmrad1 =[]
#nrad = 0
#for ssnap in range(0, nsnaps):  
#    summass=0
#    hm=0
#    cmass=0
#    hmdif=0
#    df12 = (df1.assign(nrad=radval1)).loc[ssnap].sort_values('nrad')
#    summass = df12['mass'].sum()
#    hm = (df12['mass'].sum())/2
#    cmass = df12['mass'].cumsum()
#    df13 = df12.assign(hmdif=np.abs(cmass-hm))
#    hmrad1.append(df13.loc[df13['hmdif'].idxmin(),'nrad'])      

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel1 = TV.transverse_velocity(d['fname1'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[0,'xdist'] = 0
    df1.loc[0,'ydist'] = 0  
    df1.loc[ssnap,'xdist'] = transvel1[ssnap,0]
    df1.loc[ssnap,'ydist'] = transvel1[ssnap,1]  
    
df1['PM-vel'] = (np.sqrt(df1['xdist']**2.+df1['ydist']**2.))


energy1 = BUS.bound_unbound_stars(d['fname1'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[ssnap,'energy'] = energy1[ssnap]


# for file 2

#nrad2 = CODRN.cod_radius(d['fname2'],nsnaps,nstars)
#
#for ssnap in range(0,nsnaps):
#    df2.loc[ssnap,'nradx'] = nrad2[ssnap,0]
#    df2.loc[ssnap,'nrady'] = nrad2[ssnap,1]
#    df2.loc[ssnap,'nradz'] = nrad2[ssnap,2]
#
#radval2=(np.sqrt(df2['nradx']**2+df2['nrady']**2+df2['nradz']**2))
#
#hmrad2 =[]
#nrad=0
#for ssnap in range(0, nsnaps):  
#    summass=0
#    hm=0
#    cmass=0
#    hmdif=0
#    df22 = (df2.assign(nrad=radval2)).loc[ssnap].sort_values('nrad')
#    summass = df22['mass'].sum()
#    hm = (df22['mass'].sum())/2
#    cmass = df22['mass'].cumsum()
#    df23 = df22.assign(hmdif=np.abs(cmass-hm))
#    hmrad2.append(df23.loc[df23['hmdif'].idxmin(),'nrad'])      

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel2 = TV.transverse_velocity(d['fname2'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df2.loc[0,'xdist'] = 0
    df2.loc[0,'ydist'] = 0  
    df2.loc[ssnap,'xdist'] = transvel2[ssnap,0]
    df2.loc[ssnap,'ydist'] = transvel2[ssnap,1]  
    

df2['PM-vel'] = (np.sqrt(df2['xdist']**2.+df2['ydist']**2.))

energy2 = BUS.bound_unbound_stars(d['fname2'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df2.loc[ssnap,'energy'] = energy2[ssnap]


#for file 3

#nrad3 = CODRN.cod_radius(d['fname3'],nsnaps,nstars)
#
#for ssnap in range(0,nsnaps):
#    df3.loc[ssnap,'nradx'] = nrad3[ssnap,0]
#    df3.loc[ssnap,'nrady'] = nrad3[ssnap,1]
#    df3.loc[ssnap,'nradz'] = nrad3[ssnap,2]
#
#radval3=(np.sqrt(df3['nradx']**2+df3['nrady']**2+df3['nradz']**2))
#
#hmrad3 =[]
#nrad=0
#for ssnap in range(0, nsnaps):  
#    summass=0
#    hm=0
#    cmass=0
#    hmdif=0
#    df32 = (df3.assign(nrad=radval3)).loc[ssnap].sort_values('nrad')
#    summass = df32['mass'].sum()
#    hm = (df32['mass'].sum())/2
#    cmass = df32['mass'].cumsum()
#    df33 = df32.assign(hmdif=np.abs(cmass-hm))
#    hmrad3.append(df33.loc[df33['hmdif'].idxmin(),'nrad'])      


#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel3 = TV.transverse_velocity(d['fname3'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df3.loc[0,'xdist'] = 0
    df3.loc[0,'ydist'] = 0  
    df3.loc[ssnap,'xdist'] = transvel3[ssnap,0]
    df3.loc[ssnap,'ydist'] = transvel3[ssnap,1]  


df3['PM-vel'] = (np.sqrt(df3['xdist']**2.+df3['ydist']**2.))

energy3 = BUS.bound_unbound_stars(d['fname3'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df3.loc[ssnap,'energy'] = energy3[ssnap]


# for file 4

#nrad4 = CODRN.cod_radius(d['fname4'],nsnaps,nstars)
#
#for ssnap in range(0,nsnaps):
#    df4.loc[ssnap,'nradx'] = nrad4[ssnap,0]
#    df4.loc[ssnap,'nrady'] = nrad4[ssnap,1]
#    df4.loc[ssnap,'nradz'] = nrad4[ssnap,2]
#
#radval4=(np.sqrt(df4['nradx']**2+df4['nrady']**2+df4['nradz']**2))
#
#hmrad4 =[]
#nrad=0
#for ssnap in range(0, nsnaps):  
#    summass=0
#    hm=0
#    cmass=0
#    hmdif=0
#    df42 = (df4.assign(nrad=radval4)).loc[ssnap].sort_values('nrad')
#    summass = df42['mass'].sum()
#    hm = (df42['mass'].sum())/2
#    cmass = df42['mass'].cumsum()
#    df43 = df42.assign(hmdif=np.abs(cmass-hm))
#    hmrad4.append(df43.loc[df43['hmdif'].idxmin(),'nrad'])      

#Alternatively this can be calculated in Fortran and then imported to Python, which is faster
        
transvel4 = TV.transverse_velocity(d['fname4'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df4.loc[0,'xdist'] = 0
    df4.loc[0,'ydist'] = 0  
    df4.loc[ssnap,'xdist'] = transvel4[ssnap,0]
    df4.loc[ssnap,'ydist'] = transvel4[ssnap,1]

df4['PM-vel'] = (np.sqrt(df4['xdist']**2.+df4['ydist']**2.))

energy4 = BUS.bound_unbound_stars(d['fname4'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df4.loc[ssnap,'energy'] = energy4[ssnap]


# all columns are extracted for values of nrad that are within/equal 2 times halfmass-radius or wihout/equal 2 times halfmass-radius

#%%
    
df1UB = (df1.loc[df1['energy'] >= 0])
df1B = (df1.loc[df1['energy'] < 0])

df2UB = (df2.loc[df2['energy'] >= 0])
df2B = (df2.loc[df2['energy'] < 0])

df3UB = (df3.loc[df3['energy'] >= 0])
df3B = (df3.loc[df3['energy'] < 0])

df4UB = (df4.loc[df4['energy'] >= 0])
df4B = (df4.loc[df4['energy'] < 0])


#%% Plotting mass against velocity for stars inside and outside the cluster

fnamelist =[d['fname1'],d['fname2'],d['fname3'],d['fname4']]
    
fig2, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(15.,50.))
plt.subplots_adjust(wspace=0.2)
#x_minor_locator = AutoMinorLocator(2)
#y_minor_locator = AutoMinorLocator(4)

legend =[]

for fname in fnamelist:
    
    if fname[21] == 'E':
       if fname[17] == 'X':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, stellar evolution')
       elif fname[5:7] == '2r':
           legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, stellar evolution')

    if fname[21] == 'S':
       if fname[17] == 'X':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution' %(fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, no evolution')
       elif fname[5:7] == '2r':
           legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, no evolution')


    legend.append(legendtitle)


ax1.plot(421)
ax1.scatter(df1UB.loc[50,'PM-vel'],df1UB.loc[50,'mass'],c='b',s=2,label='Unbound stars at 5 Myr: %s stars, sim: %s' %(df1UB.loc[50].index.size,d['fname1'][25:27]))
ax1.legend(loc='upper right', title=legend[0])  


ax2.plot(422)
ax2.scatter(df2UB.loc[50,'PM-vel'],df2UB.loc[50,'mass'],c='g',s=2,label='Unbound stars at 5 Myr: %s stars, sim: %s' %(df2UB.loc[50].index.size,d['fname2'][25:27]))
ax2.legend(loc='upper right', title=legend[1])


ax3.plot(423)
ax3.scatter(df3UB.loc[50,'PM-vel'],df3UB.loc[50,'mass'],c='r',s=2,label='Unbound stars at 5 Myr: %s stars, sim: %s' %(df3UB.loc[50].index.size,d['fname3'][25:27]))
ax3.legend(loc='upper right', title=legend[2])  

ax4.plot(424)
ax4.scatter(df4UB.loc[50,'PM-vel'],df4UB.loc[50,'mass'],c='orange',s=2,label='Unbound stars at 5 Myr: %s stars, sim: %s' %(df4UB.loc[50].index.size,d['fname4'][25:27]))
ax4.legend(loc='upper right', title=legend[3])  


axes = [ax1,ax2,ax3,ax4]

for i in axes:
#    i.xaxis.set_minor_locator(x_minor_locator)
#    i.yaxis.set_minor_locator(y_minor_locator)
    i.tick_params(which='both',direction='in',top='on',right='on')
#    i.xaxis.set_major_locator(MaxNLocator(integer=True))
    i.set_xlim(left=0)
    i.set_ylim(0,30)


ax1.set_ylabel('Mass (in solar mass)',fontsize=10.) 
ax3.set_ylabel('Mass (in solar mass)',fontsize=10.)
ax3.set_xlabel('Proper motion (km/s)',fontsize=10.)
ax4.set_xlabel('Proper motion (km/s)',fontsize=10.)
    
plt.show()


#plt.savefig('PM_velocity_escaped_%s.png' %legendtitle)

#%%


