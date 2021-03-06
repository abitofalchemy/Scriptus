#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/5276967/python-in-xcode-4

"""tv_list_registered_users.py: list registered users"""
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
server='localhost'
conn = None
print_local = 1
try:
    
    #conn = MySQLdb.Connection('snoopy.cse.nd.edu', 'root', 'ixaedu1', 'neurosenz')
    conn = MySQLdb.Connection(server, 'triaxim', 'tria00xB', 'neurobit')
    cursr = conn.cursor()
    query = "SELECT email from TremCamTbl"
    cursr.execute(query)
    conn.commit()
        #print cursr.rowcount
    row_count = cursr.rowcount
    results     = cursr.fetchall()
    if (print_local):
        emailDict =  parse_email_records(row_count, results)
        for email in emailDict:
            print email
    else:
        emailDict =  parse_email_records(row_count, results)
        with open("/var/www/tremcam/subjects.csv", "wb") as f:
            csv.writer(f).writerow(['Subject', 'Records'])
            for email in emailDict:
                #print email,',',len(emailDict[email])
                csv.writer(f).writerow([email, len(emailDict[email])])
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if conn:
        conn.close()
