# this code calculates and plots the cumulative PM and 3D velocity for all snaps in all simulations that are read in from an input text file


import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib.ticker import AutoMinorLocator
from function_file import read_in_any_datafiles, velocity_elements, energy_stars, stars_in_outside_2HMR 

dflist,dname,nlines  = read_in_any_datafiles('file.txt') #this reads in the .dat files from an inputfile list

dflist = energy_stars(dflist,dname,nlines)       #this calculates the energy of each star in each snapshot an simulation and adds this in a column
dflist = velocity_elements(dflist,dname,nlines)  #this calculates the velocity by using the distance travelled between each snapshot and divides it by snapshot length - this is an alternative to the provided velocities from the simulation
dflist = stars_in_outside_2HMR(dflist,dname,nlines)  # this calculates the half-mass radius based on centre of density corrected locations and then adds a column identifying if the stars are inside or outside 2*HMR
   

filename = []

for fname in dname: # to allow the filename of the simulations to dictate the labels
        
    if fname[21] == 'E':
       if fname[17] == 'X':
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_1000.csv' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_500.csv' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_E_2000.csv' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = ('%s_sim_1.6_0.3_1pc_E_1000.csv'%nlines)
       elif fname[5:7] == '2r':
           legendtitle = ('%s_sim_3.0_0.5_1pc_E_1000.csv'%nlines)

    if fname[21] == 'S':
       if fname[17] == 'X':
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_1000.csv' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '5':
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_500.csv' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[17] == '2':    
           legendtitle = ('%s_sim_%s.%s_%s.%s_%spc_S_2000.csv' %(nlines,fname[7],fname[8],fname[22],fname[23],fname[12]))
       elif fname[5:7] == '1r':
           legendtitle = ('%s_sim_1.6_0.3_1pc_S_1000.csv'%nlines)
       elif fname[5:7] == '2r':
           legendtitle = ('%s_sim_3.0_0.5_1pc_S_1000.csv'%nlines)
    filename.append(legendtitle)


#
#dflistUB = []
#dflistESC = []
#dflistHMUB = []
#dflistHMESC = []
#dflistHMall = []
#dflistLMUB = []
#dflistLMESC = []
#dflistLMall =[]

#for n in range(nlines):
#    dflistUB.append(dflist[n].loc[dflist[n]['Unbound'] == True])
#    dflistESC.append(dflist[n].loc[dflist[n]['escaped'] == True]) #this creates 20 dataframes with the escaped star in each simulation
    
#    dflistHMUB.append(dflistUB[n].loc[dflistUB[n]['mass'] >= 8.])
#    dflistHMESC.append(dflistESC[n].loc[dflistESC[n]['mass'] >= 8.])
#    dflistHMall.append(dflist[n].loc[dflist[n]['mass'] >= 8.])
#    dflistLMUB.append(dflistUB[n].loc[dflistUB[n]['mass'] < 2.5])
#    dflistLMESC.append(dflistESC[n].loc[dflistESC[n]['mass'] < 2.5])
#    dflistLMall.append(dflist[n].loc[dflist[n]['mass'] < 2.5])


#UB =[]
#ESC =[]
All =[]
#HMall = []
#HMUB = []
#HMESC = []
#LMall = []
#LMUB = []
#LMESC = []

for n in range(nlines):
    All.append(dflist[n])
#    UB.append(dflistUB[n])
#    ESC.append(dflistESC[n]) 
#    HMUB.append(dflistHMUB[n])
#    HMESC.append(dflistHMESC[n])    
#    HMall.append(dflistHMall[n])
#    LMUB.append(dflistLMUB[n])
#    LMESC.append(dflistLMESC[n])    
#    LMall.append(dflistLMall[n])


All = pd.concat(All)      
#UB = pd.concat(UB)
#ESC = pd.concat(ESC)
#HMUB = pd.concat(HMUB)
#HMESC = pd.concat(HMESC)
#HMall = pd.concat(HMall)
#LMUB = pd.concat(LMUB)
#LMESC = pd.concat(LMESC)
#LMall = pd.concat(LMall)

sub_select_list = [All] # add more dataframes, if other combined files are needed
filename_list = ['All'] # add corresponding names for the new files.

#sub_select_list = [UB,ESC,All,HMUB,HMESC,HMall]
#filename_list = ['UB','ESC','All','HMUB','HMESC','HMall']

for i in sub_select_list:
    for j in filename_list:
        i.to_csv('%s_%s' %(j,filename[0]),columns = ['snap','star','time','mass','PM-veldist','3D-veldist','Unbound','escaped'],index=['snap','star'])
        
#%% Code to use to read in combined datafiles with columns as above

#
#for j in filename_list:
#    All_read = pd.read_csv('%s_%s' %(j,filename[0]),index_col=['snap','star'],usecols=['snap','star','time','mass','PM-veldist','3D-veldist','Unbound','escaped'])        
# 
#print (All_read)       