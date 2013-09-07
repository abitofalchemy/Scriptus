#!/usr/bin/python
# -*- coding: utf-8 -*-
#http://www.androidhive.info/2012/01/android-login-and-registration-with-php-mysql-and-sqlite/
import MySQLdb 
import sys


conn = None

try:

	conn = MySQLdb.Connection('192.168.1.148', 'tremcam', 'trem00xB', 'neurobit')
	cursr = conn.cursor()
	query = "SELECT * from TremCamTbl"
	cursr.execute(query)
	conn.commit()
	print cursr.rowcount
except MySQLdb.Error, e:
  
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if conn:
        conn.close()
