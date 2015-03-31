#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
# References:
# 	http://iswsa.acm.org/mphf/mphf.py
# 	http://stackoverflow.com/questions/25757042/create-hash-value-for-each-row-of-data-with-selected-columns-in-dataframe-in-pyt

import sys, os
import pandas as pd
import argparse, pprint 
import glob, time
import hashlib, base64
import csv


def MapWikiPageTitle2PageId( fileNamePath ):
	## args ( file name with path )
	infileDf = pd.read_csv(fileNamePath, sep='\t', header=False)
	infileDf.columns=['src', 'ns0', 'trg', 'ns1']
	infileDf.convert_objects(convert_numeric=True)
	#infileDf = infileDf[:10000]
	## 
	print 'tsv:', infileDf.shape

	s1 = infileDf.ix[:,0]
	s2 = infileDf.ix[:,2]
	df = pd.concat([s1, s2], axis=0).reset_index(drop=True)

	df = pd.DataFrame(df)
	df.columns = ['title']
	grp = df.groupby(df.title).groups

	grpdf = pd.DataFrame.from_dict(grp.keys())
	grpdf.columns=['utitle']
	grpdf['element'] = 'v'
	grpdf['vId'] = grpdf.index + 1
	grpdf['label'] = pd.Series( ['"'+base64.urlsafe_b64encode(hashlib.md5(ut).digest())+'"' for ut in grpdf['utitle']])
	#grpdf['label'].astype(basestring)

	# inx = 0
	# nodes = []
	# for key in grp.keys():
	# 	strHash = base64.urlsafe_b64encode(hashlib.md5(key).digest())
	# 	nodesfull.append()
	# 	nodes.append(['v', inx, strHash])
	# 	inx += 1
	# print 'Unique # of Vertices:', len(nodes)

	vertices = grpdf[['element','vId', 'label']]
	#vertices = grpdf[['element','vId']]
	print 'Nbr of vertices in file:', vertices.shape

	## # # Edges																																																																
	e_dat = []										
	for index, row in infileDf.iterrows():																																																						 
		#lbl_str = base64.urlsafe_b64encode(hashlib.md5(row[0]).digest())
		vNode = vertices.loc[ grpdf['utitle'] == row[0]].vId.iloc[0]
		#lbl_str = base64.urlsafe_b64encode(hashlib.md5(row[2]).digest())
		uNode	= vertices.loc[ grpdf['utitle'] == row[2] ].vId.iloc[0] 
		#print 'e', vNode, uNode, "'linksTo'"	
		e_dat.append(['e', vNode, uNode, "'linksTo'"] )																																						
		#if index == 20: break
	
	edges = pd.DataFrame(e_dat) 
	print 'Nbr of edges:', edges.shape
	

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
	# parser = argparse.ArgumentParser(description='Create a look up table between page_title and page_id')
	# parser.add_argument('infile', help='Input file: wikigenesis*.tsv', action='store')
	
	# args = parser.parse_args()
	
	print "\n","-"*80
	tsvs = glob.glob("/data/tweninge/wiki*.tsv")

	#for infile in tsvs:
	tic = time.clock()
	MapWikiPageTitle2PageId( tsvs[0] )
	toc = time.clock()
	print toc-tic
	#break

