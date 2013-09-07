#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import sys, string
from math import sin, pi
#from scipy.io.wavfile import read
#from scipy.signal import hann
#from scipy.fftpack import fft
#from scipy.fftpack import rfft
import matplotlib.pyplot as plt
import MySQLdb
#from Numeric import zeros, ones, diagonal, transpose, matrixmultiply, \
#    resize, sqrt, divide, array, Float, Complex, concatenate, \
#    convolve, dot, conjugate, absolute, arange, reshape

###################################
def detrend_none(x):
    return x

def window_hanning(x):
    return hanning(len(x))*x

def psd(x, NFFT=256, Fs=2, detrend=detrend_none,
        window=window_hanning, noverlap=0):
    """
        The power spectral density by Welches average periodogram method.
        The vector x is divided into NFFT length segments.  Each segment
        is detrended by function detrend and windowed by function window.
        noperlap gives the length of the overlap between segments.  The
        absolute(np.fft.fft(segment))**2 of each segment are averaged to compute Pxx,
        with a scaling to correct for power loss due to windowing.  Fs is
        the sampling frequency.
        
        -- NFFT must be a power of 2
        -- detrend and window are functions, unlike in matlab where they are
        vectors.
        -- if length x < NFFT, it will be zero padded to NFFT
        
        
        Refs:
        Bendat & Piersol -- Random Data: Analysis and Measurement
        Procedures, John Wiley & Sons (1986)
        
        """
    
    if NFFT % 2:
        raise ValueError, 'NFFT must be a power of 2'
    
    # zero pad x up to NFFT if it is shorter than NFFT
    if len(x)<NFFT:
        n = len(x)
        x = resize(x, (NFFT,))
        x[n:] = 0
    
    
    # for real x, ignore the negative frequencies
    if x.dtype == np.dtype('c'): numFreqs = NFFT
    else: numFreqs = NFFT//2+1
    
    windowVals = window(ones((NFFT,),x.typecode()))
    step = NFFT-noverlap
    ind = range(0,len(x)-NFFT+1,step)
    n = len(ind)
    Pxx = zeros((numFreqs,n), Float)
    
    # do the ffts of the slices
    for i in range(n):
        thisX = x[ind[i]:ind[i]+NFFT]
        thisX = windowVals*detrend(thisX)
        fx = absolute(np.fft.fft(thisX))**2
        Pxx[:,i] = fx[:numFreqs]
    
    # Scale the spectrum by the norm of the window to compensate for
    # windowing loss; see Bendat & Piersol Sec 11.5.2
    if n>1: Pxx = mean(Pxx,1)
    Pxx = divide(Pxx, norm(windowVals)**2)
    freqs = Fs/NFFT*arange(0,numFreqs)
    return Pxx, freqs


def insert_timedomain(mEmail,data,mField,mCursor):
    print mField[:]
    statement = """UPDATE TremCamTbl SET `%s`=%%s WHERE `email`=%%s""" % mField[:]

    try:
        mCursor.execute(statement,(data,mEmail))
    except Exception, e: print repr(e)
    
def insert(email, data, cur):
    statement = """UPDATE TremCamTbl SET fft_result=%s WHERE email=%s""" #% (1000,`email`)
    print statement
    try:
        cur.execute(statement,(data,email))
    except Exception, e: print repr(e)

def checkRecordForUser(email, mCursor):
    statement = """SELECT email FROM TremCamTbl WHERE email=%s"""
    try:
        mCursor.execute(statement,(email))
        results = mCursor.fetchall()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        print "Checking if record exists"
    if ( mCursor.rowcount == 0 ):
        statement = """INSERT INTO TremCamTbl (email) VALUES (%s)"""
        try:
            mCursor.execute(statement,(email))
        except Exception, e:
            print repr(e)
    else:
        print "Record exists"
    
    return

def main():
    # input data
    if (len(sys.argv) < 1):
        print "Usage: python plotmysql.py hostname user_email" #`"sql query`""
        exit(0)
    else:
        host = sys.argv[1]
        user = sys.argv[2]
    
    mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')
    cur = mydb.cursor()
    # create record if found
    checkRecordForUser(user, cur)
            
    # generate sinusoidal data
    freq = 1000
    nsmp = 1024
    factor = 2 * pi * freq/8000
    sin_seg = []
    for seg in range(nsmp):
        # sine wave calculations
        sin_seg.append(sin(seg * factor))
        
    #print np.shape(sin_seg)
    t = np.arange(nsmp)
    #print "t:",len(t)

    y=sin_seg #np.sin(t/3)+np.cos(t/5)
    window = np.hanning(512)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.set_title('Time domain')
    #ax1.plot(t,sin_seg)
    ax2 = fig.add_subplot(212)
    ax2.grid(True)
    # fft
    k = np.arange(nsmp)
    Tperiod = nsmp/8000.
    frq = k/Tperiod # two sides frequency range
    frq = frq[range(nsmp/2)] # one side frequency range
    mags = abs(np.fft.fft(y[0:512]*window))
    # convert to dB
    mags = 20 * np.log10(mags)
    mags -= max(mags)
    #ax2.plot(frq,mags)
    #ax2.set_title('Magnitude (normalized to 0dB)')
    
    
    ### newway
    NFFT = 512; N = NFFT; n = np.arange(N); Fs = 50.
    window = np.hanning(NFFT) #Magnitude (normalized to 0dB)
    x = []
    for i in n:
        x.append(0.4*sin(2*pi*5/Fs*i) + 0.6*sin(2*pi*10/Fs*i))
    freqs = Fs/NFFT*np.arange(0,NFFT)
    y = abs(np.fft.fft(x*window))
    y = 20 * np.log10(y)
    y -= max(y) 
    print "freqs:",np.shape(freqs)
    print "x:",    np.shape(x)
    print "n:",    np.shape(n)
#    y,freqs = psd(x, NFFT=NFFT, Fs=Fs, detrend=detrend_none,
#              window=window_hanning, noverlap=0)  # PSD by Welch's Method
    numFreqs = NFFT/2           ## for real x, ignore the negative frequencies
    #print "numFreqs:", numFreqs

    ax1.plot(n/Fs,x)
    ax2.plot(freqs[0:numFreqs], y[0:numFreqs])
            
    sine_data  = ','.join(map(str, x))
    tv_data   =  ','.join(map(str, (n/Fs)*1e9+1e9)) # in nanosecods
    #plt.show()
    plt.draw()
    ## generate an image file
    F = plt.gcf()
    DPI = F.get_dpi()
    F.savefig('images/figplot.png',dpi = (150))
    
#    print type(td_data)
#   writing data to mysql
    #insert(user, freq_data, cur)
#   write(update) time domain data to x,y,z fields
    insert_timedomain(user,sine_data,'accelX',cur)
    insert_timedomain(user,sine_data,'accelY',cur)
    insert_timedomain(user,sine_data,'accelZ',cur)
    insert_timedomain(user,tv_data, 'accelTs',cur)

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
