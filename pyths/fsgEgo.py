#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
#
#	fsgEgo.py
#	Compute Subgraph.Nodes.Ego measures

import sys, os
import pandas as pd
import pprint 
import re, glob
import igraph as ig

def GetWirkingPath():
    working_path = "/Users/saguinag/Research/WikiGenesis/logs/"
    return working_path

def get_network_timestamp_string(net_graph_filename):
	##print inputfile
	pattern	= re.compile(r'_(\d*?)_')
	tmStamp	= pattern.search(net_graph_filename)
	graphTimeStampID  = tmStamp.group(1)
	return graphTimeStampID

def GetNodesInSubgraph():
	working_path = "/Users/saguinag/Research/WikiGenesis/logs/"
	return glob.glob(working_path+'*_emb_nodes.txt')

def LoadNetworkiG( file_str ):
	pattern = re.compile(r'(\d*?)_')
	regex_parts = pattern.search(file_str)
	net_file_timestamp = regex_parts.group(1)
	igraph_net_graph_path = "/Users/saguinag/Research/WikiGenesis/"
	igraph_net_graph_path += "wikigenesis_"+net_file_timestamp+".lg"
	print igraph_net_graph_path
	igraphObj = ig.Graph.Read_Ncol(igraph_net_graph_path)
	#print ig.summary(g)
	return igraphObj

if __name__ == "__main__":
    ## Begin
	print '-'*80

	les_files = GetNodesInSubgraph()
	node_deg_S = pd.Series()
	for ifile in les_files: 
		print ifile
		df = pd.read_csv(ifile)
		df.columns=['vId','subs-inst']
		vIdS = pd.Series(df['vId'].map(lambda x: x.split(" ")[0]), name="vIds")
		igraphObj = LoadNetworkiG(ifile)
		vDegS = pd.Series(vIdS.map(lambda x: igraphObj.degree(x, mode="all")), name="vDegree")
		df = pd.concat([vIdS,vDegS],axis=1)
		out_basename = "NetMetrics/"+os.path.basename(ifile).split('_')[0]
		df.to_csv(out_basename+"_egonet.csv", mode='w', header=True, index=False)
		print 'Saved to disk:', out_basename
		
	# print vIdS.head()
	# print vDegS.head()
