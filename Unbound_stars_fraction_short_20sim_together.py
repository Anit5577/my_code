#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

# this code calculates the energy of each star after it calls the function to read in 20 simulation data.
# it contains the callable function unbound_stars, which uses the F2PY - routine BUS to calculate the energy in Fortran and then loads it as an additional column to each file in dflist.

import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from fractions import Fraction
from function_file import read_in_summary_datafiles
import matplotlib.ticker as ticker

#%%
All_read,fname,nlines  = read_in_summary_datafiles('file20.txt')

#%% this calculates the unbound-fraction for different mass regimes at 4 times
#
#snaps = [0, 10, 50, 100]
#
#UB_fraction = np.zeros((nlines, len(snaps)))
#HM_fraction = np.zeros((nlines, len(snaps)))
#HMUB_AllHM_fraction = np.zeros((nlines, len(snaps)))
#HMUB_AllUB_fraction = np.zeros((nlines, len(snaps)))
#LMUB_AllLM_fraction = np.zeros((nlines, len(snaps)))
#
#for i, n in product(range(nlines), range(len(snaps))):
#
#    UB_fraction[i,n] = Fraction(len(All_read[i].loc[snaps[n]][All_read[i].loc[snaps[n],'Unbound'] == True]), \
#    len(All_read[i].loc[snaps[n]]))
#
#    HM_fraction[i,n] = Fraction(len(All_read[i].loc[snaps[n]][All_read[i].loc[snaps[n],'mass'] >= 8.]), \
#    len(All_read[i].loc[snaps[n]]))
#
#    LMUB_AllLM_fraction[i,n] = Fraction(len(All_read[i].loc[snaps[n]][(All_read[i].loc[snaps[n],'mass']<= 2.5) \
#                  & (All_read[i].loc[snaps[n],'Unbound']== True)]), \
#                len(All_read[i].loc[snaps[n]][(All_read[i].loc[snaps[n],'mass'] < 8.)]))
#
#    if len(All_read[i].loc[snaps[n]][(All_read[i].loc[snaps[n],'mass']>= 8.)]) != 0:
#        HMUB_AllHM_fraction[i,n] = Fraction(len(All_read[i].loc[snaps[n]][(All_read[i].loc[snaps[n],'mass']>= 8.) \
#                          & (All_read[i].loc[snaps[n],'Unbound']== True)]), \
#                        len(All_read[i].loc[snaps[n]][(All_read[i].loc[snaps[n],'mass']>= 8.)]))
#    else:
#        continue
#
#    if len(All_read[i].loc[snaps[n]][(All_read[i].loc[snaps[n],'Unbound']== True)]) != 0:
#        HMUB_AllUB_fraction[i,n] = Fraction(len(All_read[i].loc[snaps[n]][(All_read[i].loc[snaps[n],'mass']>= 8.) \
#                                  & (All_read[i].loc[snaps[n],'Unbound']== True)]), \
#                            len(All_read[i].loc[snaps[n]][(All_read[i].loc[snaps[n],'Unbound']== True)]))
#    else:
#        continue

#%%
# 
for i in range(nlines):
    print (dname[i])
    print ('HM-number-unbound', len(dflist[i].loc[100][(dflist[i].loc[100,'mass'] >= 8.) & (dflist[i].loc[100,'Unbound']== True)]))
    print ('HM-number-all', len(dflist[i].loc[100][dflist[i].loc[100,'mass'] >= 8.]))
    print ('LM-number-unbound', len(dflist[i].loc[100][(dflist[i].loc[100,'mass'] <= 2) & (dflist[i].loc[100,'Unbound']== True)]))
     
    

#%%

snaps = 101

UB_fraction = np.zeros((nlines, snaps))
IM_fraction = np.zeros((nlines, snaps))
HMUB_AllHM_fraction = np.zeros((nlines, snaps))
LMUB_AllLM_fraction = np.zeros((nlines, snaps))

for i, n in product(range(nlines), range(snaps)):

#    UB_fraction[i,n] = Fraction(len(All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == True]), \
#    len(All_read[i].loc[n]))

#    IM_fraction[i,n] = Fraction(len(All_read[i].loc[n][(All_read[i].loc[n, 'mass']> 2.5) & (All_read[i].loc[n, 'mass'] < 8.) \
#                  & (All_read[i].loc[n,'Unbound']== True)]), \
#                len(All_read[i].loc[n][(All_read[i].loc[n, 'mass'] >= 2.5) & (All_read[i].loc[n, 'mass'] < 8.)]))
#

    LMUB_AllLM_fraction[i,n] = Fraction(len(All_read[i].loc[n][(All_read[i].loc[n, 'mass']<= 2) \
                  & (All_read[i].loc[n,'Unbound']== True)]), \
                len(All_read[i].loc[n][(All_read[i].loc[n, 'mass'] <= 2)]))

    if len(All_read[i].loc[n][(All_read[i].loc[n, 'mass']>= 8.)]) != 0:
        HMUB_AllHM_fraction[i,n] = Fraction(len(All_read[i].loc[n][(All_read[i].loc[n, 'mass']>= 8.) \
                          & (All_read[i].loc[n, 'Unbound']== True)]), \
                        len(All_read[i].loc[n][(All_read[i].loc[n, 'mass']>= 8.)]))
    else:
        continue


