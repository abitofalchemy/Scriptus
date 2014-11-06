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
from wikipediagame import usersPlayedNFinishedGame
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
def grep(pattern, file_obj, include_line_nums=False):
    grepper = re.compile(r'^%s\t'%pattern)
    for line_num, line in enumerate(file_obj):
        if grepper.search(line):
            if include_line_nums:
                yield (line_num, line)
            else:
                yield line

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
    """ our_algoScores.py 
        
        input: sssp folder 
        
        Outputs: 
    """
    debug = False 
    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('gm_sp_Path',help='ssspGamesDatFiles',action='store')

    args = parser.parse_args()
    fns  = getFilenames(args.gm_sp_Path) 
 
    for inputGameFn in fns:
        print inputGameFn
        result = re.search('(.*)_games_sp.dat', inputGameFn)
        outFname = re.split(r'.dat',inputGameFn.rstrip())
        outFname = '/home/saguinag/CategoryPaths/ourAlgoScores/'+outFname[0]+'_our_sp.txt'
        if not os.path.exists(outFname):
            dfHP = pd.DataFrame() #columns=['game', 'usr', 'clicks'])
            df = pd.read_csv(args.gm_sp_Path+inputGameFn, sep=',') 
            df.columns= ['src_pg','game','end_pg','sp']
            print df.shape
            ## search file
            fileToSearch = '/data/zliu8/our_algo_sort/Yay_'+result.group(1)+'_sort.txt'
            ## Now that we have the src and dest nodes, and game, we  extract the
            ## user that played the game 
            src_ouralgo_dic = {}
            iterRow = df.iterrows()
            for i,row in iterRow:
                elem_found = grep(row.end_pg, file(fileToSearch))
                if (np.size(elem_found) == 1): 
                    for elem in elem_found: 
                        scoreArr = elem.split('\t')
                        src_ouralgo_dic[row.end_pg] = scoreArr[3]
                else: 
                    src_ouralgo_dic[row.end_pg] = np.nan
                #print i 
            df['our_score'] = df.end_pg.map(src_ouralgo_dic)
            print df.head()
            ## construct a unique output filename
            df.to_csv(outFname, sep=',',mode='w',encoding='utf-8',index=False)
    print 'Done.'
