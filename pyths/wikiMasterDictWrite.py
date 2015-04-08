#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
# References:
# 	http://iswsa.acm.org/mphf/mphf.py
# 	http://stackoverflow.com/questions/25757042/create-hash-value-for-each-row-of-data-with-selected-columns-in-dataframe-in-pyt
#	http://www.java2s.com/Tutorial/Python/0300__Database/StoringObjectsinaShelveFile.htm

import sys, os
import pandas as pd
import argparse, pprint 
import glob, time
import json
import shelve

def GetLocalTitlesDict( localDataFrame, masterTitlesDict ):
	titlesDict = dict()
	# ## get the vertices:
	inx = 1
	for row in localDataFrame.iterrows():
		if not titlesDict.has_key(row[1]['src']):
			titlesDict[row[1]['src']] = masterTitlesDict[row[1]['src']]
			inx += 1
		if not titlesDict.has_key(row[1]['trg']):
			titlesDict[row[1]['trg']] = masterTitlesDict[row[1]['trg']]
			inx +=1
		#pprint.pprint(masterDict)
		#if row[0] == 15: break
	
	print 'Size of _this_ dict:',len(titlesDict)
	return titlesDict

def MapWikiPageTitle2PageId( fileNamePath, masterDict ):
	## args ( file name with path )
	infileDf = pd.read_csv(fileNamePath, sep='\t', header=False)
	infileDf.columns=['src', 'ns0', 'trg', 'ns1']
	infileDf.convert_objects(convert_numeric=True)
	#infileDf = infileDf[:20]
	print 'tsv:', infileDf.shape

	titlesDict = GetLocalTitlesDict( infileDf, masterDict )

	i = 0
	for k,v in titlesDict.items():
		print k,v
		if i == 5: break 
		i+=1
	sys.exit()	
	## Vertices
	df = pd.DataFrame(sorted(titlesDict.items(), key=lambda x: x[1]))# masterDict.items(sort_by_values=0))
	#df = pd.DataFrame(titlesDict.items())

	df.columns=['title','node-ns']
	df['vertex'] = 'v'
	df['vId'] = df.index + 1


	vertices = df[['vertex']]
	vertices['node'] = [x for x,y in df['node-ns']] 
	vertices['ns']   = [y for x,y in df['node-ns']] 
	
	print 'Nbr of vertices in file:', vertices.shape

	## Edges																																																																
	e_dat = []										
	for index, row in infileDf.iterrows():																																																						 
		vNode = titlesDict[row[0]][0]
		#vNode = df.loc[ df['title'] == row[0] ].vId.iloc[0] 
		#uNode = df.loc[ df['title'] == row[2] ].vId.iloc[0]
		uNode = titlesDict[row[2]][0]
		#print 'e', vNode, uNode, "'linksTo'"	
		e_dat.append(['e', vNode, uNode, "'linksTo'"] )																																						
		#if index == 10: break

	edges = pd.DataFrame(e_dat) 
	#print 'Nbr of edges:', edges.shape
	#print edges.head()
	

	outFile = "wiki_genesis_data/"+os.path.basename(fileNamePath).split('.')[0]
	## Write .g file to disk
	outDotGFile = outFile +".g"
	
	try:
		vertices.to_csv(outDotGFile, mode='w',sep=' ', index=False, encoding='utf-8', header=False, quoting=csv.QUOTE_NONE)
	except Exception, e:
		raise e

	try:
		edges.to_csv(outDotGFile, mode='a',sep=' ', index=False, encoding='utf-8', header=False)
	except Exception, e:
		raise e
	print 'Wrote %s to disk' % outDotGFile

	## saving an edge-list file
	outDogLgFile = outFile +'.ig'
	try:
		edges.to_csv(outDogLgFile, mode='a',sep=' ', index=False, encoding='utf-8', header=False)
	except Exception, e:
		raise e
	print 'Wrote %s to disk' % outDogLgFile

	return
	


if	__name__ =='__main__':
	"""
	wiki2graph.py 

	Description:
	Input: 		wikigenesis*tsv
	Outputs:	masterTitle2NodeId.dat (a Python.shelve file )
				*.g  graph (veritces + edge-list) format

	We read the tsv source files, build a masterDictionary
	"""

	# parser = argparse.ArgumentParser(description='Create a look up table between page_title and page_id')
	# parser.add_argument('infile', help='Input file: wikigenesis*.tsv', action='store')
	
	# args = parser.parse_args()
	
	print "\n","-"*80

	infileDf = masterDf = pd.DataFrame()
	tsvs = glob.glob("/data/tweninge/wiki*.tsv")
	#tsvs = glob.glob("/data/tweninge/wikigenesis_1293840000000.tsv")
	for infile in tsvs:
		infileDf = pd.read_csv(infile, sep='\t', header=False)
		infileDf.columns=['src', 'ns0', 'trg', 'ns1']
		#print infileDf[infileDf['trg'] == 'Combat Infantry Badge']
		masterDf = masterDf.append(infileDf, ignore_index=True)
		
	#print master.head()
	print 'Size of  the Collection:', masterDf.shape
	
	## get the vertices master list
	## key/value
	## key = Title + NS; value = nodeId
	masterDict = dict()
	inx = 1
	for row in masterDf.iterrows():
		if not masterDict.has_key(row[1]['src']):
			masterDict["%s,%d" % (row[1]['src'],row[1]['ns0'])] = inx
			inx += 1
		if not masterDict.has_key(row[1]['trg']):
			masterDict["%s,%d" % (row[1]['trg'],row[1]['ns1'])] = inx
			inx +=1
	
	
	print 'Size of this dict:',len(masterDict)
	
	
	## write this graph's  mapped vertices to a json dictonary
		## save dictionary to disk (json format)
	outFile = "/data/saguinag/MetaGraphs/wiki_genesis_data/masterTitle2NodeId.dat"
	# with codecs.open(outFile, 'wb', encoding="utf-8")  as jf:
	# 	pickle.dump(masterDict, jf)
	# import io
	# with io.open(outFile, 'w', encoding='utf-8') as f:
 #  		f.write(unicode(json.dumps(masterDict, ensure_ascii=False)))
	titlesMasterDict = shelve.open(outFile, "n")
	titlesMasterDict.update(masterDict)
	titlesMasterDict.close()

	print "\n","-"*80


	# for infile in tsvs:
	# 	tic = time.clock()
	# 	MapWikiPageTitle2PageId( infile, masterDict )	#tsvs[1] )
	# 	toc = time.clock()
	# 	print toc-tic
	# # #break

