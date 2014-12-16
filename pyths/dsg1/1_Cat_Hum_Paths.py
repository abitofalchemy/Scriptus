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
    
    if (wantBasePaths):
		welcome(sys.argv)
		print 'Exploring the base paths\n'
		path_chain_for_game_dict = dict()
		k = 0
		for filename in src_pg_files:
			if filename is not "sssp_9475228.txt":
				print 'Processing file: ',filename
				pattern = re.compile(r'([0-9]+).txt')
				src_pg_id = pattern.search(filename)
			
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
    else:
		welcome(sys.argv)
		#print src_pg_files[:4]
		motherload = pd.DataFrame()
		path_dic = dict()
		pdLen = 0
		for filename in src_pg_files:
			pattern = re.compile(r'([0-9]+).txt')
			src_pg_id = pattern.search(filename) 

			hp_gam_path  = '/home/saguinag/CategoryPaths/hpDataFiles/'
			kFile = hp_gam_path+src_pg_id.group(1)+'_wpgame_games.dataframe'
			if not os.path.exists(kFile):    continue
			hp_game_usrs = Human_Paths(kFile)
			hp_gm_usrs_df = pd.DataFrame.from_records(hp_game_usrs.hp_game_usrs,
													  columns=('hp','game','user'))
			#print hp_gm_usrs_df.head()

			src_gam_path = '/home/saguinag/CategoryPaths/gamesDatafiles/'
			jFile = src_gam_path+src_pg_id.group(1)+'_wpgame_games.dat'
			src_gm_dest = Human_Paths(jFile)
			src_gm_dest_df = pd.DataFrame.from_records(src_gm_dest.hp_game_usrs,
													   columns=('src','game','dest'))
			print src_gm_dest_df.head()
			sys.exit()
		
		
			data = pd.DataFrame()
			data = pd.merge(hp_gm_usrs_df, src_gm_dest_df, how='left', on='game')
			pdLen += len(data)
			df = pd.concat([data.src+'_to_'+data.dest,data.user,data.hp], axis=1)
			df.columns = ['key','user','hp']
			#print df.head()
	
			## get the category paths
			our_algo_path = '/data/zliu8/our_algo/Yay_'+src_pg_id.group(1) + '.txt'
			if not os.path.exists(our_algo_path):
				print 'Warning: file %s does not exist' % (our_algo_path)
				continue
			cat_path_data = Path_Data(our_algo_path)
			cp_df = pd.DataFrame.from_dict( cat_path_data.path_data.items())
			cp_df.columns=['key','cp']
			#print cp_df.head()

			## Merge current data (dataframe) with cp_df
			df_merged = pd.DataFrame()
			df_merged = pd.merge(df, cp_df, how='left')
			#print df_merged.head()
	

			# Grow the dataframe (append at the bottom)
			motherload = pd.concat([motherload, df_merged], axis=0)
			break	

		# ends for loop
		print motherload.head()
		print 'data: ', data.shape
		print 'df_merged: ', df_merged.shape
		print 'motherload: ', motherload.shape
    
		## Save the new dataframe to disk
		motherload.to_csv(outputFile, sep=',',mode='w',encoding='utf-8',index=True)
    
    print 'Done'


