#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# src_dest_page_ids.py 
#   source and destination page_ids	

import os
import sys
import MySQLdb 
import glob
import re
import argparse
import datetime
from itertools import groupby
import csv

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
def getFilenames(inDirPath):    
    
    filenames = filter( lambda f: not f.startswith('.'),[f for f in os.listdir(inDirPath) if os.path.isfile(os.path.join(inDirPath, f))])
    return filenames

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
def src_end_pageids_4sssp(wp_page_id):
    """ src_end_pageids_4sssp
        wp = wikipedia.page table
        input = page_id

        returns sssp filename, game uuid, end page_id

    """
    print 'input: ',wp_page_id
    
    query ="SELECT w.page_id, g.uuid, w2.page_id \
            FROM   wikipedia.page w \
            JOIN   wikipediagame.game_game g ON g.start_page = w.page_title \
            RIGHT JOIN wikipedia.page w2 ON w2.page_title = g.end_page \
            where w.page_id='%s' AND w2.page_namespace=0" % wp_page_id

    server='localhost'
    conn = None
    results=()
    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipediagame')
        cursor = conn.cursor()

        cursor.execute(query)
        conn.commit()
        #print cursor.rowcount
        #print results
        results = cursor.fetchall()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()
        return results

def endpage_pageid_gameuuid_4sssp(wp_page_id):
    """ wp = wikipedia.page table 
        input = page_id
        
        returns sssp filename, game uuid, end page_id

    """
    print 'input: ',wp_page_id
    query = "select w.page_id, w.page_title, g.uuid, g.end_page, w2.page_id, \
            gc.userid, count(gc.userid) from wikipedia.page w \
            JOIN wikipediagame.game_game g ON g.start_page=w.page_title \
            JOIN wikipedia.page w2 ON w2.page_title=g.end_page \
            JOIN wikipediagame.game_click gc ON gc.game_uuid = g.uuid \
            WHERE w.page_id='%s' and w2.page_namespace=0 \
            GROUP BY gc.userid,g.uuid DESC;" % wp_page_id

    server='localhost'
    conn = None
    results=()
    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipediagame')
        cursor = conn.cursor()

        cursor.execute(query)
        conn.commit()
        #print cursor.rowcount
        #print results
        results = cursor.fetchall()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()
        return results

################################################################
##  main
###############################################################
if __name__ == "__main__":
    """ src_dest_page_ids.py
        Description: 
        
        Arguments:
        
        Returns: 
    """
    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('directory',help='directory to use',action='store')

    args = parser.parse_args()
    fns  = getFilenames(args.directory)
    page_id_set =[]
    for filename in fns:
        #root, ext = os.path.splitext(filename)
        #if (filename.startswith("sssp_") and filename.endswith(".txt")):
        result = re.search('sssp_(.*).txt', filename)
        page_id_set.append(result.group(1))
    
    write2file = 1.0
    for pageId in page_id_set:
        #human_paths = endpage_pageid_gameuuid_4sssp(pageId)
        srcNdestPageIds = src_end_pageids_4sssp(pageId)
        if (write2file):
            fn_datetime='outputFiles/'+pageId+'_src_dest_pageIds_'+datetime.date.today().strftime("%d%b%y")+".txt"
            f = open(fn_datetime,'w')
            for row in srcNdestPageIds:
                csv.writer(f).writerow(row) #f.write(row)
            f.close()
            print 'Done writing results to file io'
    print 'Done.'
