#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/5276967/python-in-xcode-4

"""
filename: tv_get_date_f0.py
description: get date and f0 for a given user
"""
__author__  = "Salvador Aguinaga"

import sys
import MySQLdb
import math
from   itertools import groupby
import csv
#from matplotlib.dates import date2num
from datetime import datetime
from datetime import date
from time import time

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
def get_spectral_magnitude(y_data,time_data, fs):
	tStep = np.max(time_data)/len(time_data)
	timeV = np.arange(0, np.max(time_data), tStep)
	numsamp = 512 #timeDomainVectorLength(timeV)
	if (len(y_data) < numsamp):
		y_data = np.resize(y_data, (numsamp,))
	window  = hann(numsamp)
	## setup the fft spectrum arrays
	mag_spectrum = np.zeros([numsamp,int(np.ceil(float(len(timeV))/numsamp))])
	#print 'time.len= %d, numsamp=%d, loop:%d' % (len(timeV), numsamp, int(np.ceil(float(len(timeV))/numsamp)))
	for k in range(0,int(np.ceil(float(len(timeV))/numsamp))):
		slice_dat	= y_data[k*numsamp:numsamp*(k+1)]
		
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
	#	print "np.shape(avg_fft_foreach):", np.shape(avg_fft_foreach)
	return avg_fft_foreach

def tc_compute_store_fft( dbHandler, record_nbr ):
	#mydb = MySQLdb.connect(host,'tremcam','trem00xB','neurobit')
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
	
	avgX	= np.empty([10,N])
	avgY	= np.empty([10,N])
	avgZ	= np.empty([10,N])
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
			avgX		= np.resize(avgX, (len(xa),N))
			avgY		= np.resize(avgY, (len(ya),N))
			avgZ		= np.resize(avgZ, (len(za),N))
			tsMtrx	  = np.resize(tsMtrx, (len(ta),N))
		
		avgX[0:lN,i]   = [float(fv) for fv in xa]
		avgY[0:lN,i]   = [float(fv) for fv in ya]
		avgZ[0:lN,i]   = [float(fv) for fv in za]
		tsMtrx[range(0,len(ta)),i] = [np.long(fv-ta[0]) for fv in ta]
		timeVector = tsMtrx[range(0,len(ta)),i] = [np.long(fv-ta[0]) for fv in ta]
	
	meanVecX =np.mean(avgX,axis=1)
	meanVecY =np.mean(avgY,axis=1)
	meanVecZ =np.mean(avgZ,axis=1)
	
	## Average XYZ
	xyzAveraged = np.mean([meanVecX,meanVecY,meanVecZ],axis=0)
	#print "np.shape(xyzAveraged): ", np.shape(xyzAveraged)
	
	if (len(xyzAveraged) == len(timeVector) ):
		fs = len(timeVector)/(np.max(timeVector)*1e-3)
	else:
		print 'input arrays do no match'
		print 'y_data:%d, time_data:%d' % (len(y_data),len(timeVector))
	
	# fft
	#mags = get_spectral_magnitude(xyzAveraged, )#abs(fft(xyzAveraged[0:fftSamples]*window))
	mags = get_spectral_magnitude(xyzAveraged,timeVector, fs )
	# convert to dB
	#	mags = 20 * np.log10(mags)
	#	mags -= max(mags)
	NNFT = len(mags)
	k = np.arange(NNFT)
	T = NNFT/fs
	frq = k/T # two sides frequency range
	frq = frq[range(NNFT/2)] # one side frequency range
	## setup plot
#	fig = plt.figure()
#	ax1 = fig.add_subplot(111)
#	ax1.grid(True)
	#plt.suptitle(query)
#	ax1.plot(frq,mags[0:len(frq)],label='X-axis')
#	ax1.set_title('X axis: All',fontsize=8)
	#	plt.xlim(0, NNFT/2-1)
#	ax1.tick_params(axis='x', labelsize=8)
#	ax1.tick_params(axis='y', labelsize=8)
	
	##  plot_fft_to_figure()
	f0= frq[maxelements(mags[0:len(frq)])]
	return [fs,float(f0),mags] # return sampling rate, fundamental hz, fft magitude

def store_tc_record_parameters(data, samplingHz, fundamentalHz, mCursor, forRecordId):
	#print "rec id:",forRecordId," type:",forRecordId[0] # because forRecordId is of list type
	dateandtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	statement = """UPDATE TremCamTbl SET fft_result=%s, samplingHz=%s, fundamentalHz=%s,datentime=%s WHERE subjectid=%s"""
	print statement
	try:
		print samplingHz
		mCursor.execute(statement,(data, samplingHz, fundamentalHz, dateandtime, forRecordId[0]))
	except Exception, e: print repr(e)

##########----------##########----------##########----------##########----------
def main():
	# input data
	if (len(sys.argv) < 2):
		print "Usage: python tv_get_date_f0  user_email" #`"sql query`""
		exit(0)
	else:
		useremail = sys.argv[1]

	server = 'localhost'
	conn   = None
	mydb = MySQLdb.Connection(server, 'triaxim', 'tria00xB', 'neurobit')
	cursr = mydb.cursor()
        print useremail
	try:
		#query = "SELECT datentime,samplingHz,fundamentalHz from TremCamTbl WHERE email=%s"
		query = "SELECT datentime,samplingHz,fundamentalHz from TremCamTbl WHERE email=%s ORDER BY datentime ASC"
		cursr.execute(query,(useremail))
		#cursr.execute(query)
		mydb.commit()
		print 'row count:', cursr.rowcount
		row_count = cursr.rowcount
		results	 = cursr.fetchall()

	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)

	finally:
		
		if cursr:
			cursr.close()
	
	date_n_time = {}
	samprate    = {}
	fundamental = {}
	
	date_n_time= [record[0]   for record in results]
	samprate   = [float(record[1]) for record in results]
	fundamental= [float(record[2]) for record in results]
        print samprate 
        print date_n_time
        print fundamental
	with open("/tmp/f0freqs.tsv","wb") as f:
		csv.writer(f,delimiter='\t').writerow(['date','frequency'])
		for i in range(len(fundamental)):
			if (date_n_time[i]): 
				dateString = date_n_time[i].date().strftime('%d-%b-%y')
				#print '%s\t%.2f'%(dateString,samprate[i])
				csv.writer(f,delimiter='\t').writerow([dateString,fundamental[i]])
        
        with open("/tmp/samprate.tsv","wb") as f:
                csv.writer(f,delimiter='\t').writerow(['date','samprate'])
                for i in range(len(fundamental)):
                        if (date_n_time[i]):
                                dateString = date_n_time[i].date().strftime('%d-%b-%y')
                                #print '%s\t%.2f'%(dateString,samprate[i])
                                csv.writer(f,delimiter='\t').writerow([dateString,samprate[i]])

## main
if __name__ == '__main__':
	main()
