#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# mysql_dsg1.py 
#	

import sys
import MySQLdb 

#server='129.74.155.16'
server='localhost'
conn = None

try:

    #conn = MySQLdb.Connection('snoopy.cse.nd.edu', 'root', 'ixaedu1', 'neurosenz')
    #                         host    user       password    db
    conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipedia')
    cursor = conn.cursor()
    query = "SELECT \
      page_namespace, \
        ns_name, \
          page_title, \
            COUNT(*) \
            FROM revision \
            JOIN page ON page_id = rev_page \
            JOIN toolserver.namespace ON page_namespace = ns_id \
            AND dbname = 'enwiki_p' \
            GROUP BY page_namespace, page_title \
            ORDER BY COUNT(*) DESC \
            LIMIT 10;" 
    cursor.execute(query)
    conn.commit()
    print cursor.rowcount
    results = cursor.fetchall()
    print results 
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if conn:
        conn.close()
