#!/usr/bin/python
# -*- coding: utf-8 -*-
"""f0avgfft.py: Computes the average FFT for a number of records"""
__author__  = "Salvador Aguinaga"

import numpy as np
import sys, string
import csv, itertools
import math
from decimal import *
#from scipy.io.wavfile import read
#from scipy.signal import hann
#from scipy.fftpack import fft
#from scipy.fftpack import rfft
import MySQLdb
###################################


def insert_running_avg_fft_spec(avgfftspec, sampRate, mCursor, forRecordId):
    print "rec id:",forRecordId," type:",forRecordId[0] # because forRecordId is of list type
    statement = """UPDATE TremCamTbl SET avgfftspectrum=%s, samplingHz=%s WHERE subjectid=%s"""
    print forRecordId[0] 
    try:
        mCursor.execute(statement,(avgfftspec, sampRate, forRecordId[0]))
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


def get_spectral_magnitude(y_data,time_data):

    
    tStep = np.max(time_data)/len(time_data)
    timeV = np.arange(0, np.max(time_data), tStep)
    #print "np.max(timeV):",np.max(timeV),", len(timeV): ",len(timeV)
    fs = float( len(timeV)/(np.max(timeV)*1e-9) )
    numsamp = 256 #timeDomainVectorLength(timeV)
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
    
    print "fs= %.4g, NFFT= %ld, y_data.shape= %d, mag_spectrum= %dx%d" % (fs, numsamp,np.shape(y_data)[0], np.shape(mag_spectrum)[0],np.shape(mag_spectrum)[1])
    ## DOUBLE CHECK  THE SIZE OF THE MATRIX
    avg_fft_foreach = np.mean(mag_spectrum, axis=1)

    return avg_fft_foreach, fs
    


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
    if (len(sys.argv) < 1):
        print "Usage: python tremcam_vis_basic.py hostname user_email" #`"sql query`""
        print "     : or ./tremcam_vis_basic.py hostname user_email"
        exit(0)
    else:
        host = 'localhost'     #sys.argv[1]
        user = sys.argv[1]
    
    mydb = MySQLdb.connect(host,'triaxim','tria00xB','neurobit')
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
            xv.append(record[0])
            yv.append(record[1])
            zv.append(record[2])
            tv.append(record[3])

    # setup 2D array
    N = int(len(xv))
    print 'number of records',N
    print ' len(xv): ', len(yv)


    avgX = np.zeros([10,N])
    avgY = np.zeros([10,N])
    avgZ = np.zeros([10,N])
    tsMtrx = np.zeros([10,N])
    tmpA = np.zeros([10,N])
    # debug
    parts = tv[0].split(",")
    if parts == [] :
        print "invalid record"
        return
#    # -----
    mag_spectrum_matrix = np.zeros([1,N])
    pwr_spectrum_matrix = np.zeros([1,N])
    fs_vector = np.zeros([1,N]) 
    frq  =  [] #np.zeros([1,N)

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
#
        smoothedX = smoothListGaussian(xa)
        smoothedXYZ = np.mean([smoothListGaussian(xa), smoothListGaussian(xa), smoothListGaussian(xa)],axis=0)
        timeVector = tsMtrx[range(0,len(ta)),i] = [np.long(fv-ta[0])/1e-6 for fv in ta]

        ## GET THE MAGNITUDE SPECTRUM
        mag_spectrum_vector,fsForRec = get_spectral_magnitude(smoothedXYZ,timeVector)
        mag_spectrum_matrix = np.resize(mag_spectrum_matrix,(2*N,len(mag_spectrum_vector)))
        Nk = len(mag_spectrum_vector) 
        mag_spectrum_vector[1:Nk] = [2*v for v in mag_spectrum_vector[1:Nk]]
        pwr_spectrum_vector = [v*v for v in mag_spectrum_vector] # compute power spectrum

        ## GET FREQ VECTOR FOR EACH RECORDING AND STORE BY COL
        n = len(mag_spectrum_matrix[i,:])  # length of the signal
        k = np.arange(n)
        T = n/fsForRec
        frq = k/T # two sides frequency range
        frq = frq[range(n/2)] # one side frequency range
        pwr_spectrum_matrix = np.resize(pwr_spectrum_matrix,(2*N,len(pwr_spectrum_vector)/2))
        
        #print "np.shape(pwr_spectrum_matrix): ",np.shape(pwr_spectrum_matrix)
        #print "np.shape(pwr_spectrum_vector): ",np.shape(pwr_spectrum_vector)
        pwr_spectrum_matrix[2*i,:] = frq
        pwr_spectrum_matrix[2*i+1,:] = pwr_spectrum_vector[0:n/2]
        print np.shape(pwr_spectrum_matrix)
        #csv.writer(f).writerow(frq)
        #csv.writer(f).writerow(mag_spectrum_vector)
        

#        mag_spectrum_packet = np.resize(mag_spectrum_matrix,(len(mag_spectrum_vector)+1,N))
#        mag_spectrum_packet[0,i] = 1.1 
#        mag_spectrum_packet[1:,i] = mag_spectrum_vector
#        fs_vector = fsForRec
#        for l in range(0,len(smoothedX)):
#            avgX[l,i] = smoothedX[l]
##            avgY[l,i] = smoothedY[l]
##            avgZ[l,i] = smoothedZ[l]
#        #end for loop
    # end of for loop------------------------------------------------
#    print '-------------------------------------'
#    print 'smoothedX ', np.shape(np.mean([smoothListGaussian(xa), smoothListGaussian(xa), smoothListGaussian(xa)],axis=0))
#d   print 'shape of tsMtrx     ', np.shape(tsMtrx)
#   print 'shape of avgX       ', np.shape(avgX)
    #print 'shape of x mag spec ', np.shape(mag_spectrum_matrix)
    #print 'shape of x mag spec ', np.shape(mag_spectrum_matrix)[0]
    #f.close()
    with open("/tmp/averagefft.csv", "wb") as csvfile:
        #csv.writer(csvfile).writerow(['samp', 'frequency_spectrum'])
        #spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        #...     for row in spamreader:
        #   ...         print ', '.join(row)
        for i in range(N):
            if (i==N-1):
                csvfile.write('freq,Rec%d'%i)
            else:
                csvfile.write('freq,Rec%d,'%i)
        csvfile.write('\n')

        list_array = map(list,zip(*pwr_spectrum_matrix))
        #floatarray = np.array(filter(None,list_array),dtype='|S10').astype(np.float128)
        csv.writer(csvfile).writerows(pwr_spectrum_matrix.T)
        #csv.writer(csvfile).writerows(map(list,zip(*mag_spectrum_matrix)))
        #csv.writer(csvfile).writerows(mag_spectrum_matrix)
            #f.write('\n' % (rec_no,record[0]))
    csvfile.close()


## main
if __name__ == '__main__':
    main()
