#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:50:17 2018

@author: php17cs
"""

# this is a callable function to read in any number of simulations from an inputfile

def read_in_any_datafiles(inputfile):
    import pandas as pd
    import numpy as np

    f = open(inputfile)
    lines = [line.rstrip('\n') for line in open(inputfile)]

    nlines = len(lines)

    d = {}
    for x in range(1, nlines+1, 1):
        d['fname{0}'.format(x)] = lines[x-1]

    f.close()

    dname = sorted(d.values())

    dflist = []
    for n in range(nlines):
        dflist.append(n)
        dflist[n] = pd.read_csv(dname[n], delim_whitespace=True, header=None,\
                      names=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                             'radz', 'velx', 'vely', 'velz', \
                             'ccname', 'cctime', 'd2cc'], index_col=['snap', 'star'],\
                             usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', \
                                      'radz', 'velx', 'vely', 'velz'], \
                             dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, \
                                    'mass': np.float64, 'radx':np.float64, 'rady':np.float64, \
                                    'radz':np.float64, 'velx':np.float64, 'vely':np.float64, \
                                    'velz':np.float64})
#                         names=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
#                         'ccname', 'cctime', 'd2cc'], index_col=['snap', 'star'], usecols=['snap', 'time', 'star', 'mass', 'radx', 'rady', 'radz', 'velx', 'vely', 'velz', \
#                         'ccname', 'cctime', 'd2cc'])

    
    return dflist, dname, nlines

def read_in_summary_datafiles(inputfile):
    import pandas as pd
    import numpy as np

    f = open(inputfile)
    lines = [line.rstrip('\n') for line in f]

    nlines = len(lines)

    A = {}
    for x in range(1, nlines+1, 1):
        A['fname{0}'.format(x)] = lines[x-1]

    f.close()

    fname = sorted(A.values())

    All_read = []
    for n in range(nlines):
        All_read.append(n)
        All_read[n] = pd.read_csv(fname[n], index_col=['snap', 'star'], \
                usecols=['snap', 'star', 'time', 'mass', 'PM-velxy', '3D-velxyz', 'Unbound'], \
                dtype={'snap': np.int16, 'time': np.float64, 'star': np.int16, \
                                    'mass': np.float64, 'PM-velxy': np.float64, '3D-velxyz': np.float64, \
                                    'Unbound': np.bool})
        
        All_read[n] = All_read[n].sort_index()
    
    return All_read, fname, nlines

#%%

def plots_legend(dname):

    legend = []

    for fname in dname:

        if fname[21] == 'E':

            if fname[17] == 'X':
                legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution,\
                               $N_{sim}$=1000'\
                               %(fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[17] == '5':
                legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution, \
                               $N_{sim}$=500'\
                               %(fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[17] == '2':
                legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, stellar evolution, \
                               $N_{sim}$=2000'\
                               %(fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[5:7] == '1r':
                legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, stellar evolution, \
                               $N_{sim}$=1000')
            elif fname[5:7] == '2r':
                legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, stellar evolution, \
                               $N_{sim}$=1000')

        if fname[21] == 'S':
            if fname[17] == 'X':
                legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution, \
                               $N_{sim}$=1000'\
                               %(fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[17] == '5':
                legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution, \
                               $N_{sim}$=500'\
                               %(fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[17] == '2':
                legendtitle = (r'D=%s.%s, $\alpha_{vir}$=%s.%s, init_rad=%s pc, no evolution, \
                               $N_{sim}$=2000'\
                               %(fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[5:7] == '1r':
                legendtitle = (r'D=1.6, $\alpha_{vir}$=0.3, init_rad=1 pc, no evolution, \
                               $N_{sim}$=1000')
            elif fname[5:7] == '2r':
                legendtitle = (r'D=3.0, $\alpha_{vir}$=0.5, init_rad=1 pc, no evolution, \
                               $N_{sim}$=1000')
        legend.append(legendtitle)

    return legend

#%% function to provide the energy for each star in each snapshot in each simulation
#and the addition of a column of its bound or unbound status

def energy_stars(dflist, dname, nlines):
    import numpy as np
    import F_BOUND_ENERGY_CRAP as BUSCRAP 
    nsnaps=101

    for n in range(nlines):
        nstars = dflist[0].loc[0].index.size
        energylist = BUSCRAP.bound_unbound_stars(dname[n], nsnaps, nstars)
        for ssnap in range(nsnaps):
            dflist[n].loc[ssnap, 'energy'] = energylist[ssnap]
        print(dname[n], ' energy calculated')
        dflist[n]['Unbound'] = np.where(dflist[n]['energy'] >= 0, True, False)

    return dflist

#%% function to calculate the velocities for each star from the distance
#travelled in each dimension over a timestep. result will be in km/s and added to dataframe

#def velocity_elements(dflist, dname, nlines):
def velocity_elements(dflist, dname, nlines):

    import numpy as np
#    import F_Transverse_Velocity_final as TV
#    nsnaps = 101
#    pc = 3.08567758*10**13   #in km
#    # takes the snapshotlength from the time of the first snapshot after initial conditions
# # takes the snapshotlength from the time of the first snapshot after initial conditions
#    timestep_in_seconds = (3.1556926*10**13)*(np.round(dflist[1].loc[1].iloc[1]\
#                          ['time'],decimals=4))
#    distance_to_velocity = pc/timestep_in_seconds
#
    for n in range(nlines):
#       dflist[n].nstars = dflist[n].loc[0].index.size
#        transvellist = TV.transverse_velocity(dname[n],nsnaps,dflist[n].nstars)
#        for ssnap in range(0,nsnaps):
#            dflist[n].loc[0, 'xdist'] = 0
#            dflist[n].loc[0, 'ydist'] = 0
#            dflist[n].loc[0, 'zdist'] = 0
#            dflist[n].loc[ssnap, 'xdist'] = transvellist[ssnap,0]
#            dflist[n].loc[ssnap, 'ydist'] = transvellist[ssnap,1]
#            dflist[n].loc[ssnap, 'zdist'] = transvellist[ssnap,2]
#
#        dflist[n]['xvel'] = dflist[n]['xdist'].multiply(distance_to_velocity)
#        dflist[n]['yvel'] = dflist[n]['ydist'].multiply(distance_to_velocity)
#        dflist[n]['zvel'] = dflist[n]['zdist'].multiply(distance_to_velocity)
#        dflist[n]['3D-veldist'] = (np.sqrt(dflist[n]['xvel']**2.+dflist[n]['yvel']**2.\
#        +dflist[n]['zvel']**2.)) #3D-velocity from distance/snapshot length
#        dflist[n]['PM-veldist'] = (np.sqrt(dflist[n]['xvel']**2.+dflist[n]['yvel']**2.))
        dflist[n]['3D-velxyz'] = (np.sqrt(dflist[n]['velx']**2.+dflist[n]['vely']**2.+\
              dflist[n]['velz']**2.)) #3D-velocity from distance/snapshot length
        dflist[n]['PM-velxy'] = (np.sqrt(dflist[n]['velx']**2.+dflist[n]['vely']**2.))

    return dflist



#%% function to classify the stars that are inside/outside 2xHMR for a dataframe
#with an added column to the list of its escaped or not status

def COD_corrected_location(dflist,dname,nlines):
    
    import numpy as np
    import F_COD_Radius_Nstars as CODRN
    nsnaps = 101

    for n in range(nlines):
        dflist[n].nstars = dflist[n].loc[0].index.size
        nrad = CODRN.cod_radius(dname[n], nsnaps, dflist[n].nstars)
        for ssnap in range(0, nsnaps):
            dflist[n].loc[ssnap, 'nradx'] = nrad[ssnap, 0]
            dflist[n].loc[ssnap, 'nrady'] = nrad[ssnap, 1]
            dflist[n].loc[ssnap, 'nradz'] = nrad[ssnap, 2]

        print(dname[n], 'COD-corrected locations calculated')
        
        dflist[n]['radval'] = (np.sqrt(dflist[n]['nradx']**2.+dflist[n]['nrady']**2.+\
              dflist[n]['nradz']**2.))
    
    return dflist    



def stars_in_outside_2HMR(dflist, dname, nlines):

    import numpy as np
    import F_COD_Radius_Nstars as CODRN
    nsnaps = 101

    for n in range(nlines):
        dflist[n].nstars = dflist[n].loc[0].index.size
        nrad = CODRN.cod_radius(dname[n], nsnaps, dflist[n].nstars)
        for ssnap in range(0, nsnaps):
            dflist[n].loc[ssnap, 'nradx'] = nrad[ssnap, 0]
            dflist[n].loc[ssnap, 'nrady'] = nrad[ssnap, 1]
            dflist[n].loc[ssnap, 'nradz'] = nrad[ssnap, 2]

        print(dname[n], 'COD-corrected locations calculated')

        dflist[n]['radval'] = (np.sqrt(dflist[n]['nradx']**2.+dflist[n]['nrady']**2.+\
              dflist[n]['nradz']**2.))
        hmrad = []

        for ssnap in range(0, nsnaps):
            dflist_sorted = []
            halfmass = 0.
            cmass = 0.
            hmrad = 0.
            dflist_sorted = dflist[n].loc[ssnap].sort_values('radval')
            halfmass = (dflist[n].loc[ssnap]['mass'].sum()/2.)
            cmass = (dflist_sorted['mass'].cumsum())
            dflist_sorted['hmdif'] = np.absolute(cmass.subtract(halfmass))
            hmrad = (dflist_sorted.loc[dflist_sorted['hmdif'].idxmin(), 'radval'])
            dhmrad = 2*hmrad
            dflist[n].loc[ssnap, 'escaped'] = np.where(dflist[n].loc[ssnap, 'radval'] \
                  >= dhmrad, True, False)

    return dflist

def stars_in_outside_HMR(dflist, nlines):

    import numpy as np
    nsnaps = 101

    for n in range(nlines):

        dflist[n]['radval'] = (np.sqrt(dflist[n]['nradx']**2.+dflist[n]['nrady']**2.\
              +dflist[n]['nradz']**2.))
        hmrad = []

        for ssnap in range(0, nsnaps):
            dflist_sorted = []
            halfmass = 0.
            cmass = 0.
            hmrad = 0.
            dflist_sorted = dflist[n].loc[ssnap].sort_values('radval')
            halfmass = (dflist[n].loc[ssnap]['mass'].sum()/2.)
            cmass = (dflist_sorted['mass'].cumsum())
            dflist_sorted['hmdif'] = np.absolute(cmass.subtract(halfmass))
            hmrad = (dflist_sorted.loc[dflist_sorted['hmdif'].idxmin(), 'radval'])
            varhmrad = 5.5*hmrad
            dflist[n].loc[ssnap, 'HMRescaped'] = np.where(dflist[n].loc[ssnap, 'radval'] \
                  >= varhmrad, True, False)

    return dflist

#%%

def concat_simulations(dflist, dname, nlines):
    import pandas as pd

    filename = []

    for fname in dname: # to allow the filename of the simulations to dictate the labels

        if fname[21] == 'E':

            if fname[17] == 'X':
                legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_1000'\
                               %(nlines, fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[17] == '5':
                legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_500'\
                               %(nlines, fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[17] == '2':
                legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_2000'\
                               %(nlines, fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[5:7] == '1r':
                legendtitle = ('%s_sim_1.6_0.3_1pc_E_1000'%nlines)
            elif fname[5:7] == '2r':
                legendtitle = ('%s_sim_3.0_0.5_1pc_E_1000'%nlines)

        if fname[21] == 'S':
            if fname[17] == 'X':
                legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_1000'\
                               %(nlines, fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[17] == '5':
                legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_500'\
                               %(nlines, fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[17] == '2':
                legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_2000'\
                               %(nlines, fname[7], fname[8], fname[22], fname[23], fname[12]))
            elif fname[5:7] == '1r':
                if fname[16] == '1':
                    legendtitle = ('%s_sim_1.6_0.3_1pc_S_1000'%nlines)
                elif fname[16] == 'M':
                    legendtitle = ('%s_sim_1.6_0.3_1pc_S_1Myr'%nlines)
            elif fname[5:7] == '2r':
                if fname[16] == '1':
                    legendtitle = ('%s_sim_3.0_0.5_1pc_S_1000'%nlines)
                elif fname[16] == 'M':
                    legendtitle = ('%s_sim_3.0_0.5_1pc_S_1Myr'%(nlines))

        filename.append(legendtitle)

    # This saves all 20 simulations for a set of initial conditions into 1 single file
    All = []

    for n in range(nlines):
        All.append(dflist[n])

    All = pd.concat(All)


    return (All, filename)

#%% functions to calculate the velocity dispersion, virial velocity dispersion and
#IQR of all 20 simulations with the same initial conditions

def virial_radvelocity_dispersion(dflist, nlines):

    import numpy as np
    import astropy.units as u
    from astropy import constants as const

    nsnaps = 101
    strucpar = 10.
    kms = u.km / u.s

    for n in range(nlines):
        dflist[n].nstars = dflist[n].loc[0].index.size

        dflist[n].virzveldisp = []
        for ssnap in range(0, nsnaps):
            dflist_sorted = []
            summass = 0.
            halfmass = 0.
            cmass = 0.
            hmrad = 0.
            dflist_sorted = dflist[n].loc[ssnap].sort_values('radval')
            halfmass = (dflist[n].loc[ssnap]['mass'].sum()/2.)
            cmass = (dflist_sorted['mass'].cumsum())
            dflist_sorted['hmdif'] = np.absolute(cmass.subtract(halfmass))
            hmrad = dflist_sorted.loc[dflist_sorted['hmdif'].idxmin(), 'radval']*u.pc
            summass = dflist[n].loc[ssnap]['mass'].sum()*u.M_sun
            dflist[n].virzveldisp.append((np.sqrt((2.*summass.to(u.kg)*const.G)/\
                  (strucpar*hmrad.to(u.m)))).to(kms))

    return dflist.virzveldisp

def virial_space_velocity_dispersion(dflist, nlines):

    import numpy as np
    import astropy.units as u
    from astropy import constants as const
    nsnaps = 101
    strucpar = 10./3.
    kms = u.km / u.s

    for n in range(nlines):
        dflist[n].nstars = dflist[n].loc[0].index.size

        dflist[n].vir_spaceveldisp = []
        for ssnap in range(0, nsnaps):
            dflist_sorted = []
            summass = 0.
            halfmass = 0.
            cmass = 0.
            hmrad = 0.
            dflist_sorted = dflist[n].loc[ssnap].sort_values('radval')
            halfmass = (dflist[n].loc[ssnap]['mass'].sum()/2.)
            cmass = (dflist_sorted['mass'].cumsum())
            dflist_sorted['hmdif'] = np.absolute(cmass.subtract(halfmass))
            hmrad = dflist_sorted.loc[dflist_sorted['hmdif'].idxmin(), 'radval']*u.pc
            summass = dflist[n].loc[ssnap]['mass'].sum()*u.M_sun
            dflist[n].vir_spaceveldisp.append((np.sqrt((2.*summass.to(u.kg)*const.G)/\
                  (strucpar*hmrad.to(u.m)))).to(kms))


    return dflist.vir_spaceveldisp

#%% velocity dispersion - radial, PM and 3D velocity


def radvelocity_dispersion(datalist, nlines):
    import numpy as np
    import statistics
    nsnaps = 101

    zveldisp = np.zeros([nlines, nsnaps])
    for n in range(nlines):

        for ssnap in range(0, nsnaps):
#this adds zero as the value of the dispersion for any snapshot without velocities
            if len(datalist[n].loc[ssnap]) == 0:
                zveldisp[n, ssnap] = np.nan

            else:
                zveldisp[n, ssnap] = statistics.pstdev(datalist[n].loc[ssnap, 'zvel'])

    return zveldisp

def pmvelocity_dispersion(datalist, nlines):
    import numpy as np
    import statistics
    nsnaps = 101

    pmveldisp = np.zeros([nlines, nsnaps])
    for n in range(nlines):

        for ssnap in range(0, nsnaps):

            if len(datalist[n].loc[ssnap]) == 0:
                pmveldisp[n, ssnap] = np.nan
            else:
                pmveldisp[n, ssnap] = statistics.pstdev(datalist[n].loc[ssnap, 'PM-veldist'])

    return pmveldisp


def spacevelocity_dispersion(datalist, nlines):
    import numpy as np
    import statistics
    nsnaps = 101

    spaceveldisp = np.zeros([nlines, nsnaps])
    for n in range(nlines):

        for ssnap in range(0, nsnaps):

            if len(datalist[n].loc[ssnap]) == 0:
                spaceveldisp[n, ssnap] = np.nan
            else:
                spaceveldisp[n, ssnap] = statistics.pstdev(datalist[n].loc[ssnap, '3D-veldist'])

    return spaceveldisp


#%% median and min/max for radial, PM and space velocity dispsersions of 20 simulations

def dispersion_median_minmax(zveldisp):
    import numpy as np
    nsnaps = 101

    mindisp = np.zeros([nsnaps])
    maxdisp = np.zeros([nsnaps])
    mediandisp = np.zeros([nsnaps])

    for ssnap in range(nsnaps):
        maxdisp[ssnap] = np.nanmax(zveldisp[:, ssnap])
        mindisp[ssnap] = np.nanmin(zveldisp[:, ssnap])
#list of medians from all 20 simulations for each snapshot.
        mediandisp[ssnap] = np.nanmedian(zveldisp[:, ssnap])


    return (mediandisp, mindisp, maxdisp)

def pmdispersion_median_minmax(pmveldisp):
    import numpy as np
    nsnaps = 101

    mindisp = np.zeros([nsnaps])
    maxdisp = np.zeros([nsnaps])
    mediandisp = np.zeros([nsnaps])

    for ssnap in range(nsnaps):
        maxdisp[ssnap] = np.nanmax(pmveldisp[:, ssnap])
        mindisp[ssnap] = np.nanmin(pmveldisp[:, ssnap])
#list of medians from all 20 simulations for each snapshot.
        mediandisp[ssnap] = np.nanmedian(pmveldisp[:, ssnap])


    return (mediandisp, mindisp, maxdisp)


def spacedispersion_median_minmax(spaceveldisp):
    import numpy as np
    nsnaps = 101

    mindisp = np.zeros([nsnaps])
    maxdisp = np.zeros([nsnaps])
    mediandisp = np.zeros([nsnaps])

    for ssnap in range(nsnaps):
        maxdisp[ssnap] = np.nanmax(spaceveldisp[:, ssnap])
        mindisp[ssnap] = np.nanmin(spaceveldisp[:, ssnap])
#list of medians from all 20 simulations for each snapshot
        mediandisp[ssnap] = np.nanmedian(spaceveldisp[:, ssnap])

    return mediandisp, mindisp, maxdisp
#%% Interquartile range (radial and 3D)

def IQR_radvelocity_dispersion(dflist, nlines):
    import numpy as np
    nsnaps = 101
    for n in range(nlines):
        dflist[n].nstars = dflist[n].loc[0].index.size
        halfsnap = int(dflist[n].nstars/2.)

        dflist[n].zvelIQR = []
        for ssnap in range(0, nsnaps):
            dflist[n].reset_index(level=1)
            lowmedian = np.median(dflist[n].loc[ssnap].sort_values('zvel')[:halfsnap]['zvel'])
            upmedian = np.median(dflist[n].loc[ssnap].sort_values('zvel')\
                                 [halfsnap:int(dflist[n].nstars+1)]['zvel'])
            dflist[n].zvelIQR.append(0.741*(upmedian-lowmedian))

    return dflist.zvelIQR

def space_IQR_velocity_dispersion(dflist, nlines):
    import numpy as np
    nsnaps = 101

    for n in range(nlines):
        dflist[n].nstars = dflist[n].loc[0].index.size
        halfsnap = int(dflist[n].nstars/2.)

        dflist[n].space_IQR = []
        for ssnap in range(0, nsnaps):
            dflist[n].reset_index(level=1)
            lowmedian = np.median(dflist[n].loc[ssnap].sort_values('3D-veldist')\
                                  [:halfsnap]['3D-veldist'])
            upmedian = np.median(dflist[n].loc[ssnap].sort_values('3D-veldist')\
                                 [halfsnap:int(dflist[n].nstars+1)]['3D-veldist'])
            dflist[n].space_IQR.append(0.741*(upmedian-lowmedian))

    return dflist.space_IQR
