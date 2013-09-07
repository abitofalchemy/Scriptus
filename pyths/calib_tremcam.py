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

def compute_plot_fft(data, nsmp, fs, pHndlr):
    # 'data' consists of x = time vector
    #                    y = data vector
    window  = hann(nsmp)
    print np.shape(data)
    mag_spectrum_x = np.zeros([nsmp,len(data[:,0])/nsmp])
    mag_spectrum_y = np.zeros([nsmp,len(data[:,1])/nsmp])
    output_vec = np.zeros(nsmp)
#    avgXaxis = np.mean(data[:,0],axis=1)
#    avgYaxis = np.mean(data[:,0],axis=1)
    
    # average 
    for k in range(0,len(data[:,0])/nsmp):
    
        sliceY = data[k*nsmp:nsmp*(k+1),1]
        #multiply it with the window and transform it into frequency domain
        #spectrumx = fft(sliceX*window);
        spectrumy = fft(sliceY*window);
        #get the spectrum magnitude at each of the 256 frequency points and store it
        #mag_spectrum_x[:,k]= 20 * np.log10(abs(spectrumx))
        mag_spectrum_y[:,k]= 20 * np.log10(abs(spectrumy))
    
#    mean_spec_mtrx_x = np.mean(mag_spectrum_x, axis=1)
#    mean_spec_mtrx_x -= max(mean_spec_mtrx_x)
    mean_spec_mtrx_y = np.mean(mag_spectrum_y, axis=1)
    mean_spec_mtrx_y -= max(mean_spec_mtrx_y)
    #output_vec[0] = mean_spectrum[0];
    #output_vec[1:126] = 1/2*(mean_spectrum[1:126]+mean_spectrum[254:-1:128]);
    #output_vec[127] = mean_spectrum[127];
    n = nsmp # length of the signal
    k = np.arange(n)
    T = n/fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range
    #print len(frq)
    #print len(mean_spec_mtrx_x[0:numsamp/2])

    pHndlr.plot(frq,mean_spec_mtrx_x[0:numsamp/2],label="X-axis");
    pHndlr.plot(frq,mean_spec_mtrx_y[0:numsamp/2],label="Y-axis");
    pHndlr.set_ylabel("Magnitude (dB)")
    x1,x2,y1,y2 = pHndlr.axis()
    pHndlr.axis([x1,x2/2,y1,y2])
    pHndlr.minorticks_on()
    leg = pHndlr.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
    leg.get_frame().set_alpha(0.5)


