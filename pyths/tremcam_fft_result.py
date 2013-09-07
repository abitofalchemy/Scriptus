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
# global sets
leg_prop = matplotlib.font_manager.FontProperties(size=8)
###################################

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

def main():
    # input data
    if (len(sys.argv) < 2):
        print "Usage: python tremcam_fft_result.py hostname user_email" #
        print "     : or ./tremcam_fft_result.py hostname email"
        print "     : This shows the latest record's fft "
        exit(0)
    else:
        host = sys.argv[1]
        user = sys.argv[2]
    
    mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')
    cur = mydb.cursor()
    # GET LAST RECORD
    sttmnt = """SELECT email,subjectid,max(datentime) FROM TremCamTbl WHERE email LIKE %s """
    try:
        cur.execute(sttmnt,(user))
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
    print "rec_id:",rec_id
    
    # get mysql running average fft data for given user
    cur = mydb.cursor()
    statement = """SELECT fft_result from TremCamTbl WHERE subjectid LIKE %s"""
    #statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl 
    #		   WHERE subjectid  LIKE %s"""
    try:
        #print user
        cur.execute(statement,(rec_id))
        results = cur.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)    
    finally:
        if cur:
            cur.close()
    spec_mag = []

    for record in results:
        #print len(record)
        if len(record) >= 1:
            spec_mag.append(record[0])
            
    ## setup plot
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.grid(True)

    N = int(len(spec_mag))
    avgX = np.zeros([10,N])
    avgY = np.zeros([10,N])
    avgZ = np.zeros([10,N])
    tsMtrx = np.zeros([10,N])
    tmpA = np.zeros([10,N])
    # debug
#    print "N = no of records:",N
    parts = spec_mag[0].split(",")
    if parts == [] :
        print "invalid record"
        return
    # -----
    for i in range(0,N):
        spma  = [float(fv)/1e9 for fv in spec_mag[i].split(",")]
        lN  = len(spma)
        #end for loop
#    print "size of spma:", len(spma)
    ax1.plot(spma)

    ## NEED TO HAVE ACCESS TO SAMPLING FREQUENCY VALUE TO BE ABLE TO RECONSTRUCT THE FREQUENCIES VECTOR
    ## NOW MIGHT NEED TO CONSIDER USING A MATLAB STYLE FILE FORMAT FOR THE OUTPUT


    plt.suptitle(user)
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
