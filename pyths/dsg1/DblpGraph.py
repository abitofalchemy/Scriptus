#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015

import sys, os
import argparse


def main():
  parser = argparse.ArgumentParser(description='Generate a txt file for a graph')
  parser.add_argument('file_path', help='input file path and name', action='store')

  args = parser.parse_args()
  
  key = dict()

  with open(args.file_path) as f:
    line = f.readline()
    lparts = re.split(r'\s', line.rstrip())
    while (!lparts[1]):
      key[lparts[0]] = [lparts[2] if (lparts[2]=='author') else None,
                        lparts[2] if (lparts[2]=='year') else None ]
      line = f.readline()
           

  
if  __name__ =='__main__':
  """
  read - gspan, gaston, closegraph, spidermine (Xifeng Yan is the go to guy - he'll supply code if we want)

  dblp -> heterogeneous graph
  imdb -> heterogeneous graph

  where graph file is:
  node_id \t type_id other info
  ...
  node_id -- node_id
  """

  main()

