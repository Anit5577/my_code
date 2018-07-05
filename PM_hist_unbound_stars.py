# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import F_Transverse_Velocity_final as TV
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



##%%
#    
#df1UB = (df1.loc[df1['energy'] >= 0])
#df1B = (df1.loc[df1['energy'] < 0])
#
#df2UB = (df2.loc[df2['energy'] >= 0])
#df2B = (df2.loc[df2['energy'] < 0])
#
#df3UB = (df3.loc[df3['energy'] >= 0])
#df3B = (df3.loc[df3['energy'] < 0])
#
#df4UB = (df4.loc[df4['energy'] >= 0])
#df4B = (df4.loc[df4['energy'] < 0])



dflist = [df1,df2,df3,df4]

for file in dflist:
    HMall = (file.loc[file['mass']>=8])
    HMUB = ((file.loc[file['energy'] >= 0]).loc[(file.loc[file['energy'] >= 0])['mass'] >= 8])
#    HMB = ((file.loc[file['energy'] < 0]).loc[(file.loc[file['energy'] < 0])['mass'] >= 8])
    file.HMUBfraction = (HMUB.loc[50].index.size)/(HMall.loc[50].index.size)
#    IMall = (file.loc[file['mass'])
#    IMUB = ((file.loc[file['energy'] >= 0]).loc[(file.loc[file['energy'] >= 0])['mass']< 8])
##   IMB = ((file.loc[file['energy'] < 0]).loc[(file.loc[file['energy'] < 0])['mass'] < 8])
#    file.IMUBfraction = (IMUB.loc[50].index.size)/(IMall.loc[50].index.size)   
    LMall = (file.loc[file['mass']<2])
    LMUB = ((file.loc[file['energy'] >= 0]).loc[(file.loc[file['energy'] >= 0])['mass'] <2])
#   LMB = ((file.loc[file['energy'] < 0]).loc[(file.loc[file['energy'] < 0])['mass'] <2])
    file.LMUBfraction = (LMUB.loc[50].index.size)/(LMall.loc[50].index.size)     
    print (file.LMUBfraction)
    print (file.HMUBfraction)    
   


#%% Plotting mass against velocity for stars inside and outside the cluster

fnamelist =[d['fname1'],d['fname2'],d['fname3'],d['fname4']]
    
fig2, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(40.,20.))
#plt.subplots_adjust(wspace=0.2)
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
#ax1.hist(df1B.loc[50,'mass'],label='Bound stars at 5 Myr: %s stars, sim: %s' %(df1B.loc[50].index.size,d['fname1'][25:27]))
ax1.hist(df1UB.loc[50,'mass'],label='Unbound stars at 5 Myr: %s stars, sim: %s' %(df1UB.loc[50].index.size,d['fname1'][25:27]))
ax1.legend(loc='upper right', title=legend[0])  


ax2.plot(422)
#ax2.hist(df2B.loc[50,'mass'],label='Bound stars at 5 Myr: %s stars, sim: %s' %(df2B.loc[50].index.size,d['fname2'][25:27]))
ax2.hist(df2UB.loc[50,'mass'],label='Unbound stars at 5 Myr: %s stars, sim: %s' %(df2UB.loc[50].index.size,d['fname2'][25:27]))
ax2.legend(loc='upper right', title=legend[1])


ax3.plot(423)
#ax3.hist(df3B.loc[50,'mass'],label='Bound stars at 5 Myr: %s stars, sim: %s' %(df3B.loc[50].index.size,d['fname3'][25:27]))
ax3.hist(df3UB.loc[50,'mass'],label='Unbound stars at 5 Myr: %s stars, sim: %s' %(df3UB.loc[50].index.size,d['fname3'][25:27]))
ax3.legend(loc='upper right', title=legend[2])  

ax4.plot(424)
#ax4.hist(df4B.loc[50,'mass'],label='Bound stars at 5 Myr: %s stars, sim: %s' %(df4B.loc[50].index.size,d['fname4'][25:27]))
ax4.hist(df4UB.loc[50,'mass'],label='Unbound stars at 5 Myr: %s stars, sim: %s' %(df4UB.loc[50].index.size,d['fname4'][25:27]))
ax4.legend(loc='upper right', title=legend[3])  


ax3.set_xlabel('Mass (in solar mass)',fontsize=10.) 
ax4.set_xlabel('Mass (in solar mass)',fontsize=10.)

   
plt.show()


#plt.savefig('PM_velocity_escaped_%s.png' %legendtitle)


#%%



