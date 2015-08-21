#!/usr/bin/python
import sys, linecache
import pandas as pd

## Begin

infile = "/home/saguinag/MetaGraphs/imdb/imdb_10000.g"
with open(infile, 'r') as f:
	line = f.readline()
	while 'v' in line:
		lparts = line.rstrip('\n\r').split()
		print int(lparts[1])+1

		break
