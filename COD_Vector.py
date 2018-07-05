#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:05:42 2017

@author: php17cs
"""

#import numpy as np

#COD_Vector calculates the vector of the centre of density for each snapshot
# results in an array cod(i,1:3) with i representing the snapshot and the 1:3 the three vector components -> to call the values for each dimension:
# x: cod[i,0], y: cod[i,1] and z: cod[i,2]


import F_COD_Vector1 as CV1


fname = input('Choose data file to be read into array: ')
nsnaps = 101
nstars = 1000

cod = CV1.cod_vector(fname,nsnaps,nstars)

print(cod)


  

            



