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
from wikipediagame import ssspScoreToEndpageIn
import numpy as np
import pandas as pd
import glob
import re
import argparse
import datetime
from itertools import groupby
from sssp_src2dest_score import find_sssp_score
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
        Description: finds human (userid) paths for a given
        game with given staring page 
        
        input: sssp folder 
        
        Outputs: 
    """
    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('directory',help='directory to use',action='store')

    args = parser.parse_args()
    fns  = getFilenames(args.directory)
    page_id_set = [] ## declare a list
    for filename in fns:
        result = re.search('sssp_(.*).txt', filename)
        if result is not None:
            page_id_set.append(result.group(1))
    srcPageIds = np.array(page_id_set)

    ## Games that start with these page_ids

    #sys.exit() 

    write2file = 0
    for pageId in page_id_set:
        #human_paths = endpage_pageid_gameuuid_4sssp(pageId)
        #srcNdestPageIds = src_end_pageids_4sssp(pageId)
        srcNdestPageIds = humanPaths4GameStartingAt(pageId,-1)
        fn_datetime='outputFiles/'+pageId+'_human_paths.dat'
        if (write2file):
            f = open(fn_datetime,'w')
            for row in srcNdestPageIds:
                csv.writer(f).writerow(row) #f.write(row)
            f.close()
            print 'Done writing results to file io'
        else:
            data = []
            for row in srcNdestPageIds:
                data.append(row)
            df = pd.DataFrame(data)
            df.columns = ['game_uuid','userid','src_pageid','ns','endPageTitle','clicks']
            df.to_csv(fn_datetime) #print df.head()

            ## Now find shortest path score to each of the userid.game.end_page
            #endPageId = ssspScoreToEndpageIn(df['game_uuid'][0])
            #print 'clicks,  userid, game_uuid, sssp_score'
            #localFile = '%s/sssp_%s.txt' % (args.directory,pageId)
            #print localFile
            #print '%s, %s, %s, %s' % (df['clicks'][0], df['userid'][0], df['game_uuid'][0], find_sssp_score(endPageId,localFile))
    print 'Done.'
