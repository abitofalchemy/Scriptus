#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015

import sys, os
import argparse, re
import pandas as pd
import numpy as np
import csv, pprint
import math
import itertools

## Begin
default_path ="/data/saguinag/MetaGraphs/"
os.chdir(default_path)
inputfile ="imdb_data/imdb_actors_movietitle.csv"
df = pd.read_csv(inputfile,header=True,nrows=10)

df.columns = ['01','00'] 
df['node'] = df.index.values

uars = [k for k,g in df.groupby(['01'])]
umov = [k for k,g in df.groupby(['00'])]

tmar = pd.DataFrame(uars)
tmar.columns = ['01']
tmar['Label'] = "01"

tmov = pd.DataFrame(umov)
tmov.columns = ['00']
tmov['Label'] = "00"


vertices = pd.concat([tmar,tmov])
#print vertices.columns
vertices['type'] = 'v'
vertices = vertices.reset_index()
vertices['node'] = vertices.index.values # remove the +1
## Reorder the columns
vertices = vertices[['type','node','Label']]

## Save vertices to disk
vertices.to_csv("imdb_data/imdb_10.gspan",mode='w', header=False, index=False, sep='\t')
print 'Saved Vertices to disk'

## EDGES
print '-'*80

#print tmov.head()
#print tmar.head()
tmar['node'] = tmar.index.values # removed the +1
tmov['node'] = tmov.index.values + len(tmar) # removed the plus 1

edges = pd.merge(df, tmar, on="01")
edges.drop('node_x',axis=1, inplace=True)
edges = pd.merge(edges, tmov, on="00")
edges['type'] = "e"
edges_g = edges[["type", "node_y", "node"]]
edges_g['Link'] = "10"
#print edges_
## Save edges to disk
edges_g.to_csv("imdb_data/imdb_10.gspan",mode='a', header=False, index=False, sep='\t')
print 'Appended edges to .g file.\nDone.'
