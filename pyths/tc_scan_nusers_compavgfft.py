#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/5276967/python-in-xcode-4

"""tc_scan_nusers_compavgfft.py: scan for new users and compute the avg fft"""
__author__  = "Salvador Aguinaga"

import sys
#from   pylab import *
#from   scipy.signal import np.hanning
import numpy as np
import MySQLdb
import math
from   itertools import groupby
import csv
import datetime

##########----------##########----------##########----------##########----------
def get_spectral_magnitude(y_data,time_data):
    #time_data[0],",",time_data[len(time_data)-1]
    tStep = np.max(time_data)/len(time_data)
    timeV = np.arange(0, np.max(time_data), tStep)
    #print "np.max(timeV):",np.max(timeV),", len(timeV): ",len(timeV)
    fs = float( len(timeV)/(np.max(timeV)*1e-3) )
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
    #    print "np.shape(avg_fft_foreach):", np.shape(avg_fft_foreach)
    return avg_fft_foreach, fs

##########----------##########----------##########----------##########----------
def parse_email_records(row_count, emails):
    #print np.shape(results)
    '''Puts the filenames in the given iterable into a dictionary where
        the key is the first component of the emails and the value is
        a list of the records for that email.'''
    keyfunc = lambda f: f.split('@', 1)[0]
    return dict( (k, list(g)) for k,g in groupby(
                                                 sorted((i[0] for i in emails), key=keyfunc), key=keyfunc
                                                 ) )

##########----------##########----------##########----------##########----------
def insert_running_avg_fft_spec(avgfftspec, mCursor, forRecordId):
    #print "rec id:",forRecordId," type:",forRecordId[0] #b/c RecordId is of list type
    statement = """UPDATE TremCamTbl SET avgfftspectrum=%s WHERE subjectid=%s"""
    try:
        mCursor.execute(statement,(avgfftspec, forRecordId[0]))
    except Exception, e: print repr(e)

##########----------##########----------##########----------##########----------
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

##########----------##########----------##########----------##########----------
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

##########----------##########----------##########----------##########----------
#def get_spectral_magnitude(y_data,time_data, fs):
#    tStep = np.max(time_data)/len(time_data)
#    timeV = np.arange(0, np.max(time_data), tStep)
#    numsamp = 512 #timeDomainVectorLength(timeV)
#    if (len(y_data) < numsamp):
#        y_data = np.resize(y_data, (numsamp,))
#    window  = np.hanning(numsamp)
#    ## setup the fft spectrum arrays
#    mag_spectrum = np.zeros([numsamp,int(np.ceil(float(len(timeV))/numsamp))])
#    #print 'time.len= %d, numsamp=%d, loop:%d' % (len(timeV), numsamp, int(np.ceil(float(len(timeV))/numsamp)))
#    for k in range(0,int(np.ceil(float(len(timeV))/numsamp))):
#        slice_dat    = y_data[k*numsamp:numsamp*(k+1)]
#        
#        if (len(slice_dat) < numsamp):
#            if (len(slice_dat) < numsamp/2): # WE DISCARDS LAST SLICE POINTS IF < NUMSAMP/2
#                break;
#            slice_dat = np.resize(slice_dat,(numsamp,))
#        #multiply it with the window and transform it into frequency domain
#        spectrum_dat = np.fft.fft(slice_dat*window);
#        #get the spectrum mag @ each of the 256 frequency points and store it
#        #print 'k:',k,' spectrum_dat.len:',len(spectrum_dat)
#        mag_spectrum[:,k]= 20 * np.log10(abs(spectrum_dat))
#        mag_spectrum[:,k]= abs(spectrum_dat)
#    #print "fs= %.4g, NFFT= %ld, y_data.shape= %d, mag_spectrum= %dx%d" % (fs, numsamp,np.shape(y_data)[0], np.shape(mag_spectrum)[0],np.shape(mag_spectrum)[1])
#    ## DOUBLE CHECK  THE SIZE OF THE MATRIX
#    avg_fft_foreach = np.mean(mag_spectrum, axis=1)
#    #    print "np.shape(avg_fft_foreach):", np.shape(avg_fft_foreach)
#    return avg_fft_foreach

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
    ## 
    return smoothed

