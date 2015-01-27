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
    def __init__(self, file_path):
	self.file_path = file_path 
	self.wp_games = []
	print 'Processing file: ' + self.file_path
	with open(self.file_path, "r") as f:
		f.readline()
		for line in f:
			line_parts = re.split(r',',line.rstrip())
			if len(line_parts) == 3:
				self.wp_games.append(line_parts[0]+"_to_"+ line_parts[2])
        return

class Cat_Path_Data:
    def __init__(self, file_path):
        self.file_path = file_path
        self.path_data = dict()
        print 'Processing file: ' + self.file_path
        f = open(self.file_path)
        #ID = self.get_ID_from_name(filename)
        pattern = re.compile(r'([0-9]+).txt')
        ID = pattern.search(self.file_path)
        pgID = ID.group(1)
        for line in f:
            line_parts = re.split(r'\s',line.rstrip())
            self.path_data[pgID + '_to_' + line_parts[0]] = line_parts[3]
        
        return

# Class that grabs data from data files
class Path_Data:
    def __init__(self, file_path):
        self.file_path = file_path
        self.path_data = dict()
        print 'Processing file: ' + self.file_path
        f = open(self.file_path)
        #ID = self.get_ID_from_name(filename)
        pattern = re.compile(r'([0-9]+).txt')
        ID = pattern.search(self.file_path)
        pgID = ID.group(1)
        for line in f:
            line_parts = re.split(r'\s',line.rstrip())
            self.path_data[pgID + '_to_' + line_parts[0]] = line_parts[1]
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

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
def getFilenames(inDirPath):
    filenames = filter( lambda f: not f.startswith('.'),[f for f in os.listdir(inDirPath) if os.path.isfile(os.path.join(inDirPath, f))])
    return filenames
