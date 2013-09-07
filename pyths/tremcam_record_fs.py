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

def showCharacteristics(matrixVar):
    print np.shape(matrixVar);
    shp = np.shape(matrixVar);
    print "[0]:",matrixVar[0,0]," [",shp[0]-1,"]:",matrixVar[shp[0]-1,0]," ms"
    fs = shp[0]/(matrixVar[shp[0]-1,0] -1)
    print "sampling frequency: ",fs
    return

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
    if (len(sys.argv) < 2):
        print "Usage: python tremcam_vis_basic.py hostname user_email" #`"sql query`""
        print "     : or ./tremcam_vis_basic.py hostname user_email"
        exit(0)
    else:
        host = sys.argv[1]
        user = sys.argv[2]
    
    mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')
    cur = mydb.cursor()
    
    # get mysql running average fft data for given user
    #statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE email =%s"""
    statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl 
		   WHERE subjectid  LIKE %s"""
    try:
        cur.execute(statement,(user))
        results = cur.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)    
    finally:
        if cur:
            cur.close()
    print "number of records for(", user, "): ", cur.rowcount
    #print "results:",type(results)
    
    xv = []
    yv = []
    zv = []
    tv = []

    for record in results:
        #print len(record)
        if len(record) == 4:
            xv.append(record[0])
            yv.append(record[1])
            zv.append(record[2])
            tv.append(record[3])

    ## setup plot
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.grid(True)
#plt.suptitle(query)
    ax1.set_title('X axis: All',fontsize=10)
#ax1.axhline(0, color='black', lw=1)
    ax2 = fig.add_subplot(212)
    ax2.grid(True)
	# setup 2D array
    N = int(len(xv))
    avgX = np.empty([10,N])
    avgY = np.empty([10,N])
    avgZ = np.empty([10,N])
    tsMtrx = np.empty([10,N])
            
    for i in range(0,N):
        xa  = [float(fv) for fv in xv[i].split(",")]
        avgX        = np.resize(avgX, (len(xa),N))
        avgX[:,i]   = [float(fv) for fv in xa]
        smoothedX = smoothListGaussian(xa)        
        #print "xa.len",len(xa)
        ta = [float(fv)/1e9 for fv in tv[i].split(",")]
        #tt = [float(fv-t[0]) for fv in t]
        tsMtrx        = np.resize(tsMtrx, (len(ta),N))
        tsMtrx[:,i] = [float(fv-ta[0]) for fv in ta]
        n = range(0,len(xa))
        #ax1.plot(n,tt)
        #ax1.plot(n, xa)
        ya  = [float(fv) for fv in yv[i].split(",")]
        n = range(0,len(ya))
        #ax1.plot(n, ya)
        avgY        = np.resize(avgY, (len(ya),N))
        avgY[:,i]   = [float(fv) for fv in ya]
        smoothedY = smoothListGaussian(ya)        
	# compute the frequency spectrum
    	fftSamples = 1024
    	window = hann(fftSamples/2)
    
	    # fft
        magsx = abs(fft(smoothedX)) #[1e3:1e3+fftSamples/2]*window))
        magsy = abs(fft(smoothedY)) #1e3:1e3+fftSamples/2]*window))
    	# convert to dB
        magsx = 20 * np.log10(magsx)
        magsy = 20 * np.log10(magsy)
	magsx -= max(magsx)
	magsy -= max(magsy)

	plt.xlim(0, 256)
	ax2.plot(magsx)
	ax2.plot(magsy)



        za = [float(fv) for fv in zv[i].split(",")]
        n = range(0,len(za))
        avgZ        = np.resize(avgZ, (len(za),N))
        avgZ[:,i]   = [float(fv) for fv in za]
        #ax3.plot(n, za)
        
    
    ax1.plot(tsMtrx)	
    showCharacteristics(tsMtrx)

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
