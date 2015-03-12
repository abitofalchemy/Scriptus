#!/usr/bin/python
# Copyright (c) Sal Aguinaga 2015
#
#	Brief description:
#	This script parses wiki genesis tsv files and converts them to
# network graph files .g 

import sys, os
import argparse, re
import pandas as pd
import numpy as np
from pprint import pprint
from collections import OrderedDict


# def create_dotG_for_wikifile(infilepath):
# 	with open (infilepath, 'rb') as f:
# 		ln = 0
# 		pgId = 0
# 		caId = 0
# 		dat    = []
# 		c1page = []
# 		c2page = []
# 		c2cat  = []
# 		firstline = f.readline()
# 		chopStr = '&quot;PC&quot; '
# 		line = firstline.lstrip(chopStr)
# 		lineParts = line.rstrip('\r\n').split('\t')	
# 		dat.append(lineParts)			
# 		if len(lineParts) == 4:
# 			c1page.append(lineParts[0])
# 			if lineParts[3] == '1':
# 				c2page.append(lineParts[2])
# 			else:
# 				c2cat.append(lineParts[2])

# 		for line in f:
# 			lineParts = line.rstrip('\r\n').split('\t')
# 			dat.append(lineParts)			
# 			if len(lineParts) == 4:                                                                              
# 				c1page.append(lineParts[0])                                                                        
# 				if lineParts[3] == '1':                                                                              
# 					c2page.append(lineParts[2])                                                                      
# 				else:                                                                                              
# 					c2cat.append(lineParts[2])
# 			if ln == 40: break
# 			ln += 1
	
# 		df = pd.DataFrame(dat, columns=['u','type','v','vtype'])
# 		left = [k for k,g in df.groupby(['u','type'])]
# 		left_df = pd.DataFrame(left, columns=['u','type'])
# 		right = [k for k,g in df.groupby(['v','vtype'])]
# 		right_df = pd.DataFrame(right, columns=['u','type'])

# 		vertices =  right_df.append(left_df, ignore_index=True)
# 		vertices = (vertices.groupby(['u','type']).groups)
		
# 		pprint (vertices) 
# 		#print [keys for keys in vertices][1] 
# 		for k in vertices:
# 			print 'v',vertices[k][0],k[1]

# 		# iterate over DataFrame rows
# 		#for index, row in df.iterrows():
				

# 		"""df = pd.DataFrame(c1page)
# 		df.columns=['wikiPg']
# 		#df.convert_objects(convert_numeric=True)
		
# 		## Idenfity unique page/articles and assign id
# 		unique =  [k for k,g in df.groupby(['wikiPg'])]
# 		c1 = pd.DataFrame(unique,columns=['wikiPg'])
# 		#c1['objId'] = list(range(len(c1.index))) # assign the pd.ix to a new column 

# 		df1 = pd.DataFrame(c2page)
# 		df1.columns=['wikiPg']
# 		unique =  [k for k,g in df1.groupby(['wikiPg'])]
# 		c2  = pd.DataFrame(unique, columns=['wikiPg'])
# 		#c2['objId'] = list(range(len(c2.index))) # assign the pd.ix to a new column 

# 		df2 = pd.DataFrame(c2cat)                                                                           
# 		df2.columns=['wikiCat']                                                                              
# 		unique =  [k for k,g in df2.groupby(['wikiCat'])]                                                    
# 		c3  = pd.DataFrame(unique,columns=['v'])                                                                           
# 		c3['objId'] = list(range(len(c3.index))) # assign the pd.ix to a new column 
		
# 		wikiPgDf = pd.merge(c1, c2, on='wikiPg',suffixes=['_left', '_right'], how='outer')
# 		wikiPgDf.append(c3)
# 		wikiPgDf['objId'] = list(range(len(wikiPgDf.index))) # assign the pd.ix to a new column 

# 		mother = pd.DataFrame(dat,columns=['wikiPg','utype','v','vtype'])
# 		mother = pd.merge(mother, wikiPgDf, on='wikiPg')
# 		mother = pd.merge(mother, c3, on='v', how='outer')
		
# 		" " " 
		
# 		wikiPg utype                                         v vtype  \
# 		0         muscle     0                              Kegel muscle     1   
# 		1  's-Heerenberg     0                                 Archangel     1   
# 		2  's-Heerenberg     0                                     Bergh     1   
# 		3  's-Heerenberg     0  Cities, towns and villages in Gelderland     2   
# 		4  's-Heerenberg     0            City rights in the Netherlands     1   
# 		5  's-Heerenberg     0                                Doetinchem     1   

# 		objId_x  objId_y  
# 		0        1      NaN  
# 		1        0      NaN  
# 		2        0      NaN  
# 		3        0        0  
# 		4        0      NaN  
# 		5        0      NaN
# 		"""


# def imdb_parse_actresses_list():
# 	print "imdb_parse_actresses_list"
# 	in_file = "/data/saguinag/Datasets/imdb/actresses.list"
# 	#
# 	with open(in_file) as f:
# 		local_data = []# key = movie, value = array of actors
# 		k = l = 0
# 		start_line_reached = False
# 		for line in f:
# 			if ('Name\t\t\tTitles') in line: start_line_reached = True
# 			line = line.replace('\t\t','')
# 			line = line.replace('\t]',']')
# 			line_parts = line.rstrip('\r\n').split('\t')
# 			if (start_line_reached and len(line_parts)>1):
# 				if len(line_parts)>2: print k, line_parts, line
# 				pattern = re.compile(r'(.*\s\(\d{4}\))')
# 				mtitle = pattern.search(line_parts[1])
# 				if mtitle is not None:
# 					k += 1
# 					#print ( [line_parts[0], mtitle.group(1)])
# 					local_data.append( [line_parts[0],mtitle.group(1)] )
# 				#if k > 10: break
# 	#print local_data
# 	return local_data

