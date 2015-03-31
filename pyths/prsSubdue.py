#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
import sys, os
import pandas as pd
import pprint 
import re

logFiles = ["/home/saguinag/logs/wikigenesis_1262304000000_30Mar15_0507.log",
			"/home/saguinag/logs/wikigenesis_1293840000000_30Mar15_1629.log",
			"/home/saguinag/logs/wikigenesis_1325376000000_30Mar15_0605.log",
			"/home/saguinag/logs/wikigenesis_1356998400000_31Mar15_0014.log",
			"/home/saguinag/logs/wikigenesis_1388534400000_31Mar15_0015.log"
			]

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
		while line:
			if 'Best' in line and inx > 32 :
				Best = 1
				data.append(line.rstrip('\n\r'))
			if ') Substructure:' in line and Best:
				#print line
				data.append(line.rstrip('\n\r'))
			if 'pos instances' in line and Best:
				data.append(line.lstrip('\s').rstrip('\n\r'))

			while 'Instance ' in line and Best:
				data.append(line.rstrip('\n\r'))
				line = f.readline()
				#print line 
				while 'v ' in line or 'd ' in line:
					data.append(line.rstrip('\n\r'))
					line = f.readline()
				line = f.readline()
				#break
			line = f.readline()
			inx += 1

		############
		#pprint.pprint(data)  
	ser = pd.Series(data)
	df[str(graphTSID)] = ser
## 
#print df.tail()
print df.head()
df.to_csv("/data/saguinag/MetaGraphs/wiki_genesis_data/tsgraphs.tsv", sep='\t', mode='w', encoding='utf-8', index=False)
print 'Done'
