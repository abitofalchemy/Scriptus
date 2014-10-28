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
#from wikipediagame import humanPaths4GameStartingAt
#from wikipediagame import ssspScoreToEndpageIn
#from wikipediagame import usersPlayedNFinishedGame
import numpy as np
import pandas as pd
import glob
import re
import argparse
import datetime
from itertools import groupby
#from sssp_src2dest_score import find_sssp_score
import csv
import mmap
from collections import namedtuple
import contextlib

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
def getFilenames(inDirPath):    
    
    filenames = filter( lambda f: not f.startswith('.'),[f for f in os.listdir(inDirPath) if os.path.isfile(os.path.join(inDirPath, f))])
    return filenames

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
def find_sssp_score(dest_page_id_lst,sssp_file):
    """ find_sssp_score
        needs optimization, maybe bring the
    parameters:
    -----------
        end_pageid
        sssp_file full path to file
    """
    print sssp_file
    spScore = []

    with open(sssp_file, 'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            for endPageId in dest_page_id_lst:
                pattern = re.compile(r'^%s\t' % endPageId,
                    re.DOTALL | re.IGNORECASE | re.MULTILINE)
                mp = pattern.search(m)
                if mp is not None:
                    spScore.append(mp.group().split('\t')[1])
                else:
                    spScore.append(np.nan)
    
    """
    SIZE = 2**24
    with open(sssp_file,'r') as f:
        table = build_table(f, SIZE)
        for endPageId in dest_page_id_lst:
            print endPageId
            print search(endPageId,table,f)

    df = pd.read_csv(sssp_file, sep='\t') 
    df.columns=['dest','score']
    #print df.head()


    for endPageId in dest_page_id_lst:
        print endPageId
        for index, row in df.iterrows():
            if row.dest == endPageId:
                print row.score
                spScore.append(row.score)
                break 
    """
    return spScore

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
    debug = False 
    parser = argparse.ArgumentParser(description='games for a given sssp filename')
    parser.add_argument('ssspPath',help='path to sssp filenames',action='store')
    parser.add_argument('gamesPath',help='path to games filenames',action='store')

    args = parser.parse_args()

    spFilenames = getFilenames(args.ssspPath)
    gmFilenames = getFilenames(args.gamesPath)
    
    for spFile in spFilenames:
        result = re.search('sssp_(.*).txt', spFile)
        gameDataFile = args.gamesPath+result.group(1)+'_wpgame_games.dat'
        outGamesSpFn = '/home/saguinag/CategoryPaths/ssspGamesDatFiles/'+ \
            result.group(1)+'_games_sp.dat'
        print 'spFile:',spFile
        if not os.path.exists(outGamesSpFn):
            #for inputGameFn in gameFilenames:
            print gameDataFile
            df = pd.read_csv(gameDataFile, sep=',') 
            df.columns= ['src_pg','game','end_pg'] 
            #print df.head()
            f = open(outGamesSpFn,'wb')
            ## find the paths for the array end_pg 
            ssspFileStr = args.ssspPath+'sssp_'+str(df.src_pg[0])+'.txt'
            #print ssspFileStr
            spScore = find_sssp_score(df.end_pg, ssspFileStr)	
            df['sp'] = pd.Series(spScore, index=df.index)
            #print df.head()
            df.to_csv(f,sep=',',mode='w',encoding='utf-8',index=False)
            print 'otuput:', outGamesSpFn
    #############
    print "Done."
"""
        # for each game (with source and destination) find the  
        userIdLst = []
        iterRow = df.iterrows()
        for i,row in iterRow:
            #print row.game,':'
            userIdLst = np.array(usersPlayedNFinishedGame( row.game )) #potentially multiple
	    #print len(userIdLst)
            if len(userIdLst)>1: 
	        for usrId in userIdLst: 
		    #print row.game, usrId[0], usrId[1]
                    dicts = {'game': row.game, 'usr': usrId[0], 'clicks': usrId[1]}
                    #print dicts #dfHP.append({"game": 34, "usr": 23, "clicks": 44}, ignore_index=True) 
                    dfHP = dfHP.append(dicts, ignore_index=True) 

        ## construct a unique output filename
        outFname = re.split(r'.dat',inputGameFn.rstrip())
        outFname = '/home/saguinag/CategoryPaths/humanpathsDatafiles/'+outFname[0]+'.dataframe' 
        dfHP.to_csv(outFname, sep=',',mode='w',encoding='utf-8',index=False)

    print 'Done.'

    hpfns  = getFilenames(args.humanpathsdir)
    
    if debug: print fns[:4
    if debug: print hpfns[:4]
    page_id_set = [] ## declare a list source page ids
    for filename in fns:
        result = re.search('sssp_(.*).txt', filename)
        if result is not None:
            page_id_set.append(result.group(1))
            #hpfile_set.append([s for s in hpfns if result.group(1) in s])
    srcPageIds     = np.array(page_id_set)
    if debug: print '\n> Isolated the source page_ids'

    for srcNode in srcPageIds:
        #if not (srcNode == '9475228'):
        ## for each source node
        print srcNode 
        ssspFile = [s for s in fns if srcNode in s][0]
        #if debug: print '> sssp file to search:',ssspFile

        pathFile = [s for s in hpfns if srcNode in s]
        if not (not pathFile):
            inputFile = args.humanpathsdir+'/'+pathFile[0]
            #if debug: print 'inputFile: ',inputFile
            df0 =pd.read_csv(inputFile, sep=',',index_col=0)
            #if debug: print df0.head()
            outFile = '/home/saguinag/knowledgeNetNav/dataFiles/'+srcNode+'_hp_guuid_uuid_sssp.csv' 
            if not os.path.exists(outFile):
                f = open(outFile,'wb')
                iterRow = df0[['game_uuid','userid','clicks']].iterrows()
                for i, row in iterRow:
                    endPageId = ssspScoreToEndpageIn(row.game_uuid)
                    if debug: print '> endPageId: ',endPageId[0][0],row.userid, row.game_uuid
                    ssspScoreStr = find_sssp_score(endPageId[0][0],args.directory+'/'+ssspFile)
                    if debug: print '>', ssspScoreStr 
                    if (ssspScoreStr is not None) and (endPageId is not None):
                        ssspScore = re.split(r'\t',ssspScoreStr.rstrip())    #find_sssp_score(endPageId[0][0],args.directory+'/'+ssspFile))
                        hpClicks =  row.clicks #df0[df0['game_uuid'].str.contains(guuid)]['clicks'].iloc[0]
                        hpUser   =  row.userid #df0[df0['game_uuid'].str.contains(guuid)]['userid'].iloc[0]
                        #print  '%s, %s, %s, %s' % (hpClicks,row.game_uuid, hpUser,ssspScore[1])
                        csv.writer(f).writerow([hpClicks,row.game_uuid, hpUser, ssspScore[1][0]])
                    #if None -> next item
                f.close()
                print '>',outFile
    print 'Done. Finished all source nodes'


    ## extract the sssp score for each game
        for ssspFn in filenames:
                    print ssspFn
                            result = re.search('sssp_(.*).txt', ssspFn)
                                    print result.groups()

"""
