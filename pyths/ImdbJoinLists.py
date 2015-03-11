#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015

import sys, os
import argparse, re
import pandas as pd
import numpy as np
from collections import OrderedDict
from itertools import islice

def imdb_join_files(fileNamePath1, fileNamePath2):
	## args (movies filename and actors or other)
	movieDf = pd.read_csv(fileNamePath1)
	actorDf = pd.read_csv(fileNamePath2)
	

	print actorDf.head()

	
	# print 'Saving to disk...' #df.shape, df.head()
	# df.to_csv("imdb_data/imdb_movies.csv", mode='w', header=True, index=False)
	return

if	__name__ =='__main__':
	parser = argparse.ArgumentParser(description='Join/Merege Two Imdb Lists')
	parser.add_argument('list1', help='input file 1 path and list name', action='store')
	parser.add_argument('list2', help='input file 2 path and list name', action='store')
	
	args = parser.parse_args()
	print "\n","-"*80

	imdb_join_files(args.list1, args.list2)
