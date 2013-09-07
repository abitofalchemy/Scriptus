#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb 
import sys


conn = None

try:

	#conn = MySQLdb.Connection('spike.cse.nd.edu', 'root', 'ixaedu1', 'neurosenz')
	conn = MySQLdb.Connection('192.168.1.112', 'tremcam', 'trem00xB', 'neurobit')
	cursr = conn.cursor()
	query = "SELECT subjectid,email from TremCamTbl WHERE email='saguinag@nd.edu'"
	#query = "SHOW COLUMNS FROM TremCamTbl"
	cursr.execute(query)
	result = cursr.fetchall()
	conn.commit()
	#for record in result:
	#	print record 
	print cursr.rowcount
except MySQLdb.Error, e:
  
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if conn:
        conn.close()
