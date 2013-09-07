#!/usr/bin/python
# -*- coding: utf-8 -*-
# tremcam_caltst  calibration test
# --------------
# Designed for the TremCam project


import numpy as np
import sys, string
import scipy, math
#from scipy.io.wavfile import read
from scipy.signal import hann
from scipy.fftpack import fft
from scipy.fftpack import rfft
import matplotlib.pyplot as plt
import MySQLdb
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.font_manager
leg_prop = matplotlib.font_manager.FontProperties(size=10)
###################################

### This is the Gaussian data smoothing function I wrote ###
##  http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
##  code from SWHarden
def smoothListGaussian(list,degree=5):
    
    window=degree*2-1
    
    weight=np.array([1.0]*window)
    
    weightGauss=[]
    
    for i in range(window):
        
        i=i-degree+1
        
        frac=i/float(window)
        
        gauss=1/(np.exp((4*(frac))**2))
        
        weightGauss.append(gauss)
    
    weight=np.array(weightGauss)*weight
    
    smoothed=[0.0]*(len(list)-window)
    
    for i in range(len(smoothed)):  
        
        smoothed[i]=sum(np.array(list[i:i+window])*weight)/sum(weight)
    
    return smoothed

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
    ## setup plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.grid(True)
    ax1.set_title('Accelerometer Calibration',fontsize=10)


    minF = 1
    maxF = 20
    ax1.plot(range(minF,maxF),range(minF,maxF),':k', label="Nexus S")
    ax1.plot(range(minF,maxF),range(minF,maxF),':r', label="LG Ignite")
    ax1.plot(range(minF,maxF),range(minF,maxF),':g', label="Droid 4")
    ax1.plot(range(minF,maxF),range(minF,maxF),':b', label="HTC Amaze 4G")
    plt.minorticks_on()
    
    leg = ax1.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
    leg.get_frame().set_alpha(0.5)

    ax1.set_ylabel('Frequency (Hz): Measured')
    ax1.set_xlabel('Frequency (Hz): Stimulus Frequency')
    #ax1.set_title('',fontsize=10)
    #plt.suptitle('Baseline: smartphone at rest; sample size: n=%d'%(N),
    #             fontsize=14)
    plt.draw()

    ## generate an image file
    F = plt.gcf()
    DPI = F.get_dpi()
    F.savefig('images/figplot.png',dpi = (150))


    

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
