#!/usr/bin/python 
# encoding: utf-8

"""
Process 
"""
__author__ = """Sal Aguinaga (saguinag@nd.edu)"""
#		Copyright (C) 2015
#		Sal Aguinaga <saguinag@nd.edu>
#		All rights reserved.
#		BSD license.

## Notes:
# http://stackoverflow.com/questions/7991138/easy-visualization-and-analysis-of-social-network-with-python

def wiki_brief_stat_on_graph(input_graph):
	print 'Is directed? ', nx.is_directed(input_graph)
	N, K = input_graph.order(), input_graph.size()
	avg_deg = float(K) / N
	print "Nodes: ", N
	print "Edges: ", K
	print "Average degree: ", avg_deg
	# print " CC: ", nx.number_connected_components(input_graph)
	print "SCC: ", nx.number_strongly_connected_components(input_graph) 
	print "WCC: ", nx.number_weakly_connected_components(input_graph)
	return

def match_game(x):

def prntme(x):
  print x

if __name__ == '__main__':
  import pandas as pd
  from dsg2.wikipedia import clickedPagesForGameAndUser


  print '-'*80
  ## input file to query wikipedia
  ipath = "/home/saguinag/CategoryPaths/wiki_data/wpg_paths/wpgame_end_points_8083.csv"

  trgs=[]
  with open (ipath, 'rb') as f:
    for line in f.readlines():
      line = line.strip()
      trgs.append(line)
  ds = pd.Series(trgs)
  #print ds.head()

  ## for ea target do:
  df = pd.DataFrame()
  df['trg'] = ds
  df['game'] = ds.apply(match_game)