def main():
    # input data
    if (len(sys.argv) < 2):
        print "Usage:   ./calib_tremcam.py hostname email1 email2 ..."
        exit(0)
    else:
        host = sys.argv[1]
        
    mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')

    # get mysql running average fft data for given user
    statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl 
                   WHERE email LIKE %s"""
    #statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl 
    #		   WHERE subjectid  LIKE %s"""

    ## setup plot
    fig = plt.figure()
    ax1 = fig.add_subplot(231)
    #ax1.axis('off')
    ax1.set_frame_on(False)
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()
    #ax1.axes.get_yaxis().set_visible(False)
    xmin, xmax = ax1.get_xaxis().get_view_interval()
    ymin, ymax = ax1.get_yaxis().get_view_interval()
    
    ax2 = fig.add_subplot(232)
    #ax1.axis('off')
    ax2.set_frame_on(False)
    ax2.get_xaxis().tick_bottom()
    ax2.axes.get_yaxis().set_visible(False)
    xmin, xmax = ax2.get_xaxis().get_view_interval()
    ymin, ymax = ax2.get_yaxis().get_view_interval()

    ax3 = fig.add_subplot(233)
    #ax1.axis('off')
    ax3.set_frame_on(False)
    ax3.get_xaxis().tick_bottom()
    ax3.axes.get_yaxis().set_visible(False)
    xmin, xmax = ax3.get_xaxis().get_view_interval()
    ymin, ymax = ax3.get_yaxis().get_view_interval()
    
    ax4 = fig.add_subplot(233)
    #ax1.axis('off')
    ax4.set_frame_on(False)
    ax4.get_xaxis().tick_bottom()
    ax4.axes.get_yaxis().set_visible(False)
    xmin, xmax = ax4.get_xaxis().get_view_interval()
    ymin, ymax = ax4.get_yaxis().get_view_interval()
    dat_mtrx = []
    
    for ix in range(0, len(sys.argv) -2 ):
        try:
            user = sys.argv[ix+2]
            print user,"i:",ix
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

        tStep = np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])

        timeV = np.arange(0, np.max(np.max(tsMtrx,axis=0)), tStep)
        if len(timeV) > len(avgX[:,0]):
            timeV = np.resize(timeV, (len(avgX[:,0]),1))
        #######
        if (ix == 0):
            print np.shape(avgY)
            K = np.floor(len(timeV)/2)
            ax1.plot(timeV[0:K], avgY[0:K,0],label="2Hz stimulus; Y-axis")
            #ax1.plot(timeV, avgY[:,1],label="2Hz stimulus; Y-axis")
            ax1.set_ylabel("Acceleration ($m/s^2$)", fontsize=10)
            leg = ax1.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
            leg.get_frame().set_alpha(0.5)
            x1,x2,y1,y2 = ax1.axis()
            majorLocator   = MultipleLocator(5)
            majorFormatter = FormatStrFormatter('%d')
            minorLocator   = MultipleLocator(1)
            ## set axis range
            ax1.tick_params(axis='x', labelsize=10)
            ax1.xaxis.set_major_locator(majorLocator)
            ax1.xaxis.set_major_formatter(majorFormatter)
            ax1.minorticks_on()
            ax1.tick_params(axis='y', labelsize=10)
            ax1.axis([x2*.1,x2*.7,-5,+6])
            x1,x2,y1,y2 = ax1.axis()
            ax1.add_artist(Line2D((x1, x2), (y1, y1), color='black', linewidth=2))
            ax1.add_artist(Line2D((x1, x1), (y1, y2), color='black', linewidth=2))

        elif (ix == 1):
            K = np.floor(len(timeV)/2)
            ax2.plot(timeV[0:K], avgY[0:K,0],label="3Hz stimulus; Y-axis")
            leg = ax2.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
            leg.get_frame().set_alpha(0.5)
            x1,x2,y1,y2 = ax2.axis()
            ax2.axis([x2*.4,x2,-5,+6])
            majorLocator   = MultipleLocator(5)
            majorFormatter = FormatStrFormatter('%d')
            minorLocator   = MultipleLocator(1)
            ## set axis range
            ax2.tick_params(axis='x', labelsize=10)
            ax2.xaxis.set_major_locator(majorLocator)
            ax2.xaxis.set_major_formatter(majorFormatter)
            ax2.minorticks_on()
            x1,x2,y1,y2 = ax2.axis()
            ax2.add_artist(Line2D((x1, x2), (y1, y1), color='black', linewidth=2))
        
        elif (ix == 2):
            K = np.floor(len(timeV))
            ax3.plot(timeV[0:K], avgY[0:K,0],label="4Hz stimulus; Y-axis")
            print "fs = ",len(timeV[0:K])/np.max(np.max(timeV,axis=0))
            fs = len(timeV[0:K])/np.max(np.max(timeV,axis=0))
            dat_mtrx = np.mat([[x for x in timeV[0:K]],[x for x in avgY[0:K,0]]])
            compute_plot_fft(dat_mtrx.conj().transpose(), 512, fs, ax4)
            
            leg = ax3.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
            leg.get_frame().set_alpha(0.5)
            x1,x2,y1,y2 = ax3.axis()
            ax3.axis([x2*.4,x2*.75,-5,+6])
            majorLocator   = MultipleLocator(10)
            majorFormatter = FormatStrFormatter('%d')
            minorLocator   = MultipleLocator(1)
            ## set axis range
            ax3.tick_params(axis='x', labelsize=10)
            ax3.xaxis.set_major_locator(majorLocator)
            ax3.xaxis.set_major_formatter(majorFormatter)
            ax3.minorticks_on()
            x1,x2,y1,y2 = ax3.axis()
            ax3.add_artist(Line2D((x1, x2), (y1, y1), color='black',
                                  linewidth=2))
        
