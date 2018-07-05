# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates and plots the cumulative radial velocity for all snaps


import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import F_Transverse_Velocity_final as TV
import F_BUS_ENERGY as BUS 

f = open('file20.txt')
lines = [line.rstrip('\n') for line in open('file20.txt')]

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

df5 = pd.read_csv(d['fname5'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df6 = pd.read_csv(d['fname6'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df7 = pd.read_csv(d['fname7'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df8 = pd.read_csv(d['fname8'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df9 = pd.read_csv(d['fname9'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df10 = pd.read_csv(d['fname10'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df11 = pd.read_csv(d['fname11'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df12 = pd.read_csv(d['fname12'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df13 = pd.read_csv(d['fname13'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df14 = pd.read_csv(d['fname14'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df15 = pd.read_csv(d['fname15'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df16 = pd.read_csv(d['fname16'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df17 = pd.read_csv(d['fname17'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df18 = pd.read_csv(d['fname18'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df19 = pd.read_csv(d['fname19'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})

df20 = pd.read_csv(d['fname20'], delim_whitespace=True, header=None,\
                  names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
                         'ccname', 'cctime', 'd2cc'], index_col=['snap','star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                                                'radz'], \
                         dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, 'mass': np.float64, 'radx':np.float64, 'rady':np.float64, 'radz':np.float64})


nsnaps = 101
nstars = int((df1.index.size)/nsnaps)  #test with different number of stars from future simulations (count_stars.py)

        

energy1 = BUS.bound_unbound_stars(d['fname1'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df1.loc[ssnap,'energy'] = energy1[ssnap]




energy2 = BUS.bound_unbound_stars(d['fname2'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df2.loc[ssnap,'energy'] = energy2[ssnap]




energy3 = BUS.bound_unbound_stars(d['fname3'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df3.loc[ssnap,'energy'] = energy3[ssnap]



energy4 = BUS.bound_unbound_stars(d['fname4'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df4.loc[ssnap,'energy'] = energy4[ssnap]

energy5 = BUS.bound_unbound_stars(d['fname5'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df5.loc[ssnap,'energy'] = energy5[ssnap]

energy6 = BUS.bound_unbound_stars(d['fname6'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df6.loc[ssnap,'energy'] = energy6[ssnap]
    
energy7 = BUS.bound_unbound_stars(d['fname7'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df7.loc[ssnap,'energy'] = energy7[ssnap]

energy8 = BUS.bound_unbound_stars(d['fname8'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df8.loc[ssnap,'energy'] = energy8[ssnap]

energy9 = BUS.bound_unbound_stars(d['fname9'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df9.loc[ssnap,'energy'] = energy9[ssnap]
    
energy10 = BUS.bound_unbound_stars(d['fname10'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df10.loc[ssnap,'energy'] = energy10[ssnap]    

energy11 = BUS.bound_unbound_stars(d['fname11'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df11.loc[ssnap,'energy'] = energy11[ssnap]

energy12 = BUS.bound_unbound_stars(d['fname12'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df12.loc[ssnap,'energy'] = energy12[ssnap]

energy13 = BUS.bound_unbound_stars(d['fname13'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df13.loc[ssnap,'energy'] = energy13[ssnap]
    
energy14 = BUS.bound_unbound_stars(d['fname14'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df14.loc[ssnap,'energy'] = energy14[ssnap]

energy15 = BUS.bound_unbound_stars(d['fname15'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df15.loc[ssnap,'energy'] = energy15[ssnap]

energy16 = BUS.bound_unbound_stars(d['fname16'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df16.loc[ssnap,'energy'] = energy16[ssnap]
    
energy17 = BUS.bound_unbound_stars(d['fname17'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df17.loc[ssnap,'energy'] = energy17[ssnap] 

energy18 = BUS.bound_unbound_stars(d['fname18'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df18.loc[ssnap,'energy'] = energy18[ssnap]
    
energy19 = BUS.bound_unbound_stars(d['fname19'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df19.loc[ssnap,'energy'] = energy19[ssnap] 
    
    
energy20 = BUS.bound_unbound_stars(d['fname20'],nsnaps,nstars)

for ssnap in range(0,nsnaps):
    df20.loc[ssnap,'energy'] = energy20[ssnap] 



dflist = [df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15,df16,df17,df18,df19,df20]


for file in dflist:
    allstars = (file)
    UB = (file.loc[file['energy'] >= 0])
    file.totalUBfraction = (UB.loc[50].index.size)/(allstars.loc[50].index.size)
    HMall = (file.loc[file['mass']>=8])
    HMUB = ((file.loc[file['energy'] >= 0]).loc[(file.loc[file['energy'] >= 0])['mass'] >= 8])
#    HMB = ((file.loc[file['energy'] < 0]).loc[(file.loc[file['energy'] < 0])['mass'] >= 8])
    file.HMUBfraction = (HMUB.loc[50].index.size)/(HMall.loc[50].index.size)
    LMall = (file.loc[file['mass']<2])
    LMUB = ((file.loc[file['energy'] >= 0]).loc[(file.loc[file['energy'] >= 0])['mass'] <2])
#   LMB = ((file.loc[file['energy'] < 0]).loc[(file.loc[file['energy'] < 0])['mass'] <2])
    file.LMUBfraction = (LMUB.loc[50].index.size)/(LMall.loc[50].index.size) 
    file.IMUBfraction = ((UB.loc[50].index.size)-(HMUB.loc[50].index.size)-(LMUB.loc[50].index.size))/((allstars.loc[50].index.size)-(HMall.loc[50].index.size)-(LMall.loc[50].index.size))      

    print (file.totalUBfraction,'/',file.LMUBfraction, '/' ,file.IMUBfraction, '/' , file.HMUBfraction)    








