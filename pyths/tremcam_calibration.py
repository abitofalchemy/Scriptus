#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import sys, string
import scipy, math
#from scipy.io.wavfile import read
from scipy.signal import hann
from scipy.fftpack import fft
from scipy.fftpack import rfft
import matplotlib.pyplot as plt
import MySQLdb
###################################
def get_fft_mysql(email, cur):
    statement = """SELECT fft_result from TremCamTbl WHERE email =%s"""   
    try:
        cur.execute(statement,(email))
        results = cur.fetchall()
    except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
    
    return results

def main():
    # input data
    if (len(sys.argv) < 1):
        print "Usage: python tremcam_calibration.py hostname user_email" #`"sql query`""
        exit(0)
    else:
        host = sys.argv[1]
        user = sys.argv[2]
    
    mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')
    cur = mydb.cursor()
    
    # generate sinusoidal data
    t = np.arange(512)
    y=np.sin(t/3)+np.cos(t/5)
    window = hann(256)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax1.set_title('Time domain')
    ax1.plot(t,y)
    ax2 = fig.add_subplot(312)
    ax2.grid(True)
    # fft        
    mags = abs(fft(y[0:256]*window))
    # convert to dB
    mags = 20 * np.log10(mags)
    mags -= max(mags)
    plt.xlim(0, 128)
    ax2.plot(mags)
    ax2.set_title('Magnitude (normalized to 0dB)')
    #plt.show()
    #freq_data = ','.join(map(str, mags))
    
    # get mysql running average fft data for given user
    statement = """SELECT fft_result from TremCamTbl WHERE email =%s"""   
    try:
        cur.execute(statement,(user))
        results = cur.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)    
    finally:
        if cur:
            cur.close()
    print "results:",type(results)
    magn = []
    for record in results:
        if (len(record)> 0):
            magn.append(record[0])
    print "int(len(magn)):",int(len(magn))
    y  = [float(fv) for fv in magn[0].split(",")] 
    n = range(0,len(y))
    

    # plot data 
    ax3 = fig.add_subplot(313)
    ax3.grid(True)
    plt.xlim(0, 128)
    ax3.plot(n,y)
    ax3.set_title('From mySQL Magnitude (normalized to 0dB)')
    plt.show()

    

## main
if __name__ == '__main__':
    main()


#query = "SELECT accelX FROM TremCamTbl WHERE email='saguinag@nd.edu'"
#cursor.execute(query)
#result = cursor.fetchall()
#input_data = []
#for record in result:
#    print "len(record)" , len(record)
#    if len(record)>0:
#        input_data.append(record[0])
#    
#input_data = read("cello.wav")
#print len(input_data)
#audio = input_data[0]
#for i in (range(10)):
#	print i,":",audio[100+i]
#
#N=len(audio)
#print "N=len(audio):",N
### plot time domain data
#plt.plot(audio)
#plt.ylabel("Amplitude")
#plt.xlabel("Time (samples)")
## set the title
#plt.title("Accelerometer X-axis")
#plt.show()
