#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/5276967/python-in-xcode-4

"""tv_write_xyzt2matlab.py: TremVibe Write Accelerometer XYZ and Timestamp to .m file"""
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
    print "Usage: ql2matlabcsvdat.py hostname email-address" #`"sql query`""
    print "     : hostname = cloud server hostname running the mysql service"
    exit(0)
else:
    email = sys.argv[1]

server = 'localhost'

try:
    conn = MySQLdb.Connection(server, 'triaxim', 'tria00xB', 'neurobit')
    cursr = conn.cursor()
    query = """SELECT accelX, accelY, accelZ, accelTs from TremCamTbl WHERE email =%s"""
    cursr.execute(query,email)
    conn.commit()
    row_count = cursr.rowcount
    results     = cursr.fetchall()
    #print type(results)
    #print len(results)
    f = open('/tmp/tv_user_accelxyzt.m', 'w')
    #for t in results:
        #line = ' '.join(str(x) for x in t)
    #    line = " ".join(map(str, results))
    #    f.write(line + '\n')
    f.write('%%  Matlab .m formated file \n')
    f.write('%%  Accelerometer data for user:%s \n' % (email))
    f.write('%%  Example how to plot X values of record 6:\n')
    f.write('%%  plot ((rec6matrix(4,:) - rec6matrix(4,1))/1e+6,rec6matrix(1,:))\n')
    rec_no = 0
    for record in results:
        #f.write('%s %s %s %s\n' % tuple)
        #print len(record)
        rec_no +=1
        f.write('%% record #:%d\n' % rec_no)
        #f.write('%% Xvalues\bYvalues\bZvalues\bTimestamp\n')
        if len(record) >= 4:
            f.write('xVal%d = [%s];\n' % (rec_no,record[0]))
            f.write('yVal%d = [%s];\n' % (rec_no,record[1]))
            f.write('zVal%d = [%s];\n' % (rec_no,record[2]))
            f.write('tVal%d = [%s];\n' % (rec_no,record[3]))
            f.write('rec%dmatrix = [xVal%d;yVal%d;zVal%d;tVal%d];\n'%(rec_no,rec_no,rec_no,rec_no,rec_no))
        
    f.close()
#    emailDict =  parse_email_records(row_count, results)
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
