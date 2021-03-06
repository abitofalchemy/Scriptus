#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
#
#	ImdbTemporal

import sys, os
import argparse, re
import pandas as pd
import numpy as np
from collections import OrderedDict
from itertools import islice
import pprint as ppr

# References:
# regex search and get substring: 
# 	http://stackoverflow.com/questions/4666973/how-to-extract-a-substring-from-inside-a-string-in-python

def imdb_parse_movies():
	
	list_input = "imdb_data/movies.list"

	with open(list_input) as f:
		movies_dict = dict()
		k = 0
		for line in f:
			#lparts = re.split('\t',line.rstrip())
			#pattern = re.compile(r'"(.*?)"\s(\(.*\))\s+(\d*-.*)\n|"(.*?)"\s(\(.*\))\s({.*})\s*(\d*)')
			#pattern = re.compile(r'^"(.*?)"\s(\(.*\))\s+(\d*-.*)\n|"(.*?)"\s(\(.*\))\s({.*})\s*(\d*)')
			pattern = re.compile(r'(^.*)\t(\d{4}.*)')
			lparts = pattern.search(line)
			if lparts is not None:
				#print k, len(lparts.groups()), lparts.group(1).replace('"', '""')
				movies_dict[lparts.group(1).replace('"', '""').replace('\t','')] = lparts.group(2)
			
	print len(movies_dict)

	return movies_dict

def imdb_parse_actors_list():
	in_file = "imdb_data/actors.list"
	print 'imdb_parse_actors_list','\n','-'*80
	with open(in_file) as f:
		#lines = list(islice(f,1,1000))
		local_data = []# key = movie, value = array of actors
		k = l = start_line_reached = 0
		for line in f:
			if ('----\t\t\t------') in line: 
				start_line_reached = True
				continue
			else: 
				k+=1
			if not start_line_reached: continue
			pattern = re.compile(r'(.*)\t(.*\(\d{4}\))')
			line_parts= pattern.search(line)
			if line_parts is not None: 
				#print line_parts.groups()

			#line = line.replace('\tFredersdorff','Fredersdorff')
			#line = line.replace('\t\t','\t')
			#line = line.replace('\t\t','\t')
			#line = line.replace('\t]',']')
			#line_parts = line.rstrip('\r\n').split('\t')
				
				if len(line_parts.groups())>2:
					print line_parts, line
					#pattern = re.compile(r'(.*\s\(\d{4}\))')
					#mtitle = pattern.search(line_parts[1])
				local_data.append( [line_parts.group(1).replace('\t',''), 
														line_parts.group(2)] )

								#end of for loop	 
	#ppr.pprint (local_data)
	return local_data

def imdb_parse_actresses_list():
	print "imdb_parse_actresses_list"
	in_file = "imdb_data/actresses.list"
	#
	with open(in_file) as f:
		local_data = []# key = movie, value = array of actors
		k = l = 0
		start_line_reached = False
		for line in f:
			if ('Name\t\t\tTitles') in line: start_line_reached = True
			line = line.replace('\t\t','')
			line = line.replace('\t]',']')
			line_parts = line.rstrip('\r\n').split('\t')
			if (start_line_reached and len(line_parts)>1):
				if len(line_parts)>2: print k, line_parts, line
				pattern = re.compile(r'(.*\s\(\d{4}\))')
				mtitle = pattern.search(line_parts[1])
				if mtitle is not None:
					k += 1
					#print ( [line_parts[0], mtitle.group(1)])
					local_data.append( [line_parts[0],mtitle.group(1)] )
				#if k > 10: break
	#print local_data
	return local_data

"""
			#lparts = re.split('\t',line.rstrip())
			pattern = re.compile(r'\$(.*),(.*)\t(.*)')
			lparts = pattern.search(line)
			if lparts is not None:
				print k, len(lparts.groups()), lparts.groups()
				#local_dict[lparts.group(1).replace('"', '""').replace('\t','')] = lparts.group(2)
				if k>15:	break
				k += 1
"""
"""
	## turn dict to pandas data frame to perform a merge
	paper_title_df = pd.DataFrame.from_dict(p_t_dict.items())
	paper_title_df.columns=['paper','title']

	## merge dataframes
	mdf = pd.DataFrame.merge(paper_title_df, author, on="paper", how="inner")
	print author.shape, paper_title_df.shape, mdf.shape
	print mdf.head()

	## output dataframe to disk
	mdf.to_csv("data/dblp_author_paper_title.csv", sep=',', mode='w', header=True, index=False)
"""
def imdb_parse_by_actresses():
	aDat= imdb_parse_actresses_list()
	df = pd.DataFrame(aDat,columns=['Name','Titles'])
	print 'Saving to disk...' #df.shape, df.head()
	df.to_csv("imdb_data/imdb_actresses_mov_tmp.csv", mode='w', header=True, index=False)
	return

def imdb_parse_by_actors():
	aDat= imdb_parse_actors_list()
	df = pd.DataFrame(aDat,columns=['actor','Titles'])
	print 'Saving to disk...' #df.shape, df.head()
	df.to_csv("imdb_data/imdb_actor_mov_tmp.csv", mode='w', header=True, index=False)
	return

def imdb_parse_by_movies():
	aDict	= imdb_parse_movies()	
	aDict	= OrderedDict(sorted(aDict.items(), key=lambda t: t[1]))
	df = pd.DataFrame.from_dict(aDict.items())
	df.columns=['Titles','year']
	
	print 'Saving to disk...' #df.shape, df.head()
	df.to_csv("imdb_data/imdb_movies.csv", mode='w', header=True, index=False)
	return

def BuildTemporalGraph():
	start_with_file = "imdb_data/imdb_actors_movietitle.csv"
	df = pd.read_csv(start_with_file,header=True)#, nrows=100)
	df.columns =['actor','title_year']
	## print re.search(r'(\d\d\d\d)', df['title_year'].iloc[0]).group(1)
	yearKeyS = pd.Series(df['title_year'].map(lambda x: re.search(r'\((\d\d\d\d)\)', x).group(1)), name="yr")
	df['yr'] = yearKeyS
	##
	gb = df.groupby('yr')
	#print type (gb.groups), gb.groups
	# <type 'dict'> ['1986', '1985', '2015', ...
	for k,v in gb.groups.items():
		#yearlyGraphSeries = pd.Series(df.iloc[v],index=v, name=k)
		#print df.iloc[v]
		out_df = df.iloc[v]
		if out_df.shape[0]>1000 and out_df.shape[0]<5000:
			out_df.to_csv("imdb_data/imdb_"+k+".csv", mode='w', header=True, index=False)
			#print v
			#if k == '2011': break
			print k, out_df.shape 
if	__name__ =='__main__':
	## Begin
	print '-'*80

	## Build a graph that is  temporal nature and uses Actors and Titles
	BuildTemporalGraph()

