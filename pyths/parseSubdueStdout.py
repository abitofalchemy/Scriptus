#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015

import sys, os, time
import pandas as pd
import re
import argparse, pprint 
# import glob, time
# import hashlib, base64
# import csv
# from collections import OrderedDict
# from operator import itemgetter

def ParseSubdueStdout( inGraphFile ):
	print inGraphFile
	pattern = re.compile(r'_(\d*?)_')
	tmStamp = pattern.search(inGraphFile)
	fileTS  = tmStamp.group(1)
	inst = 0
	topK = 0
	with open(inGraphFile, 'r') as ifile:
	 	for line in ifile:
	 		if 'Best ' in line:	
	 			topK = line.split(' ')[1]
	 			#print topK, line
	 			continue
	 		if (topK>0 and ('(' in line)):
	 			print line 
	 			pattern = re.compile(r'^\((\d*)\)')
	 			match = pattern.search(line)
	 			currInst = match.group(1)
	 			print 'Current Instance: ', currInst


	#
	return

if	__name__ =='__main__':
	parser = argparse.ArgumentParser(description='Parse Subdue Output')
	parser.add_argument('infile', help='Input file', action='store')
	
	args = parser.parse_args()
	
	print "\n","-"*80
	
	inpuFiles = args.infile

	ParseSubdueStdout( inpuFiles )
	
