#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# mysql_dsg1.py 
#	

import sys
import MySQLdb 
import datetime
from itertools import groupby
import csv
import argparse

def execQuery(query,out2file):
    """ Query mysql on dsg1

    Returns mysql output"""
    
    server='localhost'
    conn = None
    results=()
    try:
        #                         host    user       password    db
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipediagame')
        cursor = conn.cursor()

        cursor.execute(query)
        conn.commit()
        #print cursor.rowcount
        #print results
        results = cursor.fetchall()
        if (out2file):
            fn_datetime='outputFiles/'+datetime.date.today().strftime("%d%b%y")+datetime.datetime.now().strftime("_%I%M%p")
            f = open(fn_datetime,'w')
            for row in results:
                csv.writer(f).writerow(row) #f.write(row)
            f.close()
        else:
            for row in results:
                print row;

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if conn:
            conn.close()

    return
################################################################
##  main
###############################################################
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('gameid',help='game uuid',action='store')
    parser.add_argument('userid',help='user id',action='store')

    args = parser.parse_args()
    
    query = "SELECT A.game_uuid, A.userid, B.start_page, B.end_page, A.clicked_page  \
              FROM wikipediagame.game_click     A \
              JOIN wikipediagame.game_game      B ON A.game_uuid=B.uuid \
              WHERE A.game_uuid='%s' AND A.userid='%s'" % (args.gameid, args.userid) ;
    execQuery(query,0)
