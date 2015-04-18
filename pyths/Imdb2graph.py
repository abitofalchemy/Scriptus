#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015

import sys, os
import pandas as pd
import argparse, pprint
import glob, time
import json
import codecs, shelve
import csv
import re

def MapImdbActorsTitles2vId( ifile, shl_master_dict ):
	infileDf = pd.read_csv(ifile, sep=',', header=0)
	infileDf.convert_objects(convert_numeric=True)

	#print 'Input: .shape', infileDf.shape
	titlesDict = GetLocalTitlesDict( infileDf, shl_master_dict)
	
	## V Vertices	
	df = pd.DataFrame(sorted(titlesDict.items(), 
													 key=lambda x: x[1]))
	df.columns=['actor_title','node']
	dfix = 0
	vertices = []
	lastVertex = df['node'].tail(1) + 1
	print lastVertex,len(df['node'].index)

	for i in range(1,lastVertex):
		if (i == df['node'].iloc[dfix]):
			vertices.append("v %d AT"%df['node'].iloc[dfix])
			dfix += 1
		else:
			vertices.append("v %d -1"%i)
	## 
	os.chdir("/data/saguinag/MetaGraphs/")
	outFile = "./imdb_data/"+os.path.basename(ifile).split('.')[0]+".g"
	try:
		##			vertices.to_csv(outDotGFile, mode='w',sep=' ', index=False, encoding='utf-8', header=False)#, quoting=csv.QUOTE_NONE, quotechar='')
		odf = pd.DataFrame(vertices)
		odf.to_csv(outFile, mode='w', index=False, header=False)
	except Exception, e:
		raise e
	## 
	print 'wrote vertices to disk:',outFile
	## E Edges
	edges = []
	for index, row in infileDf.iterrows():
		line = "e %s %s wasIn" % (titlesDict[row['actor']],titlesDict[row['title_year']])		
		edges.append(line)

	try:
		  ##      vertices.to_csv(outDotGFile, mode='w',sep=' ', index=False, encoding='utf-8', header=Fals
			odf=pd.DataFrame(edges)
			odf.to_csv(outFile, mode="a", index=False, header=False)
	except Exception, e:
		raise e

def GetLocalTitlesDict( localDataFrame, masterTitlesDict ):
		titlesDict = dict()
		# ## get the vertices:
		inx = 1
		for row in localDataFrame.iterrows():
				if not titlesDict.has_key(row[1]['actor']):
						titlesDict[row[1]['actor']] = masterTitlesDict[row[1]['actor']]
						inx += 1
				if not titlesDict.has_key(row[1]['title_year']):
						titlesDict[row[1]['title_year']] = masterTitlesDict[row[1]['title_year']]
						inx +=1
				#pprint.pprint(masterDict)
				#if row[0] == 15: break

		print 'Size of _this_ dict:',len(titlesDict)

		return titlesDict


if __name__ =='__main__':
	print "\n","-"*80

	## Load masterDict to memory
	## using python's shelve read in the data file
	shelveDatFile = "/data/saguinag/Datasets/imdb/masterActorTitle2NodeId.shl"
	shl_master_dict = shelve.open(shelveDatFile, "r") 
	infile_lst = [
		"imdb_1908.csv",
			"imdb_1909.csv",
			"imdb_1910.csv"]
	
	for ifile in infile_lst:
		tic = time.clock()
		ifile = "/data/saguinag/MetaGraphs/imdb_data/"+ifile
		MapImdbActorsTitles2vId( ifile, shl_master_dict )	 #tsvs[1] )
		toc = time.clock()
		print toc-tic

	## Done
	shl_master_dict.close()
