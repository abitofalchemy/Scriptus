#!/usr/bin/python
# -*- coding: utf-8 -*-

"""tv_get_admin_subjects.py: TremVibe extract admin's subjects to json"""
__author__  = "Salvador Aguinaga"

import sys
import MySQLdb
import json
import collections
import math
from itertools import groupby
import csv

## http://stackoverflow.com/questions/5276967/python-in-xcode-4
## http://stackoverflow.com/questions/14626613/how-can-i-recursively-add-dictionaries-in-python-from-json

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
if (len(sys.argv) < 2):
    print "Usage: tv_get_admin_subjects.py" #`"sql query`""
    exit(0)
else:
	parent_uid = sys.argv[1]
		
server = 'localhost'

try:
	conn = MySQLdb.Connection(server, 'tremcam', 'trem00xB', 'neurobit')
	#connstr = 'DRIVER={SQL Server};SERVER=localhost;USER=tremcam;PASSWORD=trem00xB;DATABASE=neurobit;'
	#conn  = pyodbc.connect(connstr)
	cursr = conn.cursor()
	query = """SELECT user_name FROM users WHERE parent_admin = %s"""
	cursr.execute(query,(parent_uid))
	conn.commit()
	row_count = cursr.rowcount
	rows = cursr.fetchall()
	#print rows
	
	# Convert query to row arrays 
	#rowarray_list = [] #rowarray_list = []
	#for row in rows:
	#	t = (row[0], row[1], row[2])
	#	rowarray_list.append(t) 
	#
	#j = json.dumps(rowarray_list)
	#rowarrays_file = 'student_rowarrays.js'
	#f = open(rowarrays_file,'w')
	#print >> f, j
	#print "printing j: ",j

	# Convert query to objects of key-value pairs
	#objects_list = []
	#for row in rows:
	#	d = collections.OrderedDict()
	#	d['id'] = row[0]
	#	d['UserName'] = row[1]
	#	d['ParentAdmin'] = row[2]
	#	objects_list.append(d)
 	#j = json.dumps(objects_list)

	## get name of the field we are 'selecting' 
	columns = [desc[0] for desc in cursr.description]
	columns = ["name","size"]
	result  = []
	heads   = []
	for row in rows:
		#row = dict((c, v) for c,v in zip(columns,row))
		row = dict((c, v) for c,v in zip(columns,[row[0],1000]))
		result.append(row)
	#print result
	heads = {"name":'you',"children": result}
	j = json.dumps(heads)
	print j
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if conn:
        conn.close()