# """
# 			#lparts = re.split('\t',line.rstrip())
# 			pattern = re.compile(r'\$(.*),(.*)\t(.*)')
# 			lparts = pattern.search(line)
# 			if lparts is not None:
# 				print k, len(lparts.groups()), lparts.groups()
# 				#local_dict[lparts.group(1).replace('"', '""').replace('\t','')] = lparts.group(2)
# 				if k>15:	break
# 				k += 1
# """
# """
# 	## turn dict to pandas data frame to perform a merge
# 	paper_title_df = pd.DataFrame.from_dict(p_t_dict.items())
# 	paper_title_df.columns=['paper','title']

# 	## merge dataframes
# 	mdf = pd.DataFrame.merge(paper_title_df, author, on="paper", how="inner")
# 	print author.shape, paper_title_df.shape, mdf.shape
# 	print mdf.head()

# 	## output dataframe to disk
# 	mdf.to_csv("data/dblp_author_paper_title.csv", sep=',', mode='w', header=True, index=False)
# """
# def imdb_parse_by_actresses():
# 	aDat= imdb_parse_actresses_list()
# 	df = pd.DataFrame(aDat,columns=['Name','Titles'])
# 	print 'Saving to disk...' #df.shape, df.head()
# 	df.to_csv("imdb_data/imdb_actresses_mov_tmp.csv", mode='w', header=True, index=False)
# 	return

# def imdb_parse_by_actors():
# 	aDat= imdb_parse_actors_list()
# 	df = pd.DataFrame(aDat,columns=['actor','Titles'])
# 	print 'Saving to disk...' #df.shape, df.head()
# 	df.to_csv("imdb_data/imdb_actor_mov_tmp.csv", mode='w', header=True, index=False)
# 	return

# def imdb_parse_by_movies():
# 	aDict	= imdb_parse_movies()	
# 	aDict	= OrderedDict(sorted(aDict.items(), key=lambda t: t[1]))
# 	df = pd.DataFrame.from_dict(aDict.items())
# 	df.columns=['Titles','year']
	
# 	print 'Saving to disk...' #df.shape, df.head()
# 	df.to_csv("imdb_data/imdb_movies.csv", mode='w', header=True, index=False)
# 	return

if	__name__ =='__main__':
	parser = argparse.ArgumentParser(description='Generate a .g file from inputfile')
	parser.add_argument('wiki_ts_infile', help='input file path', action='store')
	
	args = parser.parse_args()
	print '\n','-'*80

	# create_dotG_for_wikifile(args.wiki_ts_infile)
	# print 'Done.'

	df = pd.read_csv( args.wiki_ts_infile, sep='\t', nrows=10)
	df.columns = ['u','uns', 'v', 'vns']

	#vertices = (df.groupby(['u','type']).groups)
	left = [k for k,g in df.groupby(['u','uns'])]
	left_df = pd.DataFrame(left, columns=['u','ns'])
	right = [k for k,g in df.groupby(['v','vns'])]
	right_df = pd.DataFrame(right, columns=['u','ns'])

	vertices =  right_df.append(left_df, ignore_index=True)
	#vertices['vId'] = list(range(1,len(vertices.index)+1)) ## modified the range to start at 1
	#pprint (vertices)
	uniques_at0 = (vertices.groupby(['u','ns']).groups) ## get uniques
	pprint (uniques_at0)
	uniques = pd.DataFrame.from_dict( uniques_at0.items())
	uniques.columns = ['node','vId']
	uniques['vId'] = list(range(1,len(uniques.index)+1))
	## print 'uniques: \t',uniques

	#print uniques.loc[uniques.node == ("'s-Heerenberg", 0)]


	# # Vertices
	v_dat = []
	for index, row in uniques.iterrows():
		## print 'v', row[1],row[0][1]
	# for k in uniques:
	# 	print 'v',k[0],k[1]
	# # 	v_dat.append(['v', uniques[k][0],k[1] ])
		v_dat.append(['v', row[1],row[0][1] ])

	# # # # Edges
	e_dat = []
	for index, row in df.iterrows():
		vNode  = uniques.loc[uniques['node'] == (row[0],row[1])].vId
		uNode  = uniques.loc[uniques.node == (row[2],row[3])].vId
		## print 'e', vNode.iloc[0], uNode.iloc[0], "'linksTo'"
  #		print 'e', uniques[(row[0],row[1])][0], uniques[(row[2],row[3])][0],"'links2'"
	# 	e_dat.append([uniques[(row[0],row[1])][0], uniques[(row[2],row[3])][0],"'links2'"])
		e_dat.append(['e', vNode.iloc[0], uNode.iloc[0], "'linksTo'"] )
	nodes = pd.DataFrame(v_dat)
	edges = pd.DataFrame(e_dat)
	
	try:
		nodes.to_csv('/tmp/file.g',mode='w',sep=' ', index=False, encoding='utf-8', header=False) 
	except Exception, e:
		raise e
	
	try:
		edges.to_csv('/tmp/file.g',mode='a',sep=' ', index=False, encoding='utf-8', header=False)
	except Exception, e:
		raise e
	