#%%
#UB_fraction = np.zeros((nlines, snaps))
#IM_fraction = np.zeros((nlines, snaps))
#HMUB_AllHM_fraction = np.zeros((nlines, snaps))
#LMUB_AllLM_fraction = np.zeros((nlines, snaps))
#
#for i, n in product(range(nlines), range(snaps)):
#
##    UB_fraction[i,n] = Fraction(len(All_read[i].loc[n][All_read[i].loc[n, 'Unbound'] == True]), \
##    len(All_read[i].loc[n]))
#
##    IM_fraction[i,n] = Fraction(len(All_read[i].loc[n][(All_read[i].loc[n, 'mass']> 2.5) & (All_read[i].loc[n, 'mass'] < 8.) \
##                  & (All_read[i].loc[n,'Unbound']== True)]), \
##                len(All_read[i].loc[n][(All_read[i].loc[n, 'mass'] >= 2.5) & (All_read[i].loc[n, 'mass'] < 8.)]))
##
#
#    LMUB_AllLM_fraction[i,n] = Fraction(len(dflist[i].loc[n][(dflist[i].loc[n, 'mass']<= 2) \
#                  & (dflist[i].loc[n,'Unbound']== True)]), \
#                len(dflist[i].loc[n][(dflist[i].loc[n, 'mass'] <= 2)]))
#
#    if len(dflist[i].loc[n][(dflist[i].loc[n, 'mass']>= 8.)]) != 0:
#        HMUB_AllHM_fraction[i,n] = Fraction(len(dflist[i].loc[n][(dflist[i].loc[n, 'mass']>= 8.) \
#                          & (dflist[i].loc[n, 'Unbound']== True)]), \
#                        len(dflist[i].loc[n][(dflist[i].loc[n, 'mass']>= 8.)]))
#    else:
#        continue


#%% plots time evolution of un-bound stars in high-mass and low-mass regimes

x = np.arange(0., 10.1, 0.1)

#fig, ax = plt.subplots()
#plt.subplots_adjust(top=0.95, bottom=0.135, left=0.15, right=0.968)

for i in range(nlines):
    fig, ax = plt.subplots()
    plt.subplots_adjust(top=0.95, bottom=0.135, left=0.106, right=0.968)

    fig.patch.set_facecolor('#002342')
    ax.set_facecolor('#002342')
    plt.setp(ax.spines.values(), linewidth=2)
    ax.set_facecolor('#002342')
    
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.plot(x, LMUB_AllLM_fraction[i],  label ='Low-mass', c='steelblue')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.plot(x, HMUB_AllHM_fraction[i], label ='High-mass', c='seagreen')
#    ax.scatter(x, IM_fraction[i], s=0.5, color='green', label ='Intermediate-mass')
    ax.tick_params(which='both', direction='in', length=6., width=2., colors='white', \
                   labelsize=12.)



#    fig.suptitle(fname[i])
#    leg = ax.legend(loc='upper left', frameon=False, fontsize=14.)
#    for text in leg.get_texts():
#        text.set_color('white')
    ax.set_xlabel('Cluster age (Myr)', fontsize=14.)
    ax.set_ylabel('Ejected fraction', fontsize=14.)
    ax.set_xlim(0., 10.1)
    ax.set_ylim(-0.01, 0.5)
#    plt.savefig('Unbound_fraction_bymass%s.png' %fname[i])



#    All_read,fname,nlines  = read_in_summary_datafiles('file20.txt')
#    
#    HMUB_HM_fraction = np.zeros((nlines, snaps))
#    LMUB_LM_fraction = np.zeros((nlines, snaps))
#    
#    LMUB_LM_fraction[i,n] = Fraction(len(All_read[0].loc[n][(All_read[0].loc[n, 'mass']<= 2) \
#                  & (All_read[0].loc[n,'Unbound']== True)]), \
#                len(All_read[0].loc[n][(All_read[0].loc[n, 'mass'] <= 2)]))
#    
#    if len(All_read[0].loc[n][(All_read[0].loc[n, 'mass']>= 8.)]) != 0:
#        HMUB_HM_fraction[i,n] = Fraction(len(All_read[0].loc[n][(All_read[0].loc[n, 'mass']>= 8.) \
#                          & (All_read[0].loc[n, 'Unbound']== True)]), \
#                        len(All_read[0].loc[n][(All_read[0].loc[n, 'mass']>= 8.)]))
#    
#    ax.plot(x, LMUB_LM_fraction[0],  label ='Low-mass', c='red')  
#    ax.plot(x, HMUB_HM_fraction[0], label ='High-mass', c='yellow')

