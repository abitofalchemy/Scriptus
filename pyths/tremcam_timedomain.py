#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import sys, string
import scipy, math
#from scipy.io.wavfile import read8
from scipy.signal import hann
from scipy.fftpack import fft
from scipy.fftpack import rfft
import matplotlib.pyplot as plt
import MySQLdb
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.lines import Line2D
import matplotlib.font_manager
# global sets
leg_prop = matplotlib.font_manager.FontProperties(size=8)
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
    if (len(sys.argv) < 3):
        print "Usage:   ./tremcam_timedomain.py hostname email[,email2]"
        exit(0)
    else:
        host = sys.argv[1]
        user = sys.argv[2]
    
    print len(sys.argv)


    mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')
#cur = mydb.cursor()
    
    # get mysql running average fft data for given user
    statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl 
                   WHERE email LIKE %s"""
    #statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl 
    #		   WHERE subjectid  LIKE %s"""

    ## setup plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    #ax1.axis('off')
    ax1.set_frame_on(False)
    ax1.get_xaxis().tick_bottom()
    ax1.axes.get_yaxis().set_visible(False)
    xmin, xmax = ax1.get_xaxis().get_view_interval()
    ymin, ymax = ax1.get_yaxis().get_view_interval()
    
    for i in range(0,len(sys.argv) - 2):
        try:
            user = sys.argv[i+2]
            print user
            cur = mydb.cursor()
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

    
    
        # setup 2D array
        N = int(len(xv))
        avgX = np.zeros([10,N])
        avgY = np.zeros([10,N])
        avgZ = np.zeros([10,N])
        tsMtrx = np.zeros([10,N])
        tmpA = np.zeros([10,N])
                
        for i in range(0,N):
            ta = [float(fv)/1e9 for fv in tv[i].split(",")]
            xa  = [float(fv) for fv in xv[i].split(",")]
            ya  = [float(fv) for fv in yv[i].split(",")]
            za  = [float(fv) for fv in zv[i].split(",")]
            lN = len(xa)
            if ( len(xa) > len(avgX[:,i]) ):
                avgX        = np.resize(avgX, (len(xa),N))
                avgY        = np.resize(avgY, (len(ya),N))
                avgZ        = np.resize(avgZ, (len(za),N))
                tsMtrx      = np.resize(tsMtrx, (len(ta),N))
            
            smoothedX = smoothListGaussian(xa)        
            smoothedY = smoothListGaussian(ya)        
            smoothedZ = smoothListGaussian(za)        
            tsMtrx[range(0,len(ta)),i] = [float(fv-ta[0]) for fv in ta]
            #avgX  [range(0,len(xa)),i] = [smoothedX]
            for l in range(0,len(smoothedX)):
                avgX[l,i] = smoothedX[l]
                avgY[l,i] = smoothedY[l]
                avgZ[l,i] = smoothedZ[l]
            #end for loop

        print len(tsMtrx[:,0]),",",np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])
        tStep = np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])

        timeV = np.arange(0, np.max(np.max(tsMtrx,axis=0)), tStep)
        if len(timeV) > len(avgX[:,0]):
            timeV = np.resize(timeV, (len(avgX[:,0]),1))
        print len(timeV),",", np.shape(avgX)
        #ax1.plot(timeV, np.mean(avgX,axis=1),label="X-axis")
        #ax1.plot(timeV, np.mean(avgY,axis=1),label="Y-axis (averaged)")
        K = np.floor(len(timeV)/2)
        ax1.plot(timeV[0:K], avgY[0:K,3],label="Y-axis (4Hz typical stimulus)")
        #ax1.plot(timeV, np.mean(avgZ,axis=1),label="Z-axis")
        leg = ax1.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
        leg.get_frame().set_alpha(0.5)
        #ax1.set_ylabel('Acceleration $m/s^2$')
        #ax1.set_xlabel("Time (s)")
        #plt.suptitle(user)
        x1,x2,y1,y2 = ax1.axis()
        #print x1,",",x2
        #ax1.add_line(Line2D([0.5, 0.5], [0, 1], transform=ax1.transAxes,
        #              linewidth=2, color='b'))
        majorLocator   = MultipleLocator(5)
        majorFormatter = FormatStrFormatter('%d')
        minorLocator   = MultipleLocator(1)
        ## set axis range
        ax1.tick_params(axis='x', labelsize=10)
        ax1.xaxis.set_major_locator(majorLocator)
        ax1.xaxis.set_major_formatter(majorFormatter)
        ax1.minorticks_on()
        ax1.add_artist(Line2D((x1, x2), (y1, y1), color='black', linewidth=2))
        #ax1.axis([x2*.3,x2*.7,y1,y2])
    ## end major for loop
            
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
