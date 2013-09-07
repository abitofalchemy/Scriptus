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

def index_min(values):
    return min(xrange(len(values)),key=values.__getitem__)

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
    # GET LAST RECORD
    sttmnt = """SELECT email,subjectid,datentime FROM TremCamTbl WHERE email LIKE %s order by subjectid desc limit 1"""
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
            
    
    # get mysql running average fft data for given user
    cur = mydb.cursor()
    statement = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE subjectid LIKE %s"""
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
    print "=========================================================\n"
    print "Number of records for(", user, "): ", cur.rowcount, ", record id: ", rec_id
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
    avgX = np.zeros([10,N])
    avgY = np.zeros([10,N])
    avgZ = np.zeros([10,N])
    tsMtrx = np.zeros([10,N])
    tmpA = np.zeros([10,N])
    # debug
    print "N = no of records:",N
    parts = tv[0].split(",")
    if parts == [] :
        print "invalid record"
        return
    # -----
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
        
        smoothedX = smoothListGaussian(xa)        
        smoothedY = smoothListGaussian(ya)        
        smoothedZ = smoothListGaussian(za)        
        tsMtrx[range(0,len(ta)),i] = [np.long(fv-ta[0]) for fv in ta]
        print "duration: ",tsMtrx[len(ta)-1,i]
        #avgX  [range(0,len(xa)),i] = [smoothedX]
        for l in range(0,len(smoothedX)):
            avgX[l,i] = smoothedX[l]
            avgY[l,i] = smoothedY[l]
            avgZ[l,i] = smoothedZ[l]
        #end for loop
    print "size of ta:", len(ta)
    print "smoothedX:", len(smoothedX)
    #print len(tsMtrx[:,0]),",",np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])
    tStep = np.max(np.max(tsMtrx,axis=0))/len(tsMtrx[:,0])
     
    print "time step:",tStep," ns"

    timeV = np.arange(0, np.max(np.max(tsMtrx,axis=0)), tStep)
    if len(timeV) > len(avgX[:,0]):
        timeV = np.resize(timeV, (len(avgX[:,0]),1))
    print len(timeV),",", np.shape(avgX)
    ax1.plot(ta, xa,label="X-axis")
    ax1.plot(ta, ya,label="Y-axis")
    ax1.plot(ta, za,label="Z-axis")
    leg = ax1.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
    leg.get_frame().set_alpha(0.5)

    ax1.set_ylabel('Acceleration $m/s^2$')
    ax1.set_xlabel("Time (s)")
    plt.suptitle(user)
   
    print "len(tsMtrx[:,0]):        ",len(tsMtrx[:,0])
    print "np.max(tsMtrx,axis=0):   ",np.max(tsMtrx,axis=0)*1e-3
    #print "fs = ",len(tsMtrx[:,0])/(np.max(tsMtrx,axis=0)*1e-3)
    fs = len(tsMtrx[:,0])/(np.max(tsMtrx,axis=0)*1e-3)
    print "fs = ",fs
    # do dsp
    numsamp = timeDomainVectorLength(ta)
    if len(ta)<numsamp:
        n = len(ta)
        ta = resize(ta, (numsamp,))
        ta[n:] = 0
        xa = resize(xa, (numsamp,))
        xa[n:] = 0
        ya = resize(ya, (numsamp,))
        ya[n:] = 0
        za = resize(za, (numsamp,))
        za[n:] = 0

    window  = hann(numsamp)
    
    ## setup the fft spectrum arrays
    mag_spectrum_x = np.zeros([numsamp,len(ta)/numsamp])
    mag_spectrum_y = np.zeros([numsamp,len(ta)/numsamp])
    mag_spectrum_z = np.zeros([numsamp,len(ta)/numsamp])
    #print "len(ta)/numsamp:", len(ta)/numsamp

    for k in range(0,len(ta)/numsamp):
        sliceX = xa[k*numsamp:numsamp*(k+1)]
        sliceY = ya[k*numsamp:numsamp*(k+1)]
        sliceZ = za[k*numsamp:numsamp*(k+1)]
        #multiply it with the window and transform it into frequency domain
        spectrumx = fft(sliceX*window);
        spectrumy = fft(sliceY*window);
        spectrumz = fft(sliceZ*window);
        #get the spectrum mag @ each of the 256 frequency points and store it
        mag_spectrum_x[:,k]= 20 * np.log10(abs(spectrumx))
        mag_spectrum_y[:,k]= 20 * np.log10(abs(spectrumy))
        mag_spectrum_z[:,k]= 20 * np.log10(abs(spectrumz))
    
    mean_spec_mtrx_x = np.mean(mag_spectrum_x, axis=1) 
    mean_spec_mtrx_x -= max(mean_spec_mtrx_x)
    mean_spec_mtrx_y = np.mean(mag_spectrum_y, axis=1)
    mean_spec_mtrx_y -= max(mean_spec_mtrx_y)
    mean_spec_mtrx_z = np.mean(mag_spectrum_z, axis=1)
    mean_spec_mtrx_z -= max(mean_spec_mtrx_z)
    #output_vec[0] = mean_spectrum[0];
    #output_vec[1:126] = 1/2*(mean_spectrum[1:126]+mean_spectrum[254:-1:128]);
    #output_vec[127] = mean_spectrum[127];
    n = numsamp # length of the signal
    k = np.arange(n)
    T = n/fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range
    #    print len(frq)
    #    print len(mean_spec_mtrx_x[0:numsamp/2])
            
    ax2.plot(frq,mean_spec_mtrx_x[0:numsamp/2],label="X-axis");
    ax2.plot(frq,mean_spec_mtrx_y[0:numsamp/2],label="Y-axis");
    ax2.plot(frq,mean_spec_mtrx_z[0:numsamp/2],label="Z-axis");
    
## Now the average of three magnitudes
    avg3d_spec_mag = np.mean ([mean_spec_mtrx_x[0:numsamp/2],
                            mean_spec_mtrx_y[0:numsamp/2],
                            mean_spec_mtrx_z[0:numsamp/2]], axis=0);
    print "avg3d_spec_mag:",len(avg3d_spec_mag)
#fx = avg3d_spec_mag.index(min(avg3d_spec_mag))
    f0index = np.argmax(avg3d_spec_mag)
    print "min:",max(avg3d_spec_mag)
    f0 = frq[f0index]
    print "fundamental frequency:(",f0index,") ",f0

    ax2.plot(frq,avg3d_spec_mag,label="3D Average");

##  Write the avg3d_spec_mag to MySQL db
    output_fft = ','.join(map(str, avg3d_spec_mag))
    cur = mydb.cursor()
    insert(output_fft , fs[0], f0, cur, rec_id)

    ax2.set_ylabel("Magnitude (dB)")
#    x1,x2,y1,y2 = ax2.axis()
#    ax2.axis([x1,x2/2,y1,y2])
    ax2.minorticks_on()
    leg = ax2.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
    leg.get_frame().set_alpha(0.5)

    plt.draw()
    ## generate an image file
    F = plt.gcf()
    DPI = F.get_dpi()
    F.savefig('images/figplot.png',dpi = (150))


    
### http://www.csh.rit.edu/~jon/projects/pip/
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
