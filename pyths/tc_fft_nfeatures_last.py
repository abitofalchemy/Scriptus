#!/usr/bin/python
# -*- coding: utf-8 -*-
# last update 2013/02/06
"""tc_fft_nfeatures_last.py: Computes the FFT and Features last record"""
__author__  = "Salvador Aguinaga"

import numpy as np
import sys, string
import math
#from scipy.signal import hanning
#from scipy.fftpack import fft
#from scipy.fftpack import rfft

import MySQLdb
#import matplotlib.pyplot as plt
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#import matplotlib.font_manager
## global sets
#leg_prop = matplotlib.font_manager.FontProperties(size=8)


##########----------##########----------##########----------##########----------
#def plot_fft_to_figure():
#    plt.draw()
#    ## generate an image file
#    F = plt.gcf()
#    DPI = F.get_dpi()
#    F.savefig('images/figplot.png',dpi = (300))

def maxelements(seq):
    ''' Return list of position(s) of largest element '''
    max_indices = []
    if seq.any():
        max_val = seq[0]
        for i,val in ((i,val) for i,val in enumerate(seq) if val >= max_val):
            if val == max_val:
                max_indices.append(i)
            else:
                max_val = val
                max_indices = [i]
    
    return max_indices

def insert(data, mCursor, forRecordId):
    #print "rec id:",forRecordId," type:",forRecordId[0] # because forRecordId is of list type
    statement = """UPDATE TremCamTbl SET fft_result=%s WHERE subjectid=%s"""
    print statement
    try:
        mCursor.execute(statement,(data,forRecordId[0]))
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
        if len(timeArray) % 2:
            raise ValueError, 'NFFT must be a power of 2'
            return NFF
        else:
            return len(timeArray)
    else:
        return NFFT


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

def get_spectral_magnitude(y_data,time_data, fs):
    tStep = np.max(time_data)/len(time_data)
    timeV = np.arange(0, np.max(time_data), tStep)
    numsamp = 512 #timeDomainVectorLength(timeV)
    if (len(y_data) < numsamp):
        y_data = np.resize(y_data, (numsamp,))
    window  = np.hanning(numsamp)
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
        spectrum_dat = np.fft.fft(slice_dat*window);
        #get the spectrum mag @ each of the 256 frequency points and store it
        #print 'k:',k,' spectrum_dat.len:',len(spectrum_dat)
        mag_spectrum[:,k]= 20 * np.log10(abs(spectrum_dat))
        mag_spectrum[:,k]= abs(spectrum_dat)
    #print "fs= %.4g, NFFT= %ld, y_data.shape= %d, mag_spectrum= %dx%d" % (fs, numsamp,np.shape(y_data)[0], np.shape(mag_spectrum)[0],np.shape(mag_spectrum)[1])
    ## DOUBLE CHECK  THE SIZE OF THE MATRIX
    avg_fft_foreach = np.mean(mag_spectrum, axis=1)
    #    print "np.shape(avg_fft_foreach):", np.shape(avg_fft_foreach)
    return avg_fft_foreach

def tc_compute_store_fft( dbHandler, record_nbr ):
    print record_nbr
    cur = dbHandler.cursor()
    
    # get mysql running average fft data for given user
    #statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE email =%s"""
    statement = """SELECT email, accelX, accelY, accelZ, accelTs from TremCamTbl WHERE subjectid=%s"""
    try:
        cur.execute(statement,(record_nbr))
        results = cur.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if cur:
            cur.close()
    user = [record[0] for record in results]
#print "number of records for(", user, "): ", cur.rowcount
    N = int(cur.rowcount)
    xv = []
    yv = []
    zv = []
    tv = []
    for record in results:
        #print len(record)
        if len(record) >= 4:
            xv.append(record[1])
            yv.append(record[2])
            zv.append(record[3])
            tv.append(record[4])

    avgX    = np.empty([10,N])
    avgY    = np.empty([10,N])
    avgZ    = np.empty([10,N])
    tsMtrx  = np.zeros([10,N])  #
    #print "shape:", np.shape(avgX)