##########----------##########----------##########----------##########----------
def store_tc_record_parameters(data, samplingHz, fundamentalHz, mCursor, forRecordId):
    #print "rec id:",forRecordId," type:",forRecordId[0] # because forRecordId is of list type
    dateandtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    statement = """UPDATE TremCamTbl SET fft_result=%s, samplingHz=%s, fundamentalHz=%s, datentime=%s WHERE subjectid=%s"""
    print statement
    try:
        print samplingHz
        mCursor.execute(statement,(data, samplingHz, fundamentalHz,dateandtime, forRecordId[0]))
    except Exception, e: print repr(e)

##########----------##########----------##########----------##########----------
def main():
    #server = '192.168.1.112'
    server = 'localhost'
    conn   = None
    mydb = MySQLdb.Connection(server, 'triaxim', 'tria00xB', 'neurobit')
    cursr = mydb.cursor()
    try:
        query = "SELECT email,subjectid,avgfftspectrum from TremCamTbl order by subjectid desc limit 1"
        cursr.execute(query)
        mydb.commit()
        #print 'row count:', cursr.rowcount
        row_count = cursr.rowcount
        results     = cursr.fetchall()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        
        if cursr:
            cursr.close()

    rec_id = {} #desc = cur.description ## http://alexharvey.eu/code/python/on-working-with-mysql-and-python/
    user_email  = {}
    avgfft      = []
    avgfft      = [record[2] for record in results]
    #print 'avgfft:', avgfft
    if avgfft[0] != '':
        print 'do nothing'
        sys.exit()
    # else we compute the avg fft for all records matching user_email
    user_email = [record[0] for record in results]
    print user_email[0]
    rec_id = [int(record[1]) for record in results]
    
    #mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')
    # GET ALL RECORDS - TO BE PROCESSED
    # get mysql running average fft data for given user
    cur = mydb.cursor()
    statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE email LIKE %s"""
    try:
        #print user
        cur.execute(statement,(user_email[0]))
        results = cur.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if cur:
            cur.close()
    print "=========================================================\n"
    print "Number of records for(", user_email[0], "): ", cur.rowcount
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
    avgX = np.zeros([10,N])
    avgY = np.zeros([10,N])
    avgZ = np.zeros([10,N])
    tsMtrx = np.zeros([10,N])
    tmpA = np.zeros([10,N])
    # debug
    #print "N = no of records:",N
    parts = tv[0].split(",")
    if parts == [] :
        print "invalid record"
        return
    # -----
    mag_spectrum_matrix = np.zeros([1,N])
    fs_vector = np.zeros([1,N])

    for i in range(0,N):
        if (len(tv[i]) != 0):
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
            
            smoothedX = smoothListGaussian(xa)
            timeVector = tsMtrx[range(0,len(ta)),i] = [np.long(fv-ta[0]) for fv in ta]
            #print "record: ", i
        
            ## GET THE MAGNITUDE SPECTRUM
            mag_spectrum_vector,fsForRec = get_spectral_magnitude(smoothedX,timeVector)
            mag_spectrum_matrix = np.resize(mag_spectrum_matrix, (len(mag_spectrum_vector),N))
            mag_spectrum_matrix[:,i]  = mag_spectrum_vector
            fs_vector = fsForRec
            for l in range(0,len(smoothedX)):
                avgX[l,i] = smoothedX[l]
    #            avgY[l,i] = smoothedY[l]
    #            avgZ[l,i] = smoothedZ[l]
    #end for loop
    # end of for loop------------------------------------------------
    ##
    mean_spec_avg_vec = np.mean(mag_spectrum_matrix, axis=1)
    mean_spec_avg_vec -= max(mean_spec_avg_vec)


    cur = mydb.cursor()
    print 'Record ID updated: ', rec_id[0]
    output_fft = ','.join(map(str, mean_spec_avg_vec))
#print np.mean(fs_vector,axis=0)
    cur = mydb.cursor()
    insert_running_avg_fft_spec(output_fft, cur, rec_id)
    
## main
if __name__ == '__main__':
    main()
