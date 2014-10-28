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
    query0 = "SELECT page_id,page_namespace,page_title from page \
            where page_id='7555441' \
            ORDER BY COUNT(*) DESC \
            LIMIT 10;" 
    query1 = "select u1.page_id,u1.page_title,u2.uuid,u2.start_page,u2.end_page from wikipedia.page u1 LEFT JOIN wikipediagame.game_game u2 ON u1.page_title = u2.start_page WHERE u1.page_id = '7555441' LIMIT 10";
    query2 = "SELECT userid,game_uuid,clicked_page from wikipediagame.game_click WHERE wikipediagame.game_click.game_uuid= '00000894fa204cb593599fce29217943' LIMIT 10;"

    
    cursor.execute(query1)
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