#print "N:", N
    for i in range(0,N):
        ta  = [np.double(fv) for fv in tv[i].split(",")]
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
        tsMtrx[range(0,len(ta)),i] = [np.float(fv-ta[0]) for fv in ta]        
        timeVector = tsMtrx[range(0,len(ta)),i] = [np.float(fv-ta[0]) for fv in ta]

    meanVecX =np.mean(avgX,axis=1)
    meanVecY =np.mean(avgY,axis=1)
    meanVecZ =np.mean(avgZ,axis=1)
    
    ## Average XYZ
    xyzAveraged = np.mean([meanVecX,meanVecY,meanVecZ],axis=0)
   
    
    if (len(xyzAveraged) == len(timeVector) ):
        fs = len(timeVector)/(np.max(timeVector))/1e-3
        print 'fs: ',fs
    else:
        print 'input arrays do no match'
        print 'y_data:%d, time_data:%d' % (len(y_data),len(timeVector))

    # fft
    #mags = get_spectral_magnitude(xyzAveraged, )#abs(fft(xyzAveraged[0:fftSamples]*window))
    mags = get_spectral_magnitude(xyzAveraged,timeVector, fs )
    # convert to dB
#    mags = 20 * np.log10(mags)
#    mags -= max(mags)
    NNFT = len(mags)
    k = np.arange(NNFT)
    T = NNFT/fs
    frq = k/T # two sides frequency range
    frq = frq[range(NNFT/2)] # one side frequency range
    ## setup plot
    #fig = plt.figure()
    #ax1 = fig.add_subplot(111)
    #ax1.grid(True)
    #plt.suptitle(query)
    #ax1.plot(frq,mags[0:len(frq)],label='X-axis')
    #ax1.set_title('X axis: All',fontsize=8)
#    plt.xlim(0, NNFT/2-1)
    #ax1.tick_params(axis='x', labelsize=8)
    #ax1.tick_params(axis='y', labelsize=8)

    #plot_fft_to_figure()
    f0= frq[maxelements(mags[0:len(frq)])]
    return [fs,float(f0),mags] # return sampling rate, fundamental hz, fft magitude

def store_tc_record_parameters(data, samplingHz, fundamentalHz, mCursor, forRecordId):
    #print "rec id:",forRecordId," type:",forRecordId[0] # because forRecordId is of list type
    statement = """UPDATE TremCamTbl SET fft_result=%s, samplingHz=%s, fundamentalHz=%s WHERE subjectid=%s"""
    print statement
    try:
        print samplingHz
        mCursor.execute(statement,(data, samplingHz, fundamentalHz, forRecordId[0]))
    except Exception, e: print repr(e)

##########----------##########----------##########----------##########----------
def main():
    # input data
    if (len(sys.argv) < 2):
        print "Usage: python tc_fft_nfeatures_last.y hostname" 
        print "     : or ./tc_fft_nfeatures_last.py hostname"
        print "     : "
        exit(0)
    else:
        host = sys.argv[1]
        #user = sys.argv[2]
    
    mydb = MySQLdb.connect(host,'triaxim','tria00xB','neurobit')
    cur = mydb.cursor()
    
    # GET LAST RECORD
    sttmnt = """SELECT email,subjectid,avgfftspectrum from TremCamTbl order by subjectid desc limit 1"""
    try:
        cur.execute(sttmnt)
        results = cur.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)    
    finally:
        if cur:
            cur.close()
        #print "For user:",user,"the latest record is:", results

    rec_id = {} #desc = cur.description ## http://alexharvey.eu/code/python/on-working-with-mysql-and-python/
    rec_id = [int(record[1]) for record in results]
    subject = [record[0] for record in results]
    
    ## Computes the FFT (dB Magnitude) for the record
    [samp_rate,f0_freq,fft_magnitude] = tc_compute_store_fft(mydb,rec_id[0])
    print "%s's latest record: %d has its fundamental frequency @: %0.2f Hz" % \
          (subject,rec_id[0],f0_freq)
    print samp_rate
    cur = mydb.cursor()
    store_tc_record_parameters(fft_magnitude,samp_rate, f0_freq, cur, rec_id)
    

## main
if __name__ == '__main__':
    main()


