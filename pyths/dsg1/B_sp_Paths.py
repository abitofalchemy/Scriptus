#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2014
# 
# NOTES
# - This version does not fetch files of same name, so the 
#   comparisons are not matching

import os
import sys
import numpy as np
import pandas as pd
import glob
import re
import argparse
import datetime
from wikipediagame import gamesWithSourceNode


# Human Path
class Human_Paths:
    def __init__(self, file_path):
        self.file_path = file_path
        self.hp_game_usrs = []
        print 'Processing file: ' + self.file_path
        with open(self.file_path, "r") as f:
            f.readline()
            for line in f:
                line_parts = re.split(r',',line.rstrip())
                ## for ea game with SP find the matching our_algo score
                ## srcPgId_to_destPgId = sp_score
                self.hp_game_usrs.append(line_parts)
        return
# Class that grabs the list of games
class Wpg_Games:
    def __init__(self, file_path):
	self.file_path = file_path 
	self.wp_games = dict()
	print 'Processing file: ' + self.file_path
	with open(self.file_path, "r") as f: 
	    for line in f:
		line_parts = re.split(r',',line.rstrip())
                ## for ea game with SP find the matching our_algo score1G
                ## srcPgId_to_destPgId = sp_score
		self.wp_games[line_parts[0]+'_to_'+line_parts[2]] = line_parts[3]
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
def getCompletedStartNodes():
	with open ("StatsNCounts/starting_page_ids_set") as infile:
		return	[line.rstrip() for line in infile]

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
def getFilenames(inDirPath):
    filenames = filter( lambda f: not f.startswith('.'),[f for f in os.listdir(inDirPath) if os.path.isfile(os.path.join(inDirPath, f))])
    return filenames

def read_csv(file_path, has_header = True):
    with open(file_path) as f:
        if has_header: f.readline()
        data = []
        for line in f:
            line = line.strip().split(",")
            data.append([x for x in line])
    return data

def welcome(sys_argvs):
	print '\n'
	print '-'*80
	print sys_argvs
	return 
	
################################################################
##  main
###############################################################
if __name__ == "__main__":
    # Bolean declarations
    wantBasePaths = True
    
    # Get list of games that start with 100 sssp files from /data/zliu8/sssp 
    starting_path = '/data/zliu8/sssp/'
    outputFile = '/home/saguinag/CategoryPaths/ssspGamesDatFiles/path_game_sp_1.csv'
    src_pg_files = getFilenames(starting_path)
   	# Get list of starting page ids processed
    st_pg_id_nodes_proc_lst = open("StatsNCounts/s_node_proc_lst.txt").read().splitlines()

    if (wantBasePaths):
		welcome(sys.argv)
		print 'Exploring the base paths\n'
		path_chain_for_game_dict = dict()
		k = 0
		for filename in src_pg_files:
			pattern = re.compile(r'([0-9]+).txt')
			src_pg_id = pattern.search(filename)
			print  "src_pg_id.group(1)",src_pg_id.group(1)
			if src_pg_id.group(1) not in st_pg_id_nodes_proc_lst:
				print 'Processing file: ',filename
				# Grab shortest path data
				print 'Fetching shortest path data'
				shortest_path_data = Path_Data(starting_path+filename)
				sp_df = pd.DataFrame.from_dict(shortest_path_data.path_data.items())
				sp_df.columns=['key','sp']
				#print sp_df.head()

				# Show games that start with this page id
				print 'Fetching games per starting node'
				for games_plus in  gamesWithSourceNode(src_pg_id.group(1)):
					if len(games_plus) >= 3:
						path_chain_for_game_dict["%ld_to_%ld" % (games_plus[0],games_plus[2])] = games_plus[1]
					else:
						print 'games_plus is not at least 3'
				
				print 'games with starting node: ',len(path_chain_for_game_dict)
			
				gm_df = pd.DataFrame.from_dict(path_chain_for_game_dict.items())
				gm_df.columns=['key','game']
				#print gm_df.head()
			
				# Merge data frames on key
				data = pd.DataFrame()
				data = pd.merge(gm_df, sp_df, on='key')
				#print data.describe()
				data.to_csv(outputFile, sep=',', mode='a', header=False, index=False)
			k += 1
		print k
