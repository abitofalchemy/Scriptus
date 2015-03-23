#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015

import sys, os
import pandas as pd
import MySQLdb
import argparse, pprint 
import csv

def MapWikiPageTitle2PageId( fileNamePath ):
	## args (movies filename and actors or other)
	dataDf = pd.read_csv(fileNamePath, sep='\t', header=False)
	dataDf.columns=['src', 'ns0', 'trg', 'ns1']
	dataDf.convert_objects(convert_numeric=True)
	#dataDf.replace({' ': '_'})
	dataDf['src'] = dataDf['src'].str.replace(' ','_')
	dataDf['trg'] = dataDf['trg'].str.replace(' ','_')

	grp1 = dataDf.groupby(['src', 'ns0'])
	grp2 = dataDf.groupby(['trg', 'ns1'])
	df = pd.DataFrame.from_dict(grp1.groups.keys())
	df.columns=['title','ns']
	df0 = pd.DataFrame.from_dict(grp2.groups.keys())
	df0.columns=['title','ns']

	df1 = pd.DataFrame()
	df1 = pd.concat([df, df0])
	df1['ns'].convert_objects(convert_numeric=True)


	# outFile = "wiki_genesis_data/"+os.path.basename(fileNamePath).split('.')[0]+"_ids_dict.csv"
	# df1.to_csv(outFile,mode='w', encoding='utf-8')
  
	## store the graph and then write it to disk
	graph = []

	## wikipedia/mysql
	server = 'localhost'
	conn   = None
	try:
		conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipedia')
		cursor = conn.cursor()
		for i,k in df1.iterrows():
			query = 'select page_id, page_title, page_namespace  from page where page_title = "%s" and page_namespace = "%d";' % (k['title'], k['ns'])
			cursor.execute(query)
			conn.commit()
			results = cursor.fetchall()
			for row in results:
				#print "v %d\t'%ld, %d'" %(i+1,row[0],k['ns']) # v
				graph.append(["v", i+1, '%d, %d' %(row[0], k['ns'])]) # v
			break
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		if conn:
			conn.close()
		return graph	
	# print 'Saving to disk...' #df.shape, df.head()
	# df.to_csv("imdb_data/imdb_movies.csv", mode='w', header=True, index=False)


if	__name__ =='__main__':
	"""parser = argparse.ArgumentParser(description='Create a look up table between page_title and page_id')
	parser.add_argument('infile', help='Input file: wikigenesis*.tsv', action='store')
	
	args = parser.parse_args()
	"""
	print "\n","-"*80

	out_data = MapWikiPageTitle2PageId( "/data/tweninge/wikigenesis_1262304000000.tsv")
	with open("wiki_genesis_data/out.csv", "wb") as f:
		writer = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_MINIMAL )
		writer.writerows(out_data)
