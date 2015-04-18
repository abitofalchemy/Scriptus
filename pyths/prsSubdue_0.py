#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
import sys, os
import pandas as pd
import pprint 
import re

# logFiles = ["/home/saguinag/logs/wikigenesis_1262304000000_30Mar15_0507.log",
# 			"/home/saguinag/logs/wikigenesis_1293840000000_30Mar15_1629.log",
# 			"/home/saguinag/logs/wikigenesis_1325376000000_30Mar15_0605.log",
# 			"/home/saguinag/logs/wikigenesis_1356998400000_31Mar15_0014.log",
# 			"/home/saguinag/logs/wikigenesis_1388534400000_31Mar15_0015.log"
# 			]

## working directory
os.chdir("/home/saguinag/logs/")

logFiles = [
"wikigenesis_1262304000000_08Apr15_0625.log",
"wikigenesis_1293840000000_08Apr15_0657.log",
"wikigenesis_1325376000000_08Apr15_0657.log",
"wikigenesis_1356998400000_08Apr15_0658.log",
"wikigenesis_1388534400000_08Apr15_0658.log" ]

df = pd.DataFrame()
for inputfile in logFiles:

	pattern = re.compile(r'_(\d*?)_')
	tmStamp = pattern.search(inputfile)
	graphTSID  = tmStamp.group(1)
	data = []
	
	## Begin
	with open (inputfile, 'r') as f:
		line = f.readline()
		inx = 1
		Best = 0
		regexp = re.compile(r'Best (\d*) substructures')
		while line:
			if regexp.search(line):
				Best = 1
				data.append(line.rstrip('\n\r'))
				#print line
				lparts = regexp.search(line)
				bestSubs = lparts.group(1)	
				break
		line = f.readline()
		while k < bestSubs:
			rgxp = re.compile(r'\d*. Substructure:')
			if rgxp.search(line): 
				k +=1
				data.append(line.rstrip('\n\r'))
			line = f.readline()
		############
		pprint.pprint(data)  
	ser = pd.Series(data)
	df[str(graphTSID)] = ser
	break
## 
#print df.tail()
print df.head(10)
df.to_csv("/data/saguinag/MetaGraphs/wiki_genesis_data/tsgraphs.tsv", sep='\t', mode='w', encoding='utf-8', index=False)
print 'Done'
