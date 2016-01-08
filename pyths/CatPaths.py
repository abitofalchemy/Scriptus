#!/usr/bin/python 
# encoding: utf-8

"""
Process  
"""
__author__ = """Sal Aguinaga (saguinag@nd.edu)"""
#		Copyright (C) 2015 
#		Sal Aguinaga <saguinag@nd.edu>
#		NDDSG
#		All rights reserved.
#		BSD license.

## Notes:
# http://stackoverflow.com/questions/7991138/easy-visualization-and-analysis-of-social-network-with-python
# http://stackoverflow.com/questions/29102744/networkx-read-edgelist-in-chunks-pandas
# http://www.cl.cam.ac.uk/~an346/day2slides.pdf

def network_shortest_path(u_v_nodes_pair, page2page_net):
	if len(u_v_nodes_pair) == 2:
		uNode = u_v_nodes_pair[0]
		vNode = u_v_nodes_pair[1]
	else:
		pp('error: input nodes pair ')
		return
	
	## are pairs in the graphs
	if not uNode in page2page_net.nodes():
		pp('error: uNode not in graph')
	if not vNode in page2page_net.nodes():
		pp('error: vNode not in graph')

	##
	pp('Searching...')
	pp(nx.shortest_path(page2page_net,uNode,vNode))

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

if __name__ == '__main__':
	import networkx as nx
	from random import sample 
	from pprint import pprint as pp
	from wikicatpath import top100sssp
	## Load WikiPedia graph files
	wiki_c2c_path = "/data/bshi/dataset/wikipedia/graph/enwiki_cate_to_cate.tsv"
	wiki_p2c_path = "/data/bshi/dataset/wikipedia/graph/enwiki_page_to_cate.tsv"
	wiki_p2p_path = "/data/bshi/dataset/wikipedia/graph/enwiki_pagelink.tsv"

	# if 'c2c_g' not in locals():
	# 	with open(wiki_c2c_path) as f:
	# 		lines = f.read().splitlines()
	# 		samp_lines = [lines[i] for i in sample(xrange(len(lines)), 1000)]
	# 	c2c_g = nx.read_edgelist(lines,create_using=nx.DiGraph(), delimiter='\t',nodetype=int)
	# 	#wiki_brief_stat_on_graph(c2c_g)

	# if 'p2c_g' not in locals():
	# 	with open(wiki_p2c_path) as f:
	# 		lines = f.read().splitlines()
	# 		samp_lines = [lines[i] for i in sample(xrange(len(lines)), 1000)]
	# 	p2c_g= nx.read_edgelist(lines,create_using=nx.DiGraph(), delimiter='\t',nodetype=int)
	# 	#wiki_brief_stat_on_graph(p2c_g)

	if 'p2p_g' not in locals():
		with open(wiki_p2p_path) as f:
			lines = f.read().splitlines()
			samp_lines = [lines[i] for i in sample(xrange(len(lines)), 1000)]
		p2p_g= nx.read_edgelist(lines,create_using=nx.DiGraph(), delimiter='\t',nodetype=int)
		#wiki_brief_stat_on_graph(p2p_g)
	
	## Play with Shortest Path
	source_target_nodes = [p2p_g.nodes()[i] for i in sample(xrange(len(p2p_g.nodes())), 2)]
	pp(source_target_nodes)
	pp(network_shortest_path(source_target_nodes, p2p_g))
	
	