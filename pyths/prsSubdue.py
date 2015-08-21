#!/Users/saguinag/ToolSet/anaconda/bin/python
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
os.chdir("/Users/saguinag/Public/WikiGenesis/logs/")

logFiles = [
"wikigenesis_1262304000000_08Apr15_0625.log",
"wikigenesis_1293840000000_08Apr15_0657.log",
"wikigenesis_1325376000000_08Apr15_0657.log",
"wikigenesis_1356998400000_08Apr15_0658.log",
"wikigenesis_1388534400000_08Apr15_0658.log" ]

df = pd.DataFrame()
for inputfile in logFiles:
	print inputfile
	pattern = re.compile(r'_(\d*?)_')
	tmStamp = pattern.search(inputfile)
	graphTSID  = tmStamp.group(1)
	data = []
	
	## Begin
	with open (inputfile, 'r') as f:
		line = f.readline()
		inx = 1
		Best = 0
		k = 0
		regexp = re.compile(r'Best (\d*) substructures')
		while line:

			if regexp.search(line):
				Best = 1
				data.append(line.rstrip('\n\r'))
				#print line
				lparts = regexp.search(line)
				bestSubs = lparts.group(1)	
				line = f.readline()
			rgxp = re.compile(r'\d*. Substructure:')
			if rgxp.search(line) and Best: 
				last = k
				k +=1
				data.append(line.rstrip('\n\r'))
				line = f.readline()
			while 'Instance ' in line and Best:
				data.append(line.rstrip('\n\r'))
				line = f.readline()
				while ('v ' in line) or ('d ' in line):
					data.append(line.rstrip('\n\r'))
					line = f.readline()
			line = f.readline()		
		############
	ser = pd.Series(data)
	df[str(graphTSID)] = ser
## 
print df.head(10)
df.to_csv("./tsgraphs.tsv", sep='\t', mode='w', encoding='utf-8', index=False)
print 'Done'