#%%
plt.savefig('Unbound_fraction_bymass%s.png' %fname[0], facecolor='#002342')
plt.show()


#%%

x = np.arange(0., 10.1, 0.1)

plt.style.use('seaborn-poster')


for i in range(nlines):
    fig, ax = plt.subplots(figsize=(8., 8.))
    plt.setp(ax.spines.values(), linewidth=4)
    ax.spines['bottom'].set_color('#002342')
    ax.spines['top'].set_color('#002342')
    ax.spines['left'].set_color('#002342')
    ax.spines['right'].set_color('#002342')
    ax.xaxis.label.set_color('#002342')
    ax.yaxis.label.set_color('#002342')
    
    
    ax.set_xlabel('x (pc)', fontsize=16.)
    ax.set_ylabel('y (pc)', fontsize=16.)

    ax.plot(x, LMUB_AllLM_fraction[i],  label ='Low-mass', c='darkred')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.plot(x, HMUB_AllHM_fraction[i], label ='High-mass', c='goldenrod')

    ax.tick_params(which='both', direction='in', length=8., width=3., labelsize=12., colors='#002342')
    ax.set_xlabel('Cluster age (Myr)', fontsize=16.)
    ax.set_ylabel('Ejected fraction', fontsize=16.)
    ax.set_xlim(0., 10.1)
    ax.set_ylim(-0.01, 0.5)
    leg = ax.legend(loc='upper right', frameon=False, fontsize=16.)    

    for text in leg.get_texts():
        text.set_color('#002342')
    
    plt.savefig('Unbound_%s.png' %i, transparent=True, dpi=600 )
    
plt.show()

#ax.set_title('Cluster age %s Myr' %(np.round(dflist[0].loc[100].iloc[0]['time'],\
#       decimals=1)), fontsize=16., color='#002342')

#%%

plt.savefig('Unbound__1.png', transparent=True, dpi=300 )



#%%

x = np.arange(0., 10.1, 0.1)

fig, ax = plt.subplots()

clist = ['b', 'g']
mlist = ['_', 'x']

i = 0
j = 1

ax.scatter(x, HMUB_AllHM_fraction[i], s=5, color=clist[0], marker=mlist[0], label ='High-mass, %s stars' %fname[i][-8:-4])
ax.scatter(x, LMUB_AllLM_fraction[i], s=5, color=clist[0], marker=mlist[1], label ='Low-mass, %s stars' %fname[i][-8:-4])
ax.scatter(x, HMUB_AllHM_fraction[j], s=5, color=clist[1], marker=mlist[0], label ='High-mass, %s stars' %fname[j][-8:-4])
ax.scatter(x, LMUB_AllLM_fraction[j], s=5, color=clist[1], marker=mlist[1], label ='Low-mass, %s stars' %fname[j][-8:-4])


fig.suptitle(fname[i])
ax.legend(loc='upper left', frameon=False, fontsize=8.)
ax.set_xlabel('Cluster age (in Myr)')
ax.set_ylabel('Unbound fraction')
ax.set_xlim(0., 10.1)
ax.set_ylim(0.)
#    plt.savefig('Unbound_fraction_bymass%s.png' %fname[i])

plt.show()


#%%

x = np.arange(0., 10.1, 0.1)

fig, ax = plt.subplots()

all_init_1_6 = [0, 1, 2, 3, 4]
all_init_3_0 = [5, 6, 7, 8, 9]

for i in all_init_1_6:
#   ax.scatter(x, HMUB_AllHM_fraction[i], s=0.5)
    ax.plot(x, HMUB_AllHM_fraction[i], label='High-mass, D=%s, alpha$_{vir}$=%s'\
            %(fname[i][11:14],fname[i][15:18]))
#    ax.scatter(x, LM8UB_AllLM_fraction[i], s=0.5, color='blue', label ='LMUB (<8) of LMtotal fraction')
    ax.plot(x, LMUB_AllLM_fraction[i],label='Low-mass, D=%s, alpha$_{vir}$=%s'\
            %(fname[i][11:14],fname[i][15:18]))

#    fig.suptitle('High-mass star unbound fractions')
    fig.suptitle('Low-mass star unbound fractions')
    ax.legend(loc='upper left', frameon=False, fontsize=8.)
    ax.set_xlabel('Cluster age (in Myr)')
    ax.set_ylabel('Unbound fraction')
    ax.set_xlim(0., 10.1)
    ax.set_ylim(0., 1.0)

plt.show()


