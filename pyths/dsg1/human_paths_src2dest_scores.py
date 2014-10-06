#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# human_paths_src2dest_scores.py 
#   Human paths: for a game with starting page (page_id) ource and

import os
import sys
import MySQLdb 
from wikipediagame import humanPaths4GameStartingAt
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
    """ human_paths_src2dest_scores.py
        Finds human (userid) paths for a given game with given staring page
        
        input: sssp folder 
        
        1.  For each file in the sssp folder, get the source 'page_id', use it to query wikipediagame
        and wikipedia to obtain the the number of clicks 
        
        2.  Using the source page_id, get games that have that as the starting page, find the 
        end_page and within the input filename, find the sssp score
        Outputs: 
    """
    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('directory',help='directory to use',action='store')

    args = parser.parse_args()
    fns  = getFilenames(args.directory)
    page_id_set =[] # holds the list of source page_ids
    
    for filename in fns:
        #root, ext = os.path.splitext(filename)
        #if (filename.startswith("sssp_") and filename.endswith(".txt")):
        result = re.search('sssp_(.*).txt', filename)
        page_id_set.append(result.group(1))
    
    write2file = 1.0
    for pageId in page_id_set:
        #human_paths = endpage_pageid_gameuuid_4sssp(pageId)
        #srcNdestPageIds = src_end_pageids_4sssp(pageId)
        srcNdestPageIds = humanPaths4GameStartingAt(pageId,-1)
        if (write2file):
            fn_datetime='outputFiles/human_paths_src_'+pageId+'.txt'
            f = open(fn_datetime,'w')
            for row in srcNdestPageIds:
                csv.writer(f).writerow(row) #f.write(row)
            f.close()
            print 'Done writing results to file io'
        else:
            print srcNdestPageIds
            break

    print 'Done.'
