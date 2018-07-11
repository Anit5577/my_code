import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import pandas as pd
import matplotlib
import pickle
import os
import info_extract
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

def plotmixed(xmaster, vmaster,  IDs, t):

    fig = plt.figure(t)
    ax = fig.gca(projection='3d')

    n = len(xmaster[0][0])

    for star in range(n):

        
        if star in IDs[0]:
            ax.scatter(xmaster[0][t][star], xmaster[1][t][star], xmaster[2][t][star], s=0.25, color='dodgerblue')
            ax.quiver(xmaster[0][t][star], xmaster[1][t][star], xmaster[2][t][star], vmaster[0][t][star], vmaster[1][t][star], vmaster[2][t][star], length=0.1,  color='g')

        

        
        elif star in IDs[1]:
            ax.scatter(xmaster[0][t][star], xmaster[1][t][star], xmaster[2][t][star], s=0.25, color='r')
            ax.quiver(xmaster[0][t][star], xmaster[1][t][star], xmaster[2][t][star], vmaster[0][t][star], vmaster[1][t][star], vmaster[2][t][star], length=0.1, color='r')
            
                        

        
        else:
            ax.scatter(xmaster[0][t][star], xmaster[1][t][star], xmaster[2][t][star], s=0.25, color='k')
            ax.quiver(xmaster[0][t][star], xmaster[1][t][star], xmaster[2][t][star], vmaster[0][t][star], vmaster[1][t][star], vmaster[2][t][star], length=0.1, color='b')
            

            
    plt.show()


    return


#Set path to simulation
path = '/local/php17cs/backed_up_on_astro3/analysis/Binary_cluster_code/binary_clusters/a_binary_sim'

#Set time you want to plot at
#t =20

ID, tmaster, mmaster, xmaster, vmaster, n = info_extract.info_extract(path)
fname = path + '/identified_clusters.txt'
with open(fname, 'rb') as f:
    table = pickle.load(f)

#Add code to address and empty second cluster

#IDs = []
#IDs.append(table[t][0][0])
#IDs.append(table[t][1][0])

Unbound_list = pd.DataFrame(columns=['snapshot', 'star-ID']) 

for t in range(94,95):
    for star in range(1000):
        try:
            if star not in (table[t][0][0]):
                try:
                    if star not in (table[t][1][0]):
                        print (t, ID[star])  
                        Unbound_list = Unbound_list.append({'snapshot':t, 'star-ID' : ID[star]}, ignore_index=True)
                except (IndexError):
                    #print (t, ID[star])
                    Unbound_list = Unbound_list.append({'snapshot':t, 'star-ID' : ID[star]}, ignore_index=True)  

        except (IndexError):
            continue

#print (Unbound_list)                 
#Unbound_list.to_csv(path + '/Unbound_list_6.csv', sep=',' ,columns=['snapshot', 'star-ID'], index=False, header=True)
        