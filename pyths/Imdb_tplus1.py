#!/Users/saguinag/ToolSet/anaconda/bin/python
# /usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
#	Imdb_tplus1
#	

import sys, os
import pandas as pd
import numpy as np
import pprint 
import re
import glob

class ImdbGraph:
	def __init__(self, file_path):
		self.file_path = file_path
		self.tplusone_df   = pd.DataFrame()
		in_files = glob.glob(file_path+"/*.csv")
		self.outFileBase  = os.path.basename(in_files[1]).split('.')[0]
		self.tplusone_df  = pd.read_csv(in_files[0], header=0)
		#print tplusone_df.head()
		j = 1
		actor_title_vId_dict = dict()
		while j< len(in_files):
			df = pd.read_csv(in_files[j], header=0)
			self.tplusone_df = pd.merge(self.tplusone_df, df, on="title_year", suffixes=['_left', '_right'], how='outer')
			#tplusone_df.append(df)
			j += 1
			break
		
		##
		##	Vertices
		##
		vId = 1 # vId 
		for index, row in self.tplusone_df.iterrows():
			if row['actor_left'] is not np.NaN and (not actor_title_vId_dict.has_key("%s,%d"%(row['actor_left'],0))):
				actor_title_vId_dict["%s,%d"%(row['actor_left'],0)] = vId
				vId += 1
			if row['title_year'] is not np.NaN and (not actor_title_vId_dict.has_key("%s,%d"%(row['title_year'],1))):
				
				actor_title_vId_dict["%s,%d"%(row['title_year'],1)] = vId 
				# if 'Hunt' in row['title_year']:
				# 	print row['title_year']
				# 	print actor_title_vId_dict

				vId += 1
			if row['actor_right'] is not np.NaN and (not actor_title_vId_dict.has_key("%s,%d"%(row['actor_right'],0))):
				actor_title_vId_dict["%s,%d"%(row['actor_right'],0)] = vId
				vId += 1
		#print actor_title_vId_dict['Wolf Hunt (1908),0']
		master_df = pd.DataFrame.from_dict(actor_title_vId_dict.items())
		
		master_df.columns =['film_actor','vId']
		master_df = master_df.sort(['vId'], ascending=True)
		master_df['vertex'] = "v"
		master_df['vLabel'] = [x[-1] for x in master_df['film_actor']]
		tplusone_vertices_df = master_df[['vertex','vId','vLabel']]
		tplusone_vertices_df.to_csv(self.outFileBase+"_tplus1.g", index=False, 
				encoding='utf-8', header=False, sep=' ')
		print 'Wrote vertices to disk'

		##
		##	Edges
		##
		edges = []
		for index, row in self.tplusone_df.iterrows():
			if row['actor_left'] is not np.NaN and row['title_year'] is not np.NaN:
				edges.append(["e", 	actor_title_vId_dict["%s,%d"%(row['actor_left'],0)], 
									actor_title_vId_dict["%s,%d"%(row['title_year'],1)],"wasIn"])
			if row['title_year'] is not np.NaN and row['actor_right'] is not np.NaN:
				edges.append(["e", 	actor_title_vId_dict["%s,%d"%(row['title_year'],1)], 
									actor_title_vId_dict["%s,%d"%(row['actor_right'],0)],"wasIn"])
		edges_df = pd.DataFrame(edges)
		##
		edges_df.to_csv(self.outFileBase+"_tplus1.g", mode="a", index=False, 
				encoding='utf-8', header=False, sep=' ')
		print 'Appended edges to .g file'

	def csvTolg(self):
		##
		##	Vertices
		##
		actor_title_vId_dict = dict()
		vId = 0 # vId 
		for index, row in self.tplusone_df.iterrows():
			if row['actor_left'] is not np.NaN and (not actor_title_vId_dict.has_key("%s,%d"%(row['actor_left'],0))):
				actor_title_vId_dict["%s,%d"%(row['actor_left'],0)] = vId
				vId += 1
			if row['title_year'] is not np.NaN and (not actor_title_vId_dict.has_key("%s,%d"%(row['title_year'],1))):
				
				actor_title_vId_dict["%s,%d"%(row['title_year'],1)] = vId 
				vId += 1
			if row['actor_right'] is not np.NaN and (not actor_title_vId_dict.has_key("%s,%d"%(row['actor_right'],0))):
				actor_title_vId_dict["%s,%d"%(row['actor_right'],0)] = vId
				vId += 1
		#print actor_title_vId_dict['Wolf Hunt (1908),0']
		master_df = pd.DataFrame.from_dict(actor_title_vId_dict.items())
		
		master_df.columns =['film_actor','vId']
		master_df = master_df.sort(['vId'], ascending=True)
		print master_df.head()

		master_df['vertex'] = "v"
		master_df['vLabel'] = [x[-1] for x in master_df['film_actor']]
		tplusone_vertices_df = master_df[['vertex','vId','vLabel']]
		tplusone_vertices_df.to_csv(self.outFileBase+"_tplus1.lg", index=False, 
				encoding='utf-8', header=False, sep=' ')
		print 'Wrote vertices to disk'

		##
		##	Edges
		##
		edges = []
		for index, row in self.tplusone_df.iterrows():
			if row['actor_left'] is not np.NaN and row['title_year'] is not np.NaN:
				edges.append(["e", 	actor_title_vId_dict["%s,%d"%(row['actor_left'],0)], 
									actor_title_vId_dict["%s,%d"%(row['title_year'],1)],"wasIn"])
			if row['title_year'] is not np.NaN and row['actor_right'] is not np.NaN:
				edges.append(["e", 	actor_title_vId_dict["%s,%d"%(row['title_year'],1)], 
									actor_title_vId_dict["%s,%d"%(row['actor_right'],0)],"wasIn"])
		edges_df = pd.DataFrame(edges)
		##
		edges_df.to_csv(self.outFileBase+"_tplus1.lg", mode="a", index=False, 
				encoding='utf-8', header=False, sep=' ')
		print 'Appended edges to .lg file'

	
if	__name__ =='__main__':
	## Begin
	print '-'*80

	## Build a graph that is  temporal nature and uses Actors and Titles
	graph = ImdbGraph("./")
	print 'Generating the lg file version'
	graph.csvTolg()
