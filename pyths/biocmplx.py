#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__  = "Salvador Aguinaga"

import numpy as np
import pandas as pd 
import sys, string, os
import matplotlib.pyplot as plt

path = "/Users/saguinag/Research/BioComplexity/msim/"
if not os.path.exists(path):
  print 'no path'
  exit()
os.chdir( path )

df = pd.DataFrame.from_csv("garki_rainfall.csv", sep=',', header=None)
df.plot()#df.columns=['date','prain']
plt.show()

print df.head()
exit()

df.time = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df.set_index(['time'],inplace=True)
df.plot()
plt.savefig('temp.png')


