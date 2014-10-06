#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# mysql_dsg1.py 
#	

import os
import sys
import MySQLdb 
import glob
import re
import argparse

def getFilenames(inDirPath):    
    
    filenames = filter( lambda f: not f.startswith('.'),[f for f in os.listdir(inDirPath) if os.path.isfile(os.path.join(inDirPath, f))])
    return filenames


################################################################
##  main
###############################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('directory',help='directory to use',action='store')

    args = parser.parse_args()
    fns  = getFilenames(args.directory)
    page_id_set =[]
    for filename in fns:
        #root, ext = os.path.splitext(filename)
        #if (filename.startswith("sssp_") and filename.endswith(".txt")):
        result = re.search('sssp_(.*).txt', filename)
        page_id_set.append(result.group(1))

    print page_id
    for pageId in page_id_set:
        generate_humanPaths (pageId)
    print ' Done.'
