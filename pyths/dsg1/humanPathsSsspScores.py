#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# humanPathsSsspScores.py 
#   given sssp folder, for each source node load the corresponding sssp,human paths 
#   data files, find the end_page id.  For the end_page ids list, find the sssp score in the 
#   sssp file 

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
    """ humanPathsSsspScores.py 
        
        input: sssp folder 
        
        Outputs: 
    """
    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('directory',help='directory to use',action='store')
    parser.add_argument('humanpathsdir',help='directory where human paths',action='store')

    args = parser.parse_args()
    fns  = getFilenames(args.directory)
    hpfns  = getFilenames(args.humanpathsdir)
    
    page_id_set = [] ## declare a list source page ids
    hpfile_set =[]
    for filename in fns:
        result = re.search('sssp_(.*).txt', filename)
        if result is not None:
            page_id_set.append(result.group(1))
            hpfile_set.append([s for s in hpfns if result.group(1) in s])
    srcPageIds     = np.array(page_id_set)
    hpFilenamesArr = np.array(hpfile_set)

    for hpathsFile in hpFilenamesArr:
        pathFile = args.humanpathsdir+'/'+hpathsFile[0]
        df0 =pd.read_csv(pathFile, sep=',',index_col=0)
        print df0.head()

        #      for row in srcNdestPageIds:
        #         data.append(row)
        #    df = pd.DataFrame(data)
        #   df.columns = ['game_uuid','userid','src_pageid','ns','endPageTitle','clicks']
        #  df.to_csv(fn_datetime) #print df.head()

        ## Now find shortest path score to each of the userid.game.end_page
        for guuid in df0['game_uuid']:
            endPageId = ssspScoreToEndpageIn(guuid)
            print endPageId[0][0]
            print [s for s in hpfns if result.group(1) in s]
            print find_sssp_score(endPageId[0][0])
            break 
        break
            #print 'clicks,  userid, game_uuid, sssp_score'
            #localFile = '%s/sssp_%s.txt' % (args.directory,pageId)
            #print localFile
            #print '%s, %s, %s, %s' % (df['clicks'][0], df['userid'][0], df['game_uuid'][0], find_sssp_score(endPageId,localFile))
    print 'Done.'
