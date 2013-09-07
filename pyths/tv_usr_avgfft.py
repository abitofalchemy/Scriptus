#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/5276967/python-in-xcode-4

"""tv_usr_avgfft.py: TremVibe user's avg fft"""
__author__  = "Salvador Aguinaga"

import sys
import MySQLdb
import math
from itertools import groupby
import csv

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
#db = MySQLdb.connect('192.168.1.112', 'tremcam', 'trem00xB','neurobit')
#cursor = db.cursor()
#
#query = sys.argv[1]
#cursor.execute(query)
#result = cursor.fetchall()

##########----------##########----------##########----------##########----------
if (len(sys.argv) < 1):
    print "Usage: tv_usr_avgfft.py hostname email-address" #`"sql query`""
    print "     : hostname = cloud server hostname running the mysql service"
    exit(0)
else:
    email = sys.argv[1]

server = 'localhost'

try:
    conn = MySQLdb.Connection(server, 'triaxim', 'tria00xB', 'neurobit')
    cursr = conn.cursor()
    ## fetch the avgfftspectrum for given email, but only last record
    query = """SELECT avgfftspectrum FROM TremCamTbl WHERE email =%s order by subjectid desc limit 1"""
    
    cursr.execute(query,email)
    conn.commit()
    
    row_count = cursr.rowcount
    results   = cursr.fetchall()
    #print type(results)
    print 'len(results): ' , len(results)
    print 'row count: ',row_count
    f = open('/tmp/tv_user_avgfft.m', 'w')
    f.write('freq,mag\n')
    m_ix = 0
    for record in results:
        if len(record) >0:
            avgfft_str = record[0]
            #print (avgfft_str)
            avgfft_lst = [x.strip() for x in avgfft_str.split(',')]
            #f.write('%s\n' % (record[0]))
        
    for mag in avgfft_lst:
        f.write('%d,%s\n' % (m_ix,mag))
        m_ix += 1
    f.close()
#    emailDict =  parse_d4
#    with open("/var/www/tremvibe/subject_accel_sensor_dat.csv", "wb") as f:
        #        csv.writer(f).writerow(['Subject', 'Records'])
#        for email in emailDict:
            #print email,',',len(emailDict[email])
#            csv.writer(f).writerow([email, len(emailDict[email])])
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if conn:
        conn.close()
