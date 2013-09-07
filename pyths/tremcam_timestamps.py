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
    statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE email =%s"""
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
    # initialize array
    tv = []
    for record in results:
        #print len(record)
        if len(record) == 4:
            tv.append(record[3])
# show each vector/list: print "xv:", xv
    print "length of tv:", len(tv)
    ## setup plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.grid(True)
    plt.suptitle(statement)
#ax1.set_title('X axis: All',fontsize=10)
#ax1.axhline(0, color='black', lw=1)
#ax1.axhline(0, color='black', lw=1)
    N = int(len(tv))
    avgTs = np.empty([10,N])
                
                #print "shape:", np.shape(avgX)

    for i in range(0,N):
        ta  = [float(fv) for fv in tv[i].split(",")]
        avgTs        = np.resize(avgTs, (len(ta),N))
        avgTs[:,i]   = [float(fv) for fv in ta]
        print "ta.len",len(ta)
        print "diff:",( avgTs[len(avgTs[1,:])-1,i] - avgTs[0,i])/1e8," s"
        #ax1.plot(ta)

    print np.shape(avgTs)
#    ax1.plot(np.min(avgTs,axis=1))
#    ax1.plot(np.mean(avgTs,axis=1))
#    ax1.plot( np.max(avgTs,axis=1))
    print len(avgTs[:,0])
    print len(avgTs[:,1])
#    print avgTs[0,0]
    print avgTs[0,1],":",avgTs[len(avgTs[1,:])-1,1]
    print "diff:",( avgTs[len(avgTs[1,:])-1,1] - avgTs[0,1])/1e9," s"

#    ax1.plot(np.mean(avgTs,axis=1))
#    ax1.plot( np.max(avgTs,axis=1))

#    #print np.shape(avgX)
#    meanVecX =np.mean(avgX,axis=1)
#    meanVecY =np.mean(avgY,axis=1)
#    meanVecZ =np.mean(avgZ,axis=1)
#
#    smoothedX = smoothListGaussian(meanVecX)
#    smoothedY = smoothListGaussian(meanVecY)
#    smoothedZ = smoothListGaussian(meanVecZ)
#
#    ax4.plot(range(0,len(smoothedX)),smoothedX,'r',label='X-Axis')
#    ax4.plot(range(0,len(smoothedY)),smoothedY,'b',label='Y-Axis')
#    ax4.plot(range(0,len(smoothedZ)),smoothedZ,'g',label='Z-Axis')
##             label=(['X-axis','Y-axis','Z-axis']))
##   ax4.legend(label =('X-axis','Y-axis','Z-axis'))
##ax4.legend(loc='best')
#    leg = ax4.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
#    leg.get_frame().set_alpha(0.5)
#    
#
#
#    # tweaks
#    plt.setp(ax2.get_yticklabels(), visible=False)
#    plt.setp(ax3.get_yticklabels(), visible=False)
#    majorLocator   = MultipleLocator(300)
#    majorFormatter = FormatStrFormatter('%d')
#    minorLocator   = MultipleLocator(5)
#    ## set axis range
#    ax1.tick_params(axis='x', labelsize=10)
#    ax1.xaxis.set_major_locator(majorLocator)
#    ax1.xaxis.set_major_formatter(majorFormatter)
#    x1,x2,y1,y2 = ax1.axis()
#    numsamp = int(len(meanVecX))
#    ax1.axis((0,numsamp-1,-1.0,1.0))
#    ax2.axis((0,numsamp-1,-1.0,1.0))
#    ax3.axis((0,numsamp-1,-1.0,1.0))
#    ax4.axis((0,numsamp-1,-1.0,1.0))
#    
#    ax2.tick_params(axis='x', labelsize=10)
#    ax2.xaxis.set_major_locator(majorLocator)
#    ax2.xaxis.set_major_formatter(majorFormatter)
#    ax3.tick_params(axis='x', labelsize=10)
#    ax3.xaxis.set_major_locator(majorLocator)
#    ax3.xaxis.set_major_formatter(majorFormatter)
#    ax1.set_ylabel('$m/s^2$')
#    ax4.set_ylabel('$m/s^2$')
#    ax4.set_xlabel('samples')
#    ax4.set_title('Records averaged followed by a 5-Point Moving-Average Smoothing',fontsize=10)
#    plt.suptitle('Baseline: smartphone at rest; sample size: n=%d'%(N),
#                 fontsize=14)
#
#    # compute the frequency spectrum
#    fftSamples = 1024
#    window = hann(fftSamples/2)
#    
#    # fft
#    mags = abs(fft(smoothedY[0:fftSamples/2]*window))
#    # convert to dB
#    mags = 20 * np.log10(mags)
#    mags -= max(mags)
#    plt.xlim(0, 256)
#    ax5.tick_params(axis='x', labelsize=8)
#    ax5.tick_params(axis='y', labelsize=8)
#    ax5.plot(mags)
#    ax5.set_title('Magnitude (normalized to 0dB)', fontsize=8)

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
