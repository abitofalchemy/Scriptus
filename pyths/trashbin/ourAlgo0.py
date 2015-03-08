#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2014
# 
# NOTES
# - This version does not fetch files of same name, so the 
#   comparisons are not matching

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

# Class that grabs the list of games
class Wpg_Games:
    def __init__(self, directory_path):
	self.directory_path = directory_path
	self.wp_games = dict()
	for filename in os.listdir(self.directory_path):
	    if filename[0] is '.':
		continue
	    print 'Processing file: ' + filename
	    with open(self.directory_path + filename, "r") as f: 
		for line in f:
		    line_parts = re.split(r',',line.rstrip())
                    ## for ea game with SP find the matching our_algo score
                    ## srcPgId_to_destPgId = sp_score
		    self.wp_games[line_parts[0]+'_to_'+line_parts[2]] = line_parts[3]
            break 
        return
# Class that grabs data from data files
class Path_Data:

    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.path_data = dict()
        self.limit = 1 # limits the number of files processed, for testing purposes
        i = 0
        for filename in os.listdir(self.directory_path):
            if filename[0] is '.':
                continue
            print 'Processing file: ' + filename
            f = open(self.directory_path + filename)
            #ID = self.get_ID_from_name(filename)
            pattern = re.compile(r'\w_(.*).txt')
            ID = pattern.search(filename)
            pgID = ID.group(1)
            for line in f:
                line_parts = re.split(r'\s',line.rstrip())
                self.path_data[pgID + '_to_' + line_parts[0]] = line_parts[3]
            break
        return

    # Grabs the node ID from the filename
    def get_ID_from_name(self, filename):
        start = -1
        end = int()
        for i in range(0, len(filename)):
            if filename[i].isdigit():
                start = i
            if start != -1 and filename[i].isalpha:
                end = i
                break
        return filename[start:end]

################################################################
##  main
###############################################################
if __name__ == "__main__":
    """ our_algoScores.py 
    input: sssp folder 
    Outputs: 
    """
    """
    # Grab shortest path data
    print 'Fetching shortest path data'
    shortest_path_data = Path_Data('/data/zliu8/sssp/')

    # Grab the category path data
    print 'Fetching category path data'
    cat_path_data = Path_Data('/data/zliu8/our_algo/')

    # Processing data to produce correlation
    print 'Path_Data done'

    sp_df = pd.DataFrame.from_dict( shortest_path_data.path_data.items())
    cp_df = pd.DataFrame.from_dict( cat_path_data.path_data.items())

    #data = pd.DataFrame()
    #data = pd.merge(sp_df, cp_df, on='key')

    print sp_df.head()
    print cp_df.head()
    """
    # Get list of games that start with 100 sssp files from /data/zliu8/sssp
    print '-'*80
    wpgame_endpage = Wpg_Games('/home/saguinag/CategoryPaths/ssspGamesDatFiles/')
    print 'wpgame_endpage: ', len(wpgame_endpage.wp_games)

    # Processing 
    wpg_df = pd.DataFrame.from_dict(wpgame_endpage.wp_games.items())
    wpg_df.columns=['key','sp']

    ## Our Algo from src to dest score
    cat_path_data = Path_Data('/data/zliu8/our_algo/')
    cp_df = pd.DataFrame.from_dict( cat_path_data.path_data.items())
    cp_df.columns=['key','cp']

    print wpg_df.head()
    print cp_df.head()
    data = pd.DataFrame()
    data = pd.merge(wpg_df, cp_df, how='left')
    print data.shape
    print data.head()

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

################################################################
##  main
###############################################################
#if __name__ == "__main__":
#    """ our_algoScores.py 
#        
#        input: sssp folder 
#        
#        Outputs: 
#    """
#    debug = False 
#    parser = argparse.ArgumentParser(description='py pub crawler...')
#    parser.add_argument('filePath',help='ssspGamesDatFiles',action='store')
#
#    args = parser.parse_args()
#    inputGameFn = args.filePath
#     
#    print inputGameFn
#    result = re.search('/home/saguinag/CategoryPaths/ssspGamesDatFiles/(.*)_games_sp.dat', inputGameFn)
#    outFname = re.split(r'.dat',inputGameFn.rstrip())
#    outFname = '/home/saguinag/CategoryPaths/ourAlgoScores/'+result.group(1)+'_our_sp.txt'
#    if not os.path.exists(outFname):
#        dfHP = pd.DataFrame() #columns=['game', 'usr', 'clicks'])
#        df = pd.read_csv(inputGameFn, sep=',') 
#        df.columns= ['src_pg','game','end_pg','sp']
#        print df.shape
#        ## search file
#        fileToSearch = '/data/zliu8/our_algo_sort/Yay_'+result.group(1)+'_sort.txt'
#        ## Now that we have the src and dest nodes, and game, we  extract the
#        ## user that played the game 
#        src_ouralgo_dic = {}
#        iterRow = df.iterrows()
#        for i,row in iterRow:
#            elem_found = grep(row.end_pg, file(fileToSearch))
#            if (np.size(elem_found) == 1): 
#                for elem in elem_found: 
#                   scoreArr = elem.split('\t')
#                   src_ouralgo_dic[row.end_pg] = scoreArr[3]
#            else: 
#                src_ouralgo_dic[row.end_pg] = np.nan
#                #print i 
#        df['our_score'] = df.end_pg.map(src_ouralgo_dic)
#        print df.head()
#        ## construct a unique output filename
#        df.to_csv(outFname, sep=',',mode='w',encoding='utf-8',index=False)
#    print 'Done.'
