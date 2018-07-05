# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from function_file import read_in_datafiles, velocity_elements, energy_stars, stars_outside_2HMR

dflist,d  = read_in_datafiles('file20.txt')

dname = sorted(d.values())

dflist = energy_stars(dflist,dname)       
dflist = velocity_elements(dflist,dname)
dflist = stars_outside_2HMR(dflist,dname)
 


#%%

for n in range(20):
    dflist[n].UB = (dflist[n].loc[dflist[n]['Unbound'] == True])  
#    dflist[n].B = (dflist[n].loc[dflist[n]['Unbound'] == False])  
#    dflist[n].ESC = (dflist[n].loc[dflist[n]['escaped'] == True])  
            


#%%

for n in range(20):
    HMall = (dflist[n].loc[dflist[n]['mass']>=8])
    HMUB = ((dflist[n].loc[dflist[n]['energy'] >= 0]).loc[(dflist[n].loc[dflist[n]['energy'] >= 0])['mass'] >= 8])
#    HMB = ((dflist[n].loc[dflist[n]['energy'] < 0]).loc[(dflist[n].loc[dflist[n]['energy'] < 0])['mass'] >= 8])
    dflist[n].HMUBfraction = (HMUB.loc[50].index.size)/(HMall.loc[50].index.size)
    IMall = (dflist[n].loc[dflist[n]['mass']<8])
    IMUB = ((dflist[n].loc[dflist[n]['energy'] >= 0]).loc[(dflist[n].loc[dflist[n]['energy'] >= 0])['mass']< 8])
#   IMB = ((dflist[n].loc[dflist[n]['energy'] < 0]).loc[(dflist[n].loc[dflist[n]['energy'] < 0])['mass'] < 8])
    dflist[n].IMUBfraction = (IMUB.loc[50].index.size)/(IMall.loc[50].index.size)   
    LMall = (dflist[n].loc[dflist[n]['mass']<2])
    LMUB = ((dflist[n].loc[dflist[n]['energy'] >= 0]).loc[(dflist[n].loc[dflist[n]['energy'] >= 0])['mass'] <2])
#   LMB = ((dflist[n].loc[dflist[n]['energy'] < 0]).loc[(dflist[n].loc[dflist[n]['energy'] < 0])['mass'] <2])
    dflist[n].LMUBfraction = (LMUB.loc[50].index.size)/(LMall.loc[50].index.size)     
    print (dflist[n].LMUBfraction, dflist[n].HMUBfraction)    
   


#%% Plotting mass against velocity for stars inside and outside the cluster

   
fig2, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(40.,20.))
#plt.subplots_adjust(wspace=0.2)
#x_minor_locator = AutoMinorLocator(2)
#y_minor_locator = AutoMinorLocator(4)

legend =[]

for fname in dname:
    
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
ax1.hist(dflist[0].UB.loc[50,'mass'],label='Unbound stars at 5 Myr: %s stars, sim: %s' %(dflist[0].UB.loc[50].index.size,d['fname1'][25:27]))
ax1.legend(loc='upper right', title=legend[0])  


ax2.plot(422)
#ax2.hist(df2B.loc[50,'mass'],label='Bound stars at 5 Myr: %s stars, sim: %s' %(df2B.loc[50].index.size,d['fname2'][25:27]))
ax2.hist(dflist[1].UB.loc[50,'mass'],label='Unbound stars at 5 Myr: %s stars, sim: %s' %(dflist[1].UB.loc[50].index.size,d['fname2'][25:27]))
ax2.legend(loc='upper right', title=legend[1])


ax3.plot(423)
#ax3.hist(df3B.loc[50,'mass'],label='Bound stars at 5 Myr: %s stars, sim: %s' %(df3B.loc[50].index.size,d['fname3'][25:27]))
ax3.hist(dflist[2].UB.loc[50,'mass'],label='Unbound stars at 5 Myr: %s stars, sim: %s' %(dflist[2].UB.loc[50].index.size,d['fname3'][25:27]))
ax3.legend(loc='upper right', title=legend[2])  

ax4.plot(424)
#ax4.hist(df4B.loc[50,'mass'],label='Bound stars at 5 Myr: %s stars, sim: %s' %(df4B.loc[50].index.size,d['fname4'][25:27]))
ax4.hist(dflist[3].UB.loc[50,'mass'],label='Unbound stars at 5 Myr: %s stars, sim: %s' %(dflist[3].UB.loc[50].index.size,d['fname4'][25:27]))
ax4.legend(loc='upper right', title=legend[3])  


ax3.set_xlabel('Mass (in solar mass)',fontsize=10.) 
ax4.set_xlabel('Mass (in solar mass)',fontsize=10.)

   
plt.show()


#plt.savefig('PM_velocity_escaped_%s.png' %legendtitle)


#%%



