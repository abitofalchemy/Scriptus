#!/usr/bin/python
# -*- coding: utf-8 -*-
"""tc_timeplot.py: Computes the average FFT for a number of records
    trying to get, generates a plot in the images folder """
"""usage: tc_timeplot.py hostname email or id %""" 
__author__  = "Salvador Aguinaga"

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
from matplotlib.lines import Line2D

##
import datetime

# global sets
leg_prop = matplotlib.font_manager.FontProperties(size=8)
###################################

def plot_fft_to_figure():
    plt.draw()
    ## generate an image file
    F = plt.gcf()
    DPI = F.get_dpi()
    F.savefig('images/figplot.png',dpi = (300))

def insert_running_avg_fft_spec(avgfftspec, sampRate, mCursor, forRecordId):
#    print "rec id:",forRecordId," type:",forRecordId[0] # because forRecordId is of list type
    print 'sampRate:',sampRate
    dateandtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#    print dateandtime
#    statement = """UPDATE TremCamTbl SET avgfftspectrum= COALESCE(avgfftspectrum, %s), samplingHz= COALESCE(samplingHz,%s), datentime=%s WHERE subjectid=%s"""
    statement = """UPDATE TremCamTbl SET datentime=%s,samplingHz=%s,avgfftspectrum=IF(avgfftspectrum IS NULL,avgfftspectrum, %s) WHERE subjectid=%s"""
    try:
        mCursor.execute(statement,(dateandtime,sampRate,avgfftspec, forRecordId[0]))
    except Exception, e: print repr(e)

def insert(data, samplingHz, fundamentalHz, mCursor, forRecordId):
    #print "rec id:",forRecordId," type:",forRecordId[0] # because forRecordId is of list type
    statement = """UPDATE TremCamTbl SET fft_result=%s, samplingHz=%s, fundamentalHz=%s WHERE subjectid=%s"""
    print statement
    try:
        mCursor.execute(statement,(data, samplingHz, fundamentalHz, forRecordId[0]))
    except Exception, e: print repr(e)


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

def timeDomainVectorLength(timeArray):
    NFFT = 512
    #if ( numsamp > len(timeArray)):
    # zero pad x up to NFFT if it is shorter than NFFT
    if len(timeArray)< NFFT:
        return NFFT
    else:
        return len(timeArray)


def get_spectral_magnitude(y_data,time_data, fs):
    tStep = np.max(time_data)/len(time_data)
    timeV = np.arange(0, np.max(time_data), tStep)
    #print len(y_data),',', len(time_data),' ,max time value:',np.max(timeV)
    #print 'fs:',fs
    numsamp = 256 #timeDomainVectorLength(timeV)
    if (len(y_data) < numsamp):
        y_data = np.resize(y_data, (numsamp,))
    window  = hann(numsamp)
    ## setup the fft spectrum arrays
    mag_spectrum = np.zeros([numsamp,int(np.ceil(float(len(timeV))/numsamp))])
            #print 'time.len= %d, numsamp=%d, loop:%d' % (len(timeV), numsamp, int(np.ceil(float(len(timeV))/numsamp)))
    for k in range(0,int(np.ceil(float(len(timeV))/numsamp))):
        slice_dat    = y_data[k*numsamp:numsamp*(k+1)]
        
        if (len(slice_dat) < numsamp):
            if (len(slice_dat) < numsamp/2): # WE DISCARDS LAST SLICE POINTS IF < NUMSAMP/2
                break;
            slice_dat = np.resize(slice_dat,(numsamp,))
        #multiply it with the window and transform it into frequency domain
        spectrum_dat = fft(slice_dat*window);
        #get the spectrum mag @ each of the 256 frequency points and store it
        #print 'k:',k,' spectrum_dat.len:',len(spectrum_dat)
        mag_spectrum[:,k]= 20 * np.log10(abs(spectrum_dat))
    
    print "fs= %.4g, NFFT= %ld, y_data.shape= %d, mag_spectrum= %dx%d" % (fs, numsamp,np.shape(y_data)[0], np.shape(mag_spectrum)[0],np.shape(mag_spectrum)[1])
    ## DOUBLE CHECK  THE SIZE OF THE MATRIX
    avg_fft_foreach = np.mean(mag_spectrum, axis=1)
#    print "np.shape(avg_fft_foreach):", np.shape(avg_fft_foreach)
    return avg_fft_foreach
    


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

def index_min(values):
    return min(xrange(len(values)),key=values.__getitem__)
