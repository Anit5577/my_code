#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:02:14 2017

@author: php17cs
"""


f = open('file.txt')
lines = [line.rstrip('\n') for line in f]
f.close()

nlines = len(lines)

x=[]
fname=[]

for x in range(1,nlines+1,1):
    x = lines[x-1]
    fname.append(x)
    
df=[]
for x in range (1,nlines+1,1):
    x = 'df' + str(x) 
    df.append(x)
    
print (df)    
