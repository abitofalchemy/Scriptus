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
from collections import OrderedDict
from operator import itemgetter

def parseSubdueLog ( infile ):
	with open (infile, 'rb') as f:
		data = []
		for line in f:
			if "Input file" in line:	data.append(line)
			if "Best" in line: data.append(line)
			if "pos instances" in line: data.append(line)

	return data
	'''
	outFile = "wiki_genesis_data/"+os.path.basename(fileNamePath).split('.')[0]	
	with open('thefilepath','wb') as thefile:
		file.write('\n'.join(data))
	print 'Done'
	return
	'''			
if	__name__ =='__main__':
	# parser = argparse.ArgumentParser(description='Create a look up table between page_title and page_id')
	# parser.add_argument('infile', help='Input file: wikigenesis*.tsv', action='store')
	
	# args = parser.parse_args()
	
	print "\n","-"*80

	## -minsize 3 -nsubs 100
	loghome = '/home/saguinag/logs/'
	glogs = ['wikigenesis_1262304000000_30Mar15_0002.log']
	for infile in glogs:
		tic = time.clock()
		outdata = parseSubdueLog( loghome+infile )
		outFile = loghome+os.path.basename(infile).split('.')[0]+'.txt'             
		with open(outFile,'w') as thefile:                                               
			thefile.write(''.join(outdata))                                                            
		print 'Done'
		toc = time.clock()
		print toc-tic
	#break
	
