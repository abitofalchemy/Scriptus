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
    #starting_path = '/data/zliu8/sssp/'
    outputPath    = '/home/saguinag/CategoryPaths/ssspGamesDatFiles/'
    
    # List of files
    #src_pg_filenames = getFilenames(starting_path)
    print "sys.argv", sys.argv
    
    filename = sys.argv[1]
    
    print 'Processing file: ',filename
    pattern = re.compile(r'([0-9]+).txt')
    src_pg_id = pattern.search(filename)
    pgID = src_pg_id.group(1)
				
    for row in gamesWithSourceNode(pgID):
        print row
    
		## Save the new dataframe to disk
#		motherload.to_csv(outputFile, sep=',',mode='w',encoding='utf-8',index=True)

    print 'Done'


