#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
#	prsSubdueSubs.py
#	Get the Best Substructures (not actual instances)

import sys, os
import pandas as pd
import pprint 
import re
import glob


class SubdueLogFiles:
	def __init__(self, log_file):
		self.log_file = log_file
	
	def getInstances(self):
		with open (self.log_file, 'r') as f:
			line = f.readline()
			Best = 0
			regexp	 = re.compile(r'Best (\d*) substructures')
			while line:
				if regexp.search(line):
					Best = 1
					line = f.readline()
				while line and Best:
					rgxp = re.compile(r'(\d*). Substructure:')
					if rgxp.search(line):
						#data.append(line.rstrip('\r\n'))
						lparts = rgxp.search(line)
						substr_nbr = lparts.group(1)
						#print substr_nbr
						line = f.readline()
						inst_re = re.compile(r'pos instances = (\d*?), pos examples')
						if inst_re.search(line):
							lparts = inst_re.search(line)
							print "{", substr_nbr ,":", lparts.group(1), "}"
					line = f.readline()
				line = f.readline()
	
	def getSubstructureModels(self):
		data   = []
		node_embedddings_dict = dict()
		Best   = 0
		kSub   = False
		with open (self.log_file, 'r') as f:
			line = f.readline()
			regexp	 = re.compile(r'Best (\d*) substructures')
			while line:
				if regexp.search(line):
					Best = 1
				#	line = f.readline()
				while line and Best:
					rgxp = re.compile(r'(\d*). Substructure:')
					if rgxp.search(line):
						data.append(line.split('value')[0].rstrip(": "))
					
					if 'Graph' in line:
						data.append(line.rstrip(':\r\n'))
					
					line = f.readline()	
				line = f.readline()
		#break # brek out the loop 
		pprint.pprint(data)
		# df = pd.DataFrame.from_dict(node_embedddings_dict.items())
		# df.columns=['key','Subs-Inst']
		##
		#df.to_csv("/data/saguinag/MetaGraphs/Logs/"+graphTimeStampID+"_emb_nodes.txt",mode='w', header=True, index=False)
		return

	def getBestSubstructures(self):
		with open (self.log_file, 'r') as f:
			line = f.readline()
			regexp = re.compile(r'Best (\d*) substructures')
			while line:
				if regexp.search(line):
					lparts = regexp.search(line)
					print lparts.group(1)
					break
				line = f.readline()
		print "Done"



def get_network_timestamp_string(net_graph_filename):
	##print inputfile
	pattern	= re.compile(r'_(\d*?)_')
	tmStamp	= pattern.search(net_graph_filename)
	graphTimeStampID  = tmStamp.group(1)
	return graphTimeStampID

if __name__ == "__main__":
	## Begin
	print '-'*80

	logFiles = SubdueLogFiles("/home/saguinag/logs/imdb_1909_tplus1_19Apr15_1544.log")
	#logFiles.getBestSubstructures()
	logFiles.getInstances()
	logFiles.getSubstructureModels()



"""
## working directory
os.chdir("/data/saguinag/MetaGraphs/")

logFiles = glob.glob("/data/saguinag/MetaGraphs/Logs/*.log")
print logFiles[0], os.path.basename(logFiles[0])

data   = []
node_embedddings_dict = dict()
Best   = 0
for subd_log_file in logFiles:
	graphTimeStampID = get_network_timestamp_string(subd_log_file)
	with open (subd_log_file, 'r') as f:
		line = f.readline()
		regexp	 = re.compile(r'Best (\d*) substructures')
		while line:
			if regexp.search(line):
				Best = 1
				line = f.readline()
			while line and Best:
				rgxp = re.compile(r'(\d*). Substructure:')
				if rgxp.search(line):
					data.append(line.rstrip('\r\n'))
					lparts = rgxp.search(line) 
					substr_nbr = lparts.group(1)
				while 'Instance ' in line and Best:
					data.append(line.rstrip('\r\n'))
					rgxp = re.compile(r'Instance (\d*?):')
					lparts = rgxp.search(line) 
					inst_nbr = lparts.group(1)
					line = f.readline()
					while 'v ' in line:
						node_embeddings = line.lstrip(r'  v').rstrip('\n\r')
						#data.append(node_embeddings.split(' '))
						key_toks = node_embeddings.split(' ')
						node_embedddings_dict[node_embeddings] =  "%s,%s"%(substr_nbr,inst_nbr)
						line = f.readline()
				line = f.readline()
				
			line = f.readline()
	#break # brek out the loop 
	df = pd.DataFrame.from_dict(node_embedddings_dict.items())
	df.columns=['key','Subs-Inst']
	##
	df.to_csv("/data/saguinag/MetaGraphs/Logs/"+graphTimeStampID+"_emb_nodes.txt",mode='w', header=True, index=False)

sys.exit()


df = pd.DataFrame()
best_subs = dict()
for inputfile in logFiles:
	##print inputfile
	pattern	= re.compile(r'_(\d*?)_')
	tmStamp	= pattern.search(inputfile)
	graphTSID  = tmStamp.group(1)
	
	best_subs_dat = dict()
	
	
	## Begin
	with open (inputfile, 'r') as f:
		line = f.readline()
		inx  = 1
		Best = 0
		k	= 0
		GSTR = False
		lparts = []
		data   = []
		graphStructure = str()
		substr_nbr = 0
		regexp	 = re.compile(r'Best (\d*) substructures')
		while line:
			if regexp.search(line):
				Best = 1
				#data.append(line.rstrip('\n\r'))
				#print line
				lparts = regexp.search(line)
				data.append({'best_subs': lparts.group(1)})
				line = f.readline()
			rgxp = re.compile(r'(\d*). Substructure:')
			if rgxp.search(line) and Best:
				lparts = rgxp.search(line) 
				substr_nbr = lparts.group(1)
			if '  Graph(' in line and Best:
				graphStructure =  line.strip('  ').rstrip(':\n\r')
			 	#data.append({lparts.group(1): graphStructure})
			 	GSTR = True#
			 	line = f.readline()	
			if Best and GSTR:
				best_graph =[]
				while 'v ' in line or 'd ' in line:
					best_graph.append(str(line.strip('  ').rstrip('\n\r')))
					line = f.readline()	
				GSTR = False # reset flag
				data.append({substr_nbr: {graphStructure: best_graph}})
			line = f.readline()
		print 'finished: ',inputfile			
		############
		# ser = pd.Series(data)
	best_subs[ str(graphTSID) ] = data
	pprint.pprint(best_subs)
	## 
"""
