#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
import sys
import MySQLdb 

#server='129.74.155.16'
server='192.168.1.112'
conn = None

try:

    #conn = MySQLdb.Connection('snoopy.cse.nd.edu', 'root', 'ixaedu1', 'neurosenz')
	conn = MySQLdb.Connection(server, 'tremcam', 'trem00xB', 'neurobit')
	cursr = conn.cursor()
	query = "SELECT fft_result from TremCamTbl WHERE email = 'saguinag@nd.edu'"
	cursr.execute(query)
	conn.commit()
	print cursr.rowcount
	results = cursr.fetchall()
	print results 
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if conn:
        conn.close()
