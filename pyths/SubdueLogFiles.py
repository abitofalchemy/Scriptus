#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
#	SubdueLogFiles.py
#	A class that helps parse a Subdue Log file


import sys, os
import pandas as pd
import pprint 
import re
import glob
from igraph import *
from collections import OrderedDict
import argparse

class SubdueLogFiles:
	def __init__(self, log_file):
		self.log_file = log_file
		self.fsg_inst = []
		self.fsg_models = []
		self.subgraph_nodes_dict = dict()
	
	def getSubgraphNodesInInstance(self):
		with open (self.log_file, 'r') as f:
			line = f.readline()
			Best = 0

			regexp	 = re.compile(r'Best (\d*) substructures')
			while line:	
				if regexp.search(line):
					Best = 1
					line = f.readline()
				if Best and ') Substructure' in line:
					print line.rstrip('\r\n')
					rgxp = re.compile(r'(\d*). Substructure:')
					lparts = rgxp.search(line)
					subd_subs = lparts.group(1)
					# subgraph_nodes_dict[lparts.group(1)] = 
					line = f.readline()
				if Best and 'Instance' in line:
					rgxp = re.compile(r'Instance (\d*?):')
					lparts = rgxp.search(line)
					instnc = lparts.group(1)
					#print line.rstrip('\r\n')
					line = f.readline()
					nodes = []
					while  'v ' in line:
						rgxp = re.compile(r'v (\d*?) .')
						lparts = rgxp.search(line)
						nodes.append(int (lparts.group(1)))
						line = f.readline()
					self.subgraph_nodes_dict["%s_%s"%(subd_subs,instnc)] = nodes

				line = f.readline()
			#pprint.pprint (subgraph_nodes_dict)

	def getInstancesCount(self):
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
							#print "{", substr_nbr ,":", lparts.group(1), "}"
							## Best substrugure and instance count
							self.fsg_inst.append([substr_nbr, lparts.group(1)])	# 
					line = f.readline()
				line = f.readline()
	
	def getSubstructureModels(self):
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
						self.fsg_models.append(line.split('value')[0].rstrip(": "))
					
					if 'Graph' in line:
						self.fsg_models.append(line.rstrip(':\r\n'))
					
					line = f.readline()	
				line = f.readline()
		#break # brek out the loop 
		#pprint.pprint(self.fsg_models)
		# df = pd.DataFrame.from_dict(node_embedddings_dict.items())
		# df.columns=['key','Subs-Inst']
		##
		#df.to_csv("/data/saguinag/MetaGraphs/Logs/"+graphTimeStampID+"_emb_nodes.txt",mode='w', header=True, index=False)
		
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

# def subgraph_nodes_list (subgraph):
# 	sbg_nbr = int(subgraph[0])
# 	sbg_ins = int(subgraph[1])
# 	subgraph_nodes 

if __name__ == "__main__":
	## Begin
	print '-'*80
	parser = argparse.ArgumentParser(description='Parse Subdue Ouput files')
	parser.add_argument('log_file', help='Input file: subdue log', action='store')
	parser.add_argument('igraph_file', help='Input file: .ig graph file', action='store')
	args = parser.parse_args()
    
    ## "/data/saguinag/Datasets/subdue/overlap_21Apr15_2106.log"
	logFiles = SubdueLogFiles(args.log_file)
	logFiles.getBestSubstructures()
	logFiles.getInstancesCount()
	logFiles.getSubstructureModels()
	# matrix_df = pd.DataFrame()
	matrix_df = pd.DataFrame( logFiles.fsg_inst )
	matrix_df.columns = ['fsg','instances']
	models = logFiles.fsg_models
		
	models_lst = []
	subg_weight = []
	k = 1
	while k< len(models):
		models_lst.append(models[k])
		regx = re.compile(r'Graph\((\d*?)v,(\d*?)e\)')
		lparts = regx.search(models[k])
		subg_weight.append(int(lparts.group(1))+int(lparts.group(2)))
		k+=2
	matrix_df['models'] = models_lst
	matrix_df['sbg_wt'] = subg_weight
	####
	## find the degree of graph:
	#   fsg instances		  models  sbg_wt
	# 0   1	   215	Graph(3v,2e)	   5
	# 1   2	   211	Graph(3v,2e)	   5

	logFiles.getSubgraphNodesInInstance() 
	subgs_dict = logFiles.subgraph_nodes_dict
	subgs_od   = OrderedDict(sorted(subgs_dict.items()))
		

	## "/data/saguinag/Datasets/subdue/overlap.ig"
	g = Graph()
	g = g.Read_Edgelist(args.igraph_file)
	#print 'Da graph:\n',(g)
	
	subg_nodes_dict	= dict()
	## iterate over the ordered dict 
	for skey in subgs_od:
		subg_nodes_dict[skey] = [g.degree(x) for x in subgs_od[skey]]       # sbg node degree
		
	df = pd.DataFrame.from_dict(subg_nodes_dict.items())
	df.columns =['sbg_inst','vDegree']		# dict to dataframe
	df['sDegree']   = [sum(x) for x in df['vDegree']]		# total subgraph degree
	df['sVertices'] = [len(x) for x in df['vDegree']]		# nbr of vertices in subgraph
	df['sbg'] = [x.split('_')[0] for x in df['sbg_inst']]
	df['inst'] = [x.split('_')[1] for x in df['sbg_inst']]
	print df.head()
	# print logFiles.fsg_inst
	df.to_csv("subgraphs_netanalysis.csv", index = False, quoting=0)

	## Summary
	# print matrix_df
	# print df.shape