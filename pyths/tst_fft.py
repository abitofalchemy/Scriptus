#!/usr/bin/python
# -*- coding: utf-8 -*-
# tst_fft  test the fft from 'HOSTNAME'
#          accelX
# usage:  tst_fft hostname 


import numpy as np
import sys
import scipy
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import MySQLdb, csv, StringIO

# input data
if (len(sys.argv) < 1):
    print "Usage: python plotmysql.py hostname" #`"sql query`""
    exit(0)

#db = MySQLdb.connect(sys.argv[1],'tremcam','trem00xB','neurobit')
db = MySQLdb.connect('192.168.1.148','tremcam','trem00xB','neurobit')
mCursor = db.cursor()
query = "SELECT accelX FROM TremCamTbl WHERE email='saguinag@nd.edu'"
mCursor.execute(query)
result = mCursor.fetchall()
input_data  = []
a = []

for record in result:
    print "len(record)" , len(record)
    if len(record)>0:
        input_data.append(record[0])
    
signal = input_data[0].split(',')
signal = np.array(signal)

## plot time domain data
plt.plot(signal)
plt.ylabel("Amplitude")
plt.xlabel("Time (samples)")
### set the title
plt.title("Accelerometer X-axis")
plt.show()
