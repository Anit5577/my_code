# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import F_Transverse_Velocity_final as TV
#import F_COD_Radius_Nstars as CODRN  #turn this on, if COD-correction is required.

fname1 = input('Datafile virial ratio=0.1, D=1.6: ')
fname2 = input('Datafile virial ratio=0.1, D=3.0: ')
fname3 = input('Datafile virial ratio=0.3, D=1.6: ')
fname4 = input('Datafile virial ratio=0.3, D=3.0: ')
fname5 = input('Datafile virial ratio=0.5, D=1.6: ')
fname6 = input('Datafile virial ratio=0.5, D=3.0: ')
fname7 = input('Datafile virial ratio=1.5, D=1.6: ')
fname8 = input('Datafile virial ratio=1.5, D=3.0: ')

df1 = pd.read_csv(fname1, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})

df2 = pd.read_csv(fname2, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})

df3 = pd.read_csv(fname3, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})

df4 = pd.read_csv(fname4, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})        

df5 = pd.read_csv(fname5, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})        

df6 = pd.read_csv(fname6, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})        

df7 = pd.read_csv(fname7, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})   

df8 = pd.read_csv(fname8, delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz', 'velx','vely','velz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64, \
                                'velx':np.float64,'vely':np.float64,'velz':np.float64})   

dflist =[df1,df2,df3,df4,df5,df6,df7,df8]
fnamelist =[fname1,fname2,fname3,fname4,fname5,fname6,fname7,fname8]

nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  


 #%%    

#for fname in fnamelist:
#    transvel = TV.transverse_velocity(fname,nsnaps,nstars)
#    
#    for x and df in runlist and dflist:
#        for ssnap in range(0,nsnaps):
#            x.loc[0,'xdist'] = 0
#            x.loc[0,'ydist'] = 0  
#            x.loc[ssnap,'xdist'] = transvel[ssnap,0]
#            x.loc[ssnap,'ydist'] = transvel[ssnap,1]
#            df.append(x)    
#
#print(df5, df7)