######################
#    """
#    # Grab shortest path data
#    print 'Fetching shortest path data'
#    shortest_path_data = Path_Data('/data/zliu8/sssp/')
#
#    # Grab the category path data
#    print 'Fetching category path data'
#    cat_path_data = Path_Data('/data/zliu8/our_algo/')
#
#    # Processing data to produce correlation
#    print 'Path_Data done'
#
#    sp_df = pd.DataFrame.from_dict( shortest_path_data.path_data.items())
#    cp_df = pd.DataFrame.from_dict( cat_path_data.path_data.items())
#
#    #data = pd.DataFrame()
#    #data = pd.merge(sp_df, cp_df, on='key')
#
#    print sp_df.head()
#    print cp_df.head()
#    """
#    # Get list of games that start with 100 sssp files from /data/zliu8/sssp
#
#    src_pg_files = getFilenames('/data/zliu8/sssp/')
#    #print src_pg_files[:4]
#    for filename in src_pg_files:
#        print '\n'
#        print '-'*80
#        pattern = re.compile(r'([0-9]+).txt')
#        src_pg_id = pattern.search(filename)
#        #print src_pg_id.group(1)
#
#        ## the files to be compared/merged
#        games_path = '/home/saguinag/CategoryPaths/ssspGamesDatFiles/' \
#                     + src_pg_id.group(1) + '_games_sp.dat'
#        if not os.path.exists(games_path):
#            print 'Warning: file %s does not exist' % (games_path)
#            continue
#        our_algo_path = '/data/zliu8/our_algo/Yay_'+src_pg_id.group(1) + '.txt'
#        if not os.path.exists(our_algo_path):
#            print 'Warning: file %s does not exist' % (our_algo_path)
#            continue
#        wpgame_endpage = Wpg_Games(games_path)
#        wpg_df = pd.DataFrame.from_dict(wpgame_endpage.wp_games.items())
#        wpg_df.columns=['key','sp']
#
#        ## Our Algo from src to dest score
#        cat_path_data = Path_Data(our_algo_path)
#        cp_df = pd.DataFrame.from_dict( cat_path_data.path_data.items())
#        cp_df.columns=['key','cp']
#
#        #print wpg_df.head()
#        #print cp_df.head()
#        data = pd.DataFrame()
#        data = pd.merge(wpg_df, cp_df, how='left')
#        #print data.shape
#        #print data.head()
#
#        ## Output the new dataframe to disk
#        out_path = '/home/saguinag/CategoryPaths/ourAlgoScores/'
#        out_file_h = out_path + src_pg_id.group(1) + '_sp_cp.csv'
#        data.to_csv(out_file_h, sep=',',mode='w',encoding='utf-8',index=False)
#    print 'Done.'
def category_shortest_paths_gen():
    # Start
    starting_path = ('/data/zliu8/sssp/')
    our_algo_path = ('/data/zliu8/our_algo/')
    
    filenames4pageId   = getFilenames(starting_path)  # source page id filenames
    filenames_our_algo = getFilenames(our_algo_path)  #
    
    motherload = pd.DataFrame()
    for file in filenames4pageId:
        # Grab shortest path data
        print 'Fetching shortest path data'
        shortest_path_data = Path_Data(starting_path+file)
        
        # Grab category path data
        print 'Fetching category path data'
        pattern = re.compile(r'([0-9]+).txt')
        ID = pattern.search(file)
        pgID = ID.group(1)
        our_algo_file = "Yay_"+pgID+".txt"
        cat_path_data = Cat_Path_Data(our_algo_path+our_algo_file)
        #
        # Processing data to produce correlation
        print 'Path_Data done'
        
        sp_df = pd.DataFrame.from_dict( shortest_path_data.path_data.items())
        sp_df.columns=['key','sp']
        print sp_df.head()
        cp_df = pd.DataFrame.from_dict( cat_path_data.path_data.items())
        cp_df.columns=['key','cp']
        print cp_df.head()
        #
        print "sp_df:", sp_df.shape
        print "cp_df:", cp_df.shape
        data = pd.DataFrame()
        data = pd.merge(sp_df, cp_df, on='key')
        #
        # Save data to disk
        output_file = "/home/saguinag/CategoryPaths/cat_vs_shortest_paths/"+"cat_sp_"+pgID+".csv"
        if not os.path.exists(output_file):
            data.to_csv(output_file, sep=',',mode='w',encoding='utf-8',index=True)
# ends for loop
    return
################################################################
##  main
###############################################################
if __name__ == "__main__":
    """ CatPaths.py
        Description:
        
    """

    # generate the files
    # category_shortest_paths_gen()

    # Given the generated files, filter by games with matching end points (destination page_ids)
    # Start
    starting_sssp_path     = "/data/zliu8/sssp/"
    category_shortest_path = "cat_vs_shortest_paths/"
    games_by_src_node_path = "gamesDatafiles/"
    
    filenames = getFilenames(starting_sssp_path)

    for file in filenames:
        pattern = re.compile(r'([0-9]+).txt')
        ID = pattern.search(file)
        pgID = ID.group(1)
        #
        gameDataFilename = pgID+"_wpgame_games.dat"
        print "Data for games starting with source node",pgID
        games_by_src_data = Wpg_Games(games_by_src_node_path+gameDataFilename)
        ## to dataframe
        gm_df = pd.DataFrame(games_by_src_data.wp_games, columns=['key'])
        #print gm_df.head()
        
        catSpFilename =category_shortest_path + "cat_sp_"+ pgID + ".csv"
        catSp_df = pd.read_csv(catSpFilename, index_col=0)
        #print catSp_df.head()
        
        # Merge data frames on key
        min_data_df = pd.DataFrame()
        min_data_df = pd.merge(gm_df, catSp_df, on='key')
        # on key ... some are removed, so instead of 174 we are left with about 169
        # b/c some games have the same start and end points (needs to be investigated)
        
        outputFile = "cp_sp_filtered/"+ pgID +"_cp_sp_filt.csv"
        min_data_df.to_csv(outputFile, sep=',', mode='w', header=True, index=False)
        
        