#        ## do dps
#        fft_dat = compute_fft([], nbrSmp, fs)
#                
#        ax2.plot(frq,mean_spec_mtrx_x[0:numsamp/2],label="X-axis");
#        ax2.plot(frq,mean_spec_mtrx_y[0:numsamp/2],label="Y-axis");
#        ax2.set_ylabel("Magnitude (dB)")
#        x1,x2,y1,y2 = ax2.axis()
#        ax2.axis([x1,x2/2,y1,y2])
#        ax2.minorticks_on()
#        leg = ax2.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
#        leg.get_frame().set_alpha(0.5)
    
        #######
        # do dsp
#        print "fs = ",len(tsMtrx[:,0])/np.max(np.max(tsMtrx,axis=0))
#        fs = len(tsMtrx[:,0])/np.max(np.max(tsMtrx,axis=0))
#        numsamp = 1024
#        window  = hann(numsamp)
#
#        avgXaxis = np.mean(avgX,axis=1)
#        avgYaxis = np.mean(avgY,axis=1)
#        #print np.shape(avgXaxis)
#        mag_spectrum_x = np.zeros([numsamp,len(tsMtrx[:,0])/numsamp])
#        mag_spectrum_y = np.zeros([numsamp,len(tsMtrx[:,0])/numsamp])
#        output_vec = np.zeros(numsamp)
#
#        for k in range(0,len(tsMtrx[:,0])/numsamp):
#            sliceX = avgXaxis[k*numsamp:numsamp*(k+1)]
#            sliceY = avgYaxis[k*numsamp:numsamp*(k+1)]
#            #multiply it with the window and transform it into frequency domain
#            spectrumx = fft(sliceX*window);
#            spectrumy = fft(sliceY*window);
#            #get the spectrum magnitude at each of the 256 frequency points and store it
#            mag_spectrum_x[:,k]= 20 * np.log10(abs(spectrumx))
#            mag_spectrum_y[:,k]= 20 * np.log10(abs(spectrumy))
#
#        mean_spec_mtrx_x = np.mean(mag_spectrum_x, axis=1)
#        mean_spec_mtrx_x -= max(mean_spec_mtrx_x)
#        mean_spec_mtrx_y = np.mean(mag_spectrum_y, axis=1)
#        mean_spec_mtrx_y -= max(mean_spec_mtrx_y)
#        #output_vec[0] = mean_spectrum[0];
#        #output_vec[1:126] = 1/2*(mean_spectrum[1:126]+mean_spectrum[254:-1:128]);
#        #output_vec[127] = mean_spectrum[127];
#        n = numsamp # length of the signal
#        k = np.arange(n)
#        T = n/fs
#        frq = k/T # two sides frequency range
#        frq = frq[range(n/2)] # one side frequency range
#        print len(frq)
#        print len(mean_spec_mtrx_x[0:numsamp/2])
#
#        ax4 = fig.add_subplot(234)
#        #ax2.plot(frq,mean_spec_mtrx_x[0:numsamp/2],label="X-axis");
#        ax4.plot(frq,mean_spec_mtrx_y[0:numsamp/2],label="Y-axis");
#        ax4.set_ylabel("Magnitude (dB)")
#        x1,x2,y1,y2 = ax4.axis()
#        ax4.axis([x1,x2/2,y1,y2])
#        ax4.minorticks_on()
#        leg = ax4.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
#        leg.get_frame().set_alpha(0.5)

    #ends for
    ###########################################################################
    
                
