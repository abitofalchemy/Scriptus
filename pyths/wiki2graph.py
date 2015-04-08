#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
# wiki2graph
# 	reads tsv (graph) files 
#
# Edit log:
# 	
# References:
# 	http://iswsa.acm.org/mphf/mphf.py
# 	http://stackoverflow.com/questions/25757042/create-hash-value-for-each-row-of-data-with-selected-columns-in-dataframe-in-pyt

import sys, os
import pandas as pd
import argparse, pprint 
import glob, time
import json
import codecs, shelve
import csv
import re


def GetLocalTitlesDict( localDataFrame, masterTitlesDict ):
	titlesDict = dict()
	# ## get the vertices:
	inx = 1
	for row in localDataFrame.iterrows():
		if not titlesDict.has_key("%s,%d" % (row[1]['src'],row[1]['ns0'])):
			titlesDict["%s,%d" % (row[1]['src'],row[1]['ns0'])] = masterTitlesDict["%s,%d" % (row[1]['src'],row[1]['ns0'])]
			inx += 1
		if not titlesDict.has_key("%s,%d" % (row[1]['trg'],row[1]['ns1'])):
			titlesDict["%s,%d" % (row[1]['trg'],row[1]['ns1'])] = masterTitlesDict["%s,%d" % (row[1]['trg'],row[1]['ns1'])]
			inx +=1
		#pprint.pprint(masterDict)
		#if row[0] == 15: break
	
	print 'Size of _this_ dict:',len(titlesDict)

	return titlesDict

def MapWikiPageTitle2PageId( fileNamePath, masterDict ):
	print 'Processing %s' % fileNamePath
	## args ( file name with path )
	infileDf = pd.read_csv(fileNamePath, sep='\t', header=False)
	infileDf.columns=['src', 'ns0', 'trg', 'ns1']
	infileDf.convert_objects(convert_numeric=True)
	#infileDf = infileDf[:20]
	print 'Input: tsv.shape', infileDf.shape

	titlesDict = GetLocalTitlesDict( infileDf, masterDict )

	# i = 0
	# for k,v in titlesDict.items():
	# 	print k,v
	# 	if i == 5: break 
	# 	i+=1
	# sys.exit()	


	## Vertices
	df = pd.DataFrame(sorted(titlesDict.items(), key=lambda x: x[1]))# masterDict.items(sort_by_values=0))
	df.columns=['title-ns','node']
	#df['ns']  = [re(",(.*?)$",y.split(",")[1] for y in df['title-ns']] 
	df['ns']  = [re.split(r",(\d*$)",y)[-2] for y in df['title-ns']] 
	
	# print df.head()
	# sys.exit()

	vertex_arr = []
	lastVertex = df['node'].tail(1)
	print lastVertex,len(df['node'].index)
	dfix = 0
	for i in range(1,lastVertex+1):
		if (i == df['node'].iloc[dfix]):	
			#vertex_arr.append(["v %d %d"%(df.iloc[1,dfix], df.iloc[2,dfix])])
			vertex_arr.append(["v",df['node'].iloc[dfix], df['ns'].iloc[dfix]])
			dfix += 1
		else:
			vertex_arr.append(["v",i,-1])
		#if (dfix == 2): break
	
	#df['vertex'] = 'v'
	#df['vId'] = df.index + 1

	# vertices = df[['vertex']]
	# vertices['node'] = df['node'] 
	# vertices = df[['node']] 
	# vertices['ns']   = [y.split(",")[1] for y in df['title-ns']] 
	print 'Nbr of vertices in file:', len(vertex_arr) #vertices.shape
	
	outFile = "wiki_genesis_data/"+os.path.basename(fileNamePath).split('.')[0]
	
	## Write Vertices for the .g file to disk
	## writin the vertices to disk takes considerable amount of time
	outDotGFile = outFile +".g"
	
	try:
		##	vertices.to_csv(outDotGFile, mode='w',sep=' ', index=False, encoding='utf-8', header=False)#, quoting=csv.QUOTE_NONE, quotechar='')
		with open (outDotGFile,'wb') as f:
			writer = csv.writer(f, delimiter=" ")
			writer.writerows(vertex_arr)
	except Exception, e:
		raise e

	print "\n","."*80

	##############################
	## Edges																																																																
	e_dat = []										
	for index, row in infileDf.iterrows():																																																						 
		vNode = titlesDict["%s,%d"%(row[0],row[1])]
		#vNode = df.loc[ df['title'] == row[0] ].vId.iloc[0] 
		#uNode = df.loc[ df['title'] == row[2] ].vId.iloc[0]
		uNode = titlesDict["%s,%d"%(row[2],row[3])]
		#print 'e', vNode, uNode, "'linksTo'"	
		e_dat.append(['e', vNode, uNode, "'linksTo'"] )																																						
		#if index == 10: break

	edges = pd.DataFrame(e_dat) 
	#print 'Nbr of edges:', edges.shape
	#print edges.head()
	

	

	try:
		edges.to_csv(outDotGFile, mode='a',sep=' ', index=False, encoding='utf-8', header=False)
	except Exception, e:
		raise e
	print 'Wrote %s to disk' % outDotGFile

	## saving an edge-list file
	outIgraphFile = outFile +'.ig'
	try:
		edges.to_csv(outIgraphFile, mode='a',sep=' ', index=False, encoding='utf-8', header=False)
	except Exception, e:
		raise e
	print 'Wrote %s to disk' % outIgraphFile

	return
	


if	__name__ =='__main__':
	# parser = argparse.ArgumentParser(description='Create a look up table between page_title and page_id')
	# parser.add_argument('infile', help='Input file: wikigenesis*.tsv', action='store')
	
	# args = parser.parse_args()
	
	print "\n","-"*80

	## Load masterDict to memory
	## using python's shelve read in the data file 
	shelveDatFile = "/data/saguinag/Datasets/wikigenesis/masterTitle2NodeId.dat"
	shelveMasterDict = shelve.open(shelveDatFile, "r")

	tsvs = glob.glob("/data/tweninge/wiki*.tsv")
	for infile in tsvs:
		tic = time.clock()
		MapWikiPageTitle2PageId( infile, shelveMasterDict )	#tsvs[1] )
		toc = time.clock()
		print toc-tic
		# break

