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
    #statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE email =%s"""
    statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE email LIKE %s"""
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
#n = []
    for record in results:
        #print len(record)
        if len(record) == 4:
            xv.append(record[0])
            yv.append(record[1])
            zv.append(record[2])
            tv.append(record[3])
# show each vector/list: print "xv:", xv
    print "length of xv:", len(xv)
    ## setup plot
    fig = plt.figure()
    ax1 = fig.add_subplot(231)
    ax1.grid(True)
#plt.suptitle(query)
    ax1.set_title('X axis: All',fontsize=10)
#ax1.axhline(0, color='black', lw=1)
    ax2 = fig.add_subplot(232)
    ax2.grid(True)
    #plt.suptitle(query)
    ax2.set_title('Y axis: All',fontsize=10)
    #ax1.axhline(0, color='black', lw=1)
    ax3 = fig.add_subplot(233)
    ax3.grid(True)
    #plt.suptitle(query)
    ax3.set_title('Z axis: All',fontsize=10)
    #ax1.axhline(0, color='black', lw=1)

    ax4 = fig.add_subplot(212)
    ax4.grid(True)
    #plt.suptitle(query)
    
    #ax1.axhline(0, color='black', lw=1)
#    ax3 = fig.add_subplot(313)
#    ax3.grid(True)
#    #plt.suptitle(query)
#    ax3.set_title('Z axis')
#    #ax1.axhline(0, color='black', lw=1)


    N = int(len(xv))
    avgX = np.empty([10,N])
    avgY = np.empty([10,N])
    avgZ = np.empty([10,N])
                
                #print "shape:", np.shape(avgX)

    for i in range(0,N):
        xa  = [float(fv) for fv in xv[i].split(",")]
        avgX        = np.resize(avgX, (len(xa),N))
        avgX[:,i]   = [float(fv) for fv in xa]
        #print "xa.len",len(xa)
        t = [float(fv)/1e9 for fv in tv[i].split(",")]
        tt = [float(fv-t[0]) for fv in t]
        n = range(0,len(xa))
        #ax1.plot(n,tt)
        ax1.plot(n, xa)
        ya  = [float(fv) for fv in yv[i].split(",")]
        n = range(0,len(ya))
        ax2.plot(n, ya)
        avgY        = np.resize(avgY, (len(ya),N))
        avgY[:,i]   = [float(fv) for fv in ya]
        
        za = [float(fv) for fv in zv[i].split(",")]
        n = range(0,len(za))
        avgZ        = np.resize(avgZ, (len(za),N))
        avgZ[:,i]   = [float(fv) for fv in za]
        ax3.plot(n, za)
        
    
    #print np.shape(avgX)
    meanVecX =np.mean(avgX,axis=1)
    meanVecY =np.mean(avgY,axis=1)
    meanVecZ =np.mean(avgZ,axis=1)

    smoothedX = smoothListGaussian(meanVecX)
    smoothedY = smoothListGaussian(meanVecY)
    smoothedZ = smoothListGaussian(meanVecZ)

    ax4.plot(range(0,len(smoothedX)),smoothedX,'r',label='X-Axis')
    ax4.plot(range(0,len(smoothedY)),smoothedY,'b',label='Y-Axis')
    ax4.plot(range(0,len(smoothedZ)),smoothedZ,'g',label='Z-Axis')
#             label=(['X-axis','Y-axis','Z-axis']))
#   ax4.legend(label =('X-axis','Y-axis','Z-axis'))
#ax4.legend(loc='best')
    leg = ax4.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
    leg.get_frame().set_alpha(0.5)
    


    # tweaks
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax3.get_yticklabels(), visible=False)
    majorLocator   = MultipleLocator(300)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator   = MultipleLocator(5)
    ## set axis range
    ax1.tick_params(axis='x', labelsize=10)
    ax1.xaxis.set_major_locator(majorLocator)
    ax1.xaxis.set_major_formatter(majorFormatter)
    x1,x2,y1,y2 = ax1.axis()
    ax1.axis((0,1.2e3,-1.0,1.0))
    ax2.axis((0,1.2e3,-1.0,1.0))
    ax3.axis((0,1.2e3,-1.0,1.0))
    ax4.axis((0,1.2e3,-1.0,1.0))
    
    ax2.tick_params(axis='x', labelsize=10)
    ax2.xaxis.set_major_locator(majorLocator)
    ax2.xaxis.set_major_formatter(majorFormatter)
    ax3.tick_params(axis='x', labelsize=10)
    ax3.xaxis.set_major_locator(majorLocator)
    ax3.xaxis.set_major_formatter(majorFormatter)
    ax1.set_ylabel('$m/s^2$')
    ax4.set_ylabel('$m/s^2$')
    ax4.set_xlabel('samples')
    ax4.set_title('Records averaged followed by a 5-Point Moving-Average Smoothing',fontsize=10)
    plt.suptitle('Baseline: smartphone at rest; sample size: n=%d'%(N),
                 fontsize=14)
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
