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
    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('gamesPath',help='directory to games/userids sets',action='store')
    #parser.add_argument('directory',help='directory to use for sssp files',action='store')
    #parser.add_argument('humanpathsdir',help='directory where human paths',action='store')

    args = parser.parse_args()
    gameFilenameLst  = getFilenames(args.gamesPath)
    # print gameFilenameLst
    
    for inputGameFn in gameFilenameLst:
        print inputGameFn
        dfHP = pd.DataFrame() #columns=['game', 'usr', 'clicks'])
        df = pd.read_csv(args.gamesPath+inputGameFn, sep=',') 
        df.columns= ['src_pg','game','end_pg'] 
        # print df.head()
        
        ## Now that we have the src and dest nodes, and game, we  extract the
        ## user that played the game 
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
"""    

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

"""
