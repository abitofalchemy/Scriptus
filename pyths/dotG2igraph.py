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

def ConvertGraphToiGraph(args):
  print args.dotGfile
  #df = pd.read_csv(args.dotGfile, sep=' ', header=False)
  edgesArr = []
  with open(args.dotGfile, 'rb') as f:
  	for line in f:
  	  lparts = line.strip('\r\n').split(' ')
  	  if len(lparts) == 4:
  	  	edgesArr.append(lparts)
  		
  df = pd.DataFrame(edgesArr, columns=['eType','u','v','label'])
  df.to_csv(args.outFile, mode='w', sep='\t', header=False, index=False)
  print 'Saved to disk:', args.outFile, '... Done.'
  

if  __name__ =='__main__':
  parser = argparse.ArgumentParser(description='Convert .g to .ig iGraph format')
  parser.add_argument('dotGfile', help='input file path', action='store')
  parser.add_argument('outFile', help='output file .ig', action='store')
  
  args = parser.parse_args()
  
  print '\n','-'*80
  ConvertGraphToiGraph(args)
  