transvel1 = TV.transverse_velocity(fname1,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[0,'xdist'] = 0
    df1.loc[0,'ydist'] = 0  
    df1.loc[ssnap,'xdist'] = transvel1[ssnap,0]
    df1.loc[ssnap,'ydist'] = transvel1[ssnap,1]


transvel2 = TV.transverse_velocity(fname2,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df2.loc[0,'xdist'] = 0
    df2.loc[0,'ydist'] = 0  
    df2.loc[ssnap,'xdist'] = transvel2[ssnap,0]
    df2.loc[ssnap,'ydist'] = transvel2[ssnap,1]


transvel3 = TV.transverse_velocity(fname3,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df3.loc[0,'xdist'] = 0
    df3.loc[0,'ydist'] = 0  
    df3.loc[ssnap,'xdist'] = transvel3[ssnap,0]
    df3.loc[ssnap,'ydist'] = transvel3[ssnap,1]


transvel4 = TV.transverse_velocity(fname4,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df4.loc[0,'xdist'] = 0
    df4.loc[0,'ydist'] = 0  
    df4.loc[ssnap,'xdist'] = transvel4[ssnap,0]
    df4.loc[ssnap,'ydist'] = transvel4[ssnap,1]


transvel5 = TV.transverse_velocity(fname5,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df5.loc[0,'xdist'] = 0
    df5.loc[0,'ydist'] = 0  
    df5.loc[ssnap,'xdist'] = transvel5[ssnap,0]
    df5.loc[ssnap,'ydist'] = transvel5[ssnap,1]

  
transvel6 = TV.transverse_velocity(fname6,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df6.loc[0,'xdist'] = 0
    df6.loc[0,'ydist'] = 0  
    df6.loc[ssnap,'xdist'] = transvel6[ssnap,0]
    df6.loc[ssnap,'ydist'] = transvel6[ssnap,1]


transvel7 = TV.transverse_velocity(fname7,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df7.loc[0,'xdist'] = 0
    df7.loc[0,'ydist'] = 0  
    df7.loc[ssnap,'xdist'] = transvel7[ssnap,0]
    df7.loc[ssnap,'ydist'] = transvel7[ssnap,1]


transvel8 = TV.transverse_velocity(fname8,nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df8.loc[0,'xdist'] = 0
    df8.loc[0,'ydist'] = 0  
    df8.loc[ssnap,'xdist'] = transvel8[ssnap,0]
    df8.loc[ssnap,'ydist'] = transvel8[ssnap,1]    


#%% Plotting cumulative distribution of 2D-velocities of x and y component, proper motion velocities and 3D velocities on one plot

from matplotlib.ticker import MaxNLocator

snaplist = [1,5,10,50]
star = np.arange(1,nstars+1,1)

fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8)) = plt.subplots(4, 2, figsize=(15.,25.))

axes = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]

plt.subplots_adjust(wspace=0.3)
#x_minor_locator = AutoMinorLocator(2)
y_minor_locator = AutoMinorLocator(4)

legend=[]

for fname in fnamelist:

    if fname[17] == 'X':
       legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
    elif fname[17] == '5':
        legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
    elif fname[17] == '2':    
        legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, sim=%s' %(fname[7],fname[8],fname[22],fname[23],fname[12],fname[25:27]))
    elif fname[5:7] == '1r':
        legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, sim=%s' %fname[25:27])
    elif fname[5:7] == '2r':
        legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, sim=%s' %fname[25:27])
    
    legend.append(legendtitle)
            

for locsnap in snaplist:
    
    if locsnap == 1:
        linecolour ='b'
        line1='-'
    elif locsnap == 5:
        linecolour = 'g'
        line1='--'
    elif locsnap == 10:
        linecolour = 'r'
        line1='-.'
    elif locsnap == 50:
        linecolour = 'orange'
        line1=':'
  
    df1.loc[locsnap,'PM-vel'] = (np.sqrt(df1['xdist']**2. + df1['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df1PM = df1.loc[locsnap].sort_values('PM-vel')
        
    ax1.plot(421)
    ax1.plot(df1PM['PM-vel'],star,c=linecolour,linestyle=line1,label='%s Myr' %(locsnap/10))
    ax1.legend(loc='lower right', ncol=2, frameon=False, title=legend[0])
        
    df2.loc[locsnap,'PM-vel'] = (np.sqrt(df2['xdist']**2. + df2['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df2PM = df2.loc[locsnap].sort_values('PM-vel')
    
    ax2.plot(422)
    ax2.plot(df2PM['PM-vel'],star,c=linecolour,linestyle=line1,label='%s Myr' %(locsnap/10))
    ax2.legend(loc='lower right', ncol=2, frameon=False, title=legend[1])    
    
    df3.loc[locsnap,'PM-vel'] = (np.sqrt(df3['xdist']**2. + df3['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df3PM = df3.loc[locsnap].sort_values('PM-vel')
    
    ax3.plot(423)
    ax3.plot(df3PM['PM-vel'],star,c=linecolour,linestyle=line1,label='%s Myr' %(locsnap/10))
    ax3.legend(loc='lower right', ncol=2, frameon=False, title=legend[2])   
    
    df4.loc[locsnap,'PM-vel'] = (np.sqrt(df4['xdist']**2. + df4['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df4PM = df4.loc[locsnap].sort_values('PM-vel')
    
    ax4.plot(424)
    ax4.plot(df4PM['PM-vel'],star,c=linecolour,linestyle=line1,label='%s Myr' %(locsnap/10))
    ax4.legend(loc='lower right', ncol=2, frameon=False, title=legend[3])   

    df5.loc[locsnap,'PM-vel'] = (np.sqrt(df5['xdist']**2. + df5['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df5PM = df5.loc[locsnap].sort_values('PM-vel')
    
    ax5.plot(425)
    ax5.plot(df5PM['PM-vel'],star,c=linecolour,linestyle=line1,label='%s Myr' %(locsnap/10))
    ax5.legend(loc='lower right', ncol=2, frameon=False, title=legend[4])       
    
    df6.loc[locsnap,'PM-vel'] = (np.sqrt(df6['xdist']**2. + df6['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df6PM = df6.loc[locsnap].sort_values('PM-vel')
    
    ax6.plot(426)
    ax6.plot(df6PM['PM-vel'],star,c=linecolour,linestyle=line1,label='%s Myr' %(locsnap/10))
    ax6.legend(loc='lower right', ncol=2, frameon=False, title=legend[5])   
    
    df7.loc[locsnap,'PM-vel'] = (np.sqrt(df7['xdist']**2. + df7['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df7PM = df7.loc[locsnap].sort_values('PM-vel')
        
    ax7.plot(427)
    ax7.plot(df7PM['PM-vel'],star,c=linecolour,linestyle=line1,label='%s Myr' %(locsnap/10))
    ax7.legend(loc='lower right', ncol=2, frameon=False, title=legend[6])   
    
    df8.loc[locsnap,'PM-vel'] = (np.sqrt(df8['xdist']**2. + df8['ydist']**2.)) * (30856780000000./(31556926.*10.**5.))  
    df8PM = df8.loc[locsnap].sort_values('PM-vel')
    
    ax8.plot(428)
    ax8.plot(df8PM['PM-vel'],star,c=linecolour,linestyle=line1,label='%s Myr' %(locsnap/10))
    ax8.legend(loc='lower right', ncol=2, frameon=False, title=legend[7])   
    
    
for i in axes:
    i.xaxis.set_minor_locator(AutoMinorLocator(2))
    i.yaxis.set_minor_locator(y_minor_locator)
    i.tick_params(which='both',direction='in',top='on',right='on')
    i.xaxis.set_major_locator(MaxNLocator(integer=True))
    i.set_xlabel('Proper motion (km/s)',fontsize=12.) 
    i.set_ylabel(r'$N_{stars}$',fontsize=12.)
    i.set_xlim(0,5)
    i.set_ylim(0,nstars)

plt.savefig('Proper_Motion_plot_%d stars.png' %nstars)