#    user = 'sa_jr%'
#    
#
#    try:
#        #user = sys.argv[i+2]
#        print user
#        cur = mydb.cursor()
#        cur.execute(statement,(user))
#        results = cur.fetchall()
#    except MySQLdb.Error, e:
#        print "Error %d: %s" % (e.args[0], e.args[1])
#        sys.exit(1)
#    finally:
#        if cur:
#            cur.close()
#    print "number of records for(", user, "): ", cur.rowcount
#    #print "results:",type(results)
#
#    xv = []
#    yv = []
#    zv = []
#    tv = []
#
#    for record in results:
#        #print len(record)
#        if len(record) == 4:
#            xv.append(record[0])
#            yv.append(record[1])
#            zv.append(record[2])
#            tv.append(record[3])
#
#
#
#    # setup 2D array
#    N = int(len(xv))
#    avgX = np.zeros([10,N])
#    avgY = np.zeros([10,N])
#    avgZ = np.zeros([10,N])
#    tsMtrx = np.zeros([10,N])
#    tmpA = np.zeros([10,N])
#
#    for i in range(0,N):
#        ta = [float(fv)/1e9 for fv in tv[i].split(",")]
#        xa  = [float(fv) for fv in xv[i].split(",")]
#        ya  = [float(fv) for fv in yv[i].split(",")]
#        za  = [float(fv) for fv in zv[i].split(",")]
#        lN = len(xa)
#        if ( len(xa) > len(avgX[:,i]) ):
#            avgX        = np.resize(avgX, (len(xa),N))
#            avgY        = np.resize(avgY, (len(ya),N))
#            avgZ        = np.resize(avgZ, (len(za),N))
#            tsMtrx      = np.resize(tsMtrx, (len(ta),N))
#        
#        smoothedX = smoothListGaussian(xa)
#        smoothedY = smoothListGaussian(ya)
#        smoothedZ = smoothListGaussian(za)
#        tsMtrx[range(0,len(ta)),i] = [float(fv-ta[0]) for fv in ta]
#        #avgX  [range(0,len(xa)),i] = [smoothedX]
#        for l in range(0,len(smoothedX)):
#            avgX[l,i] = smoothedX[l]
#            avgY[l,i] = smoothedY[l]
#            avgZ[l,i] = smoothedZ[l]
#    #end for loop
#
#    tStep = np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])
#
#    timeV = np.arange(0, np.max(np.max(tsMtrx,axis=0)), tStep)
#    if len(timeV) > len(avgX[:,0]):
#        timeV = np.resize(timeV, (len(avgX[:,0]),1))
#    #######
#    ax2.plot(timeV, avgY[:,1],label="3Hz stimulus; Y-axis")
#    #######
#    
#    ###########################################################################
#    user = 'test@nd.edu'
#    
#
#    try:
#        #user = sys.argv[i+2]
#        print user
#        cur = mydb.cursor()
#        cur.execute(statement,(user))
#        results = cur.fetchall()
#    except MySQLdb.Error, e:
#        print "Error %d: %s" % (e.args[0], e.args[1])
#        sys.exit(1)
#    finally:
#        if cur:
#            cur.close()
#    print "number of records for(", user, "): ", cur.rowcount
#    #print "results:",type(results)
#
#    xv = []
#    yv = []
#    zv = []
#    tv = []
#
#    for record in results:
#        #print len(record)
#        if len(record) == 4:
#            xv.append(record[0])
#            yv.append(record[1])
#            zv.append(record[2])
#            tv.append(record[3])
#
#
#
#    # setup 2D array
#    N = int(len(xv))
#    avgX = np.zeros([10,N])
#    avgY = np.zeros([10,N])
#    avgZ = np.zeros([10,N])
#    tsMtrx = np.zeros([10,N])
#    tmpA = np.zeros([10,N])
#
#    for i in range(0,N):
#        ta = [float(fv)/1e9 for fv in tv[i].split(",")]
#        xa  = [float(fv) for fv in xv[i].split(",")]
#        ya  = [float(fv) for fv in yv[i].split(",")]
#        za  = [float(fv) for fv in zv[i].split(",")]
#        lN = len(xa)
#        if ( len(xa) > len(avgX[:,i]) ):
#            avgX        = np.resize(avgX, (len(xa),N))
#            avgY        = np.resize(avgY, (len(ya),N))
#            avgZ        = np.resize(avgZ, (len(za),N))
#            tsMtrx      = np.resize(tsMtrx, (len(ta),N))
#        
#        smoothedX = smoothListGaussian(xa)
#        smoothedY = smoothListGaussian(ya)
#        smoothedZ = smoothListGaussian(za)
#        tsMtrx[range(0,len(ta)),i] = [float(fv-ta[0]) for fv in ta]
#        #avgX  [range(0,len(xa)),i] = [smoothedX]
#        for l in range(0,len(smoothedX)):
#            avgX[l,i] = smoothedX[l]
#            avgY[l,i] = smoothedY[l]
#            avgZ[l,i] = smoothedZ[l]
#    #end for loop
#
#    tStep = np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])
#
#    timeV = np.arange(0, np.max(np.max(tsMtrx,axis=0)), tStep)
#    if len(timeV) > len(avgX[:,0]):
#        timeV = np.resize(timeV, (len(avgX[:,0]),1))
    #######


    #######


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
