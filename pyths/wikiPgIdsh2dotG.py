#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015

import sys, os
import pandas as pd
import MySQLdb
import argparse, pprint 
import csv, json


def MapWikiPageTitle2PageId( fileNamePath ):
	## args (movies filename and actors or other)
	dataDf = pd.read_csv(fileNamePath, sep='\t', header=False)
	dataDf.columns=['src', 'ns0', 'trg', 'ns1']
	dataDf.convert_objects(convert_numeric=True)
	
	dataDf['src'] = dataDf['src'].str.replace(' ','_')
	dataDf['trg'] = dataDf['trg'].str.replace(' ','_')
	
	print 'Input file shape:', dataDf.shape

	grp1 = dataDf.groupby(['src', 'ns0'])
	grp2 = dataDf.groupby(['trg', 'ns1'])
	df = pd.DataFrame.from_dict(grp1.groups.keys())
	df.columns=['title','ns']
	df0 = pd.DataFrame.from_dict(grp2.groups.keys())
	df0.columns=['title','ns']

	df1 = pd.DataFrame()
	df1 = pd.concat([df, df0])
	df1['ns'].convert_objects(convert_numeric=True) ## this may have duplicates
	df1.reset_index(inplace=True)

	## test
	#tmpDict = dict()
	#for index,row in df1.iterrows():
	#	tmpDict[(row[0],row[1])] = index


	print 'Unique Src and Destination nodes list size:',df1.shape
	print 'Got key/values'

	outFile = "wiki_genesis_data/"+os.path.basename(fileNamePath).split('.')[0]
	
	## store the graph and then write it to disk
	graph_dict     = dict()
	graph_str_dict = dict()
	dotGvertices   = []

	## wikipedia/mysql
	server = 'localhost'
	conn	 = None
	try:
		conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipedia')
		cursor = conn.cursor()
		for i,k in df1.iterrows():
			if k['ns'] == 14:
				query = 'select cat_id, cat_title FROM category where cat_title = "%s";' % (k['title'])
			else:
				query = 'select page_id, page_title, page_namespace	from page where page_title = "%s" and page_namespace = "%d";' % (k['title'], k['ns'])
			cursor.execute(query)
			conn.commit()
			results = cursor.fetchall()
			if len(results)<1: # no found in wikipedia
				#print i,"huston we have a problem, titled removed from our WP"
				graph_dict[(k['title'],k['ns'])] = -1 # dict (title, ns) = page_id
				graph_str_dict["%s, %d" % (k['title'],k['ns'])] = (-1,i+1) # dict (title, ns) = (page_id, nodeId)
				dotGvertices.append(["v", i+1, '%d, %d' %(-1, k['ns'])]) # v
			elif len(results) == 1: 
				for row in results:
					#print "v %d\t'%ld, %d'" %(i+1,row[0],k['ns']) # v
					dotGvertices.append(["v", i+1, '%d, %d' %(row[0], k['ns'])]) # v
					graph_dict[(k['title'],k['ns'])] = row[0] # dict (title, ns) = page_id
					graph_str_dict["%s, %d" % (k['title'],k['ns'])] = (row[0], i+1) # dict (title, ns) = (page_id, nodeId)
			else:
				print "Huston, we have a problem, results is of size: ",len(results)
			#break
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		if conn:
			conn.close()

 		## write this graph's  mapped vertices to a json dictonary
		with open(outFile+".json", 'wb')  as jf:
			json.dump(graph_str_dict, jf)
		
		print 'Got page_ids'
		## done reading from wikipedia

	vertices = pd.DataFrame(dotGvertices)
	vertices.columns = ['element','vId', 'label']
	print 'vertices, graph_dict, graph_str_dict'
	print vertices.shape, len(graph_dict), len(graph_str_dict)

	## # # Edges																																																																
	e_dat = []										
	for index, row in dataDf.iterrows():																																																						 
		lbl_str = ("%d, %d" % (graph_dict[(row[0],row[1])], row[1]))
		vNode = vertices.loc[ vertices['label'] == lbl_str ].vId.iloc[0]
		lbl_str = ("%d, %d" % (graph_dict[(row[2],row[3])], row[3])) 
		#print index 	#
		uNode	= vertices.loc[ vertices['label'] == lbl_str ].vId.iloc[0] 
		#print 'e', vNode, uNode, "'linksTo'"																																										
		e_dat.append(['e', vNode, uNode, "'linksTo'"] )																																						

	#nodes = pd.DataFrame(v_dat)																																																									
	edges = pd.DataFrame(e_dat) 
	print 'edges shape:', edges.shape

	## Write .g file to disk
	outFile += ".g"
	try:
		vertices.to_csv(outFile, mode='w',sep=' ', index=False, encoding='utf-8', header=False)
	except Exception, e:
		raise e

	try:
		edges.to_csv(outFile, mode='a',sep=' ', index=False, encoding='utf-8', header=False)
	except Exception, e:
		raise e
	# 
	print 'Wrote .g to disk'
	return



if	__name__ =='__main__':
	parser = argparse.ArgumentParser(description='Create a look up table between page_title and page_id')
	parser.add_argument('infile', help='Input file: wikigenesis*.tsv', action='store')
	
	args = parser.parse_args()
	
	print "\n","-"*80

	out_data = MapWikiPageTitle2PageId( args.infile )
	#out_data = MapWikiPageTitle2PageId( "/data/tweninge/wikigenesis_1262304000000.tsv")
	"""with open("wiki_genesis_data/out.csv", "wb") as f:
		writer = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_MINIMAL )
		writer.writerows(out_data)
	"""