# 
def lastRecordIdForUser( email, mCursor ):
    statement = """SELECT email,subjectid,datentime FROM TremCamTbl WHERE email LIKE %s order by subjectid desc limit 1"""
    try: 
        mCursor.execute(statement,(email))
        results = mCursor.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if mCursor:
            mCursor.close()
    rec_id = {} #desc = cur.description ## http://alexharvey.eu/code/python/on-working-with-mysql-and-python/
    rec_id = [int(record[1]) for record in results]
    return rec_id

def main():
    # input data
    if (len(sys.argv) < 2):
        print "Usage: python tc_ft_avgg_vis_1.py hostname user_email" #`"sql query`""
        print "     Computes the vector for running average & plots the spectrum to a file" 
        print "     Uploads the average fft and average sampling rate\n"
        exit(0)
    else:
        host = sys.argv[1]
        user = sys.argv[2]
    
    mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')
    # GET ALL RECORDS - TO BE PROCESSED 
    # get mysql running average fft data for given user
    cur = mydb.cursor()
    statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE email LIKE %s"""
    try:
        #print user
        cur.execute(statement,(user))
        results = cur.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)    
    finally:
        if cur:
            cur.close()
    print "=========================================================\n"
    print "Number of records for(", user, "): ", cur.rowcount
    #print "results:",np.shape(results[0])
    
    xv = []
    yv = []
    zv = []
    tv = []

    for record in results:
        #print len(record)
        if len(record) >= 4:
            xv.append(record[0])    # X
            yv.append(record[1])    # Y
            zv.append(record[2])    # Z
            tv.append(record[3])    # timestamp
    
    ## setup plot
    fig = plt.figure()#num=None,figsize=(1.6*7,1*7))
    ax1 = fig.add_subplot(211)
    ax1.grid(True)
    ax1.set_frame_on(False)
    ax2 = fig.add_subplot(212)
    ax2.grid(True)
    ax2.set_frame_on(False)

    
    # setup 2D array
    N = int(len(xv))
    avgX = np.zeros([10,N])
    avgY = np.zeros([10,N])
    avgZ = np.zeros([10,N])
    tsMtrx = np.zeros([10,N])  # 
    acMtrx = np.zeros([10,N])  # accelerometer
    samprate_vec = []#np.ones((1,N))  #np.empty((1,N),dtype='float')
#    print 'samprate_vec', np.shape(samprate_vec)
    tmpA = np.zeros([10,N])
    # debug
    parts = tv[0].split(",")
    if parts == [] :
        print "invalid record"
        return
    # -----
    mag_spectrum_matrix = np.zeros([256,N]) # make 256 a global variable (or defined onece)
    fs_vector = np.empty(N);
    for i in range(0,N):
        ta  = [np.long(fv) for fv in tv[i].split(",")]
        xa  = [float(fv) for fv in xv[i].split(",")]
        ya  = [float(fv) for fv in yv[i].split(",")]
        za  = [float(fv) for fv in zv[i].split(",")]
        lN  = len(xa)
        if ( len(xa) > len(avgX[:,i]) ):
            avgX        = np.resize(avgX, (len(xa),N))
            avgY        = np.resize(avgY, (len(ya),N))
            avgZ        = np.resize(avgZ, (len(za),N))
            tsMtrx      = np.resize(tsMtrx, (len(ta),N))
        avgX[0:lN,i]   = [float(fv) for fv in xa]
        avgY[0:lN,i]   = [float(fv) for fv in ya]
        avgZ[0:lN,i]   = [float(fv) for fv in za]
        tsMtrx[range(0,len(ta)),i] = [np.long(fv-ta[0]) for fv in ta]


        #ax1.plot(tsMtrx[range(0,len(ta)),i], avgX[0:lN,i],label='X')
        ## denoisng record
#        smoothedX = smoothListGaussian(xa)

        ## AVERAGE XYZ - RAW
#       acMtrx[range(0,len(ta)),i] 
        #print np.mean((avgX[:,i],avgY[:,i],avgZ[:,i]),axis=0) # we avg x,y,z into acGroupred
        avgdAxis  = np.mean(([float(fv) for fv in xa],
                             [float(fv) for fv in ya],
                             [float(fv) for fv in za]), axis = 0)
        acGrouped = np.mean((avgX[:,i],avgY[:,i],avgZ[:,i]),axis=0) # we avg x,y,z into acGroupred
        timeVector = tsMtrx[range(0,len(ta)),i] = [np.long(fv-ta[0]) for fv in ta]

        if (len(avgdAxis) == len(timeVector) ):
            fs = len(timeVector)/(np.max(timeVector)*1e-3)
        else:
            print 'input arrays do no match'
            print 'y_data:%d, time_data:%d' % (len(y_data),len(timeVector))
            
        ## GET THE MAGNITUDE SPECTRUM
        mag_spectrum_vector = get_spectral_magnitude(avgdAxis,timeVector, fs )
        #mag_spectrum_matrix = np.resize(mag_spectrum_matrix,
        #                      (len(mag_spectrum_vector),N))
        mag_spectrum_matrix[:,i]  = mag_spectrum_vector
        print i,', ',np.shape(fs_vector)
        fs_vector[i] = fs

    print '-------------------------------------'
#    print 'shape of tsMtrx     ', np.shape(tsMtrx)
#    print 'shape of avgX       ', np.shape(avgX)
#    print 'shape of x mag spec ', np.shape(mag_spectrum_matrix)
    ##
    mean_spec_avg_vec = np.mean(mag_spectrum_matrix, axis=1)
    mean_spec_avg_vec -= max(mean_spec_avg_vec)
   
    ## Inset data to storage
    cur = mydb.cursor()
    recordId  = lastRecordIdForUser( user, cur )
    print 'recordId: ', recordId
    output_fft = ','.join(map(str, mean_spec_avg_vec))
    print np.mean(fs_vector,axis=0)
    cur = mydb.cursor()
    insert_running_avg_fft_spec(output_fft, np.mean(fs_vector,axis=0), cur, recordId)


    #    fs = np.mean(samprate_vec,axis=0)
#    print ta[0],'-',ta[len(ta)-1]
    n = len(mean_spec_avg_vec) # length of the signal
    k = np.arange(n)
    T = n/fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range
#    #    print len(frq)
#    #    print len(mean_spec_mtrx_x[0:numsamp/2])
#
#    print n,', freq:', len(frq)
    ax1.plot(np.mean(tsMtrx, axis=1), np.mean(avgX, axis=1), '.', label='X')
    ax1.plot(np.mean(tsMtrx, axis=1), np.mean(avgY, axis=1), '.', label='Y')
    ax1.plot(np.mean(tsMtrx, axis=1), np.mean(avgZ, axis=1), '.', label='Z')
    ax1.plot(timeVector, avgdAxis, 'k',linewidth=2)
    ax1.set_ylabel('Acceleration ($m/s^2$)')
    ax1.set_xlabel("Time (ms)")
    x1,x2,y1,y2 = ax1.axis()
    ax1.add_artist(Line2D((x1, x2), (y1, y1), color='black', linewidth=1))
    leg = ax1.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
    leg.get_frame().set_alpha(0.5)

    ax2.plot(frq, mean_spec_avg_vec[0:n/2], linewidth=2);
    ax2.set_ylabel('Magnitude Spectrum\n(Normalized to 0dB)')
    ax2.set_xlabel('Cycles per Second (Hz)')
    x1,x2,y1,y2 = ax2.axis()
    ax2.add_artist(Line2D((x1, x2), (y1, y1), color='black', linewidth=1))
    plot_fft_to_figure()


#    print "size of ta:", len(ta)
#    print "smoothedX:", len(smoothedX)
    #print len(tsMtrx[:,0]),",",np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])
#    tStep = np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])
#     
##    print "time step:",tStep," ns"
#
#    timeV = np.arange(0, np.max(np.max(tsMtrx,axis=0)), tStep)
#    if len(timeV) > len(avgX[:,0]):
#        timeV = np.resize(timeV, (len(avgX[:,0]),1))
#    print len(timeV),",", np.shape(avgX)
#    ax1.plot(ta, xa,label="X-axis")
#    ax1.plot(ta, ya,label="Y-axis")
#    ax1.plot(ta, za,label="Z-axis")
#    leg = ax1.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
#    leg.get_frame().set_alpha(0.5)
#
#    ax1.set_ylabel('Acceleration $m/s^2$')
#    ax1.set_xlabel("Time (s)")
#    plt.suptitle(user)
#   
#    print "len(tsMtrx[:,0]):        ",len(tsMtrx[:,0])
#    print "np.max(tsMtrx,axis=0):   ",np.max(tsMtrx,axis=0)*1e-3
#    #print "fs = ",len(tsMtrx[:,0])/(np.max(tsMtrx,axis=0)*1e-3)
#    fs = len(tsMtrx[:,0])/(np.max(tsMtrx,axis=0)*1e-3)
#    print "fs = ",fs
#    # do dsp
#    numsamp = timeDomainVectorLength(ta)
#    if len(ta)<numsamp:
#        n = len(ta)
#        ta = resize(ta, (numsamp,))
#        ta[n:] = 0
#        xa = resize(xa, (numsamp,))
#        xa[n:] = 0
#        ya = resize(ya, (numsamp,))
#        ya[n:] = 0
#        za = resize(za, (numsamp,))
#        za[n:] = 0
#
#    window  = hann(numsamp)
#    
#    ## setup the fft spectrum arrays
#    mag_spectrum_x = np.zeros([numsamp,len(ta)/numsamp])
#    mag_spectrum_y = np.zeros([numsamp,len(ta)/numsamp])
#    mag_spectrum_z = np.zeros([numsamp,len(ta)/numsamp])
#    #print "len(ta)/numsamp:", len(ta)/numsamp
#
#    for k in range(0,len(ta)/numsamp):
#        sliceX = xa[k*numsamp:numsamp*(k+1)]
#        sliceY = ya[k*numsamp:numsamp*(k+1)]
#        sliceZ = za[k*numsamp:numsamp*(k+1)]
#        #multiply it with the window and transform it into frequency domain
#        spectrumx = fft(sliceX*window);
#        spectrumy = fft(sliceY*window);
#        spectrumz = fft(sliceZ*window);
#        #get the spectrum mag @ each of the 256 frequency points and store it
#        mag_spectrum_x[:,k]= 20 * np.log10(abs(spectrumx))
#        mag_spectrum_y[:,k]= 20 * np.log10(abs(spectrumy))
#        mag_spectrum_z[:,k]= 20 * np.log10(abs(spectrumz))
#    
#    mean_spec_mtrx_x = np.mean(mag_spectrum_x, axis=1) 
#    mean_spec_mtrx_x -= max(mean_spec_mtrx_x)
#    mean_spec_mtrx_y = np.mean(mag_spectrum_y, axis=1)
#    mean_spec_mtrx_y -= max(mean_spec_mtrx_y)
#    mean_spec_mtrx_z = np.mean(mag_spectrum_z, axis=1)
#    mean_spec_mtrx_z -= max(mean_spec_mtrx_z)
#    #output_vec[0] = mean_spectrum[0];
#    #output_vec[1:126] = 1/2*(mean_spectrum[1:126]+mean_spectrum[254:-1:128]);
#    #output_vec[127] = mean_spectrum[127];
#    n = numsamp # length of the signal
#    k = np.arange(n)
#    T = n/fs
#    frq = k/T # two sides frequency range
#    frq = frq[range(n/2)] # one side frequency range
#    #    print len(frq)
#    #    print len(mean_spec_mtrx_x[0:numsamp/2])
#            
#    ax2.plot(frq,mean_spec_mtrx_x[0:numsamp/2],label="X-axis");
#    ax2.plot(frq,mean_spec_mtrx_y[0:numsamp/2],label="Y-axis");
#    ax2.plot(frq,mean_spec_mtrx_z[0:numsamp/2],label="Z-axis");
#    
### Now the average of three magnitudes
#    avg3d_spec_mag = np.mean ([mean_spec_mtrx_x[0:numsamp/2],
#                            mean_spec_mtrx_y[0:numsamp/2],
#                            mean_spec_mtrx_z[0:numsamp/2]], axis=0);
#    print "avg3d_spec_mag:",len(avg3d_spec_mag)
##fx = avg3d_spec_mag.index(min(avg3d_spec_mag))
#    f0index = np.argmax(avg3d_spec_mag)
#    print "min:",max(avg3d_spec_mag)
#    f0 = frq[f0index]
#    print "fundamental frequency:(",f0index,") ",f0
#
#    ax2.plot(frq,avg3d_spec_mag,label="3D Average");
#
###  Write the avg3d_spec_mag to MySQL db
#    output_fft = ','.join(map(str, avg3d_spec_mag))
#    cur = mydb.cursor()
#    insert(output_fft , fs[0], f0, cur, rec_id)
#
#    ax2.set_ylabel("Magnitude (dB)")
##    x1,x2,y1,y2 = ax2.axis()
##    ax2.axis([x1,x2/2,y1,y2])
#    ax2.minorticks_on()
#    leg = ax2.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
#    leg.get_frame().set_alpha(0.5)
#



    
### http://www.csh.rit.edu/~jon/projects/pip/
## main
if __name__ == '__main__':
    main()


