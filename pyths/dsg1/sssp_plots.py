#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# src_dest_pageid_sssp_score.py
#   source and destination page_id sssp score

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

import sys
import glob
import re
import argparse
import datetime
from itertools import groupby
import csv

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
def save_fig(path, ext='pdf', close=True, verbose=True):
	"""Save a figure from pyplot.
 
	Parameters
	----------
	path : string
	The path (and filename, without the extension) to save the
	figure to.
 
	ext : string (default='png')
	The file extension. This must be supported by the active
	matplotlib backend (see matplotlib.backends module). Most
	backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.
 
	close : boolean (default=True)
	Whether to close the figure after saving. If you want to save
	the figure multiple times (e.g., to multiple formats), you
	should NOT close it in between saves or you will have to
	re-plot it.
 
	verbose : boolean (default=True)
	Whether to print information about when and where the image
	has been saved.
 
	"""
	# Extract the directory and filename from the given path
	directory = os.path.split(path)[0]
	filename = "%s.%s" % (os.path.split(path)[1], ext)
	if directory == '':
		directory = '.'
 
	# If the directory does not exist, create it
	if not os.path.exists(directory):
		os.makedirs(directory)
 
	# The final path to save to
	savepath = os.path.join(directory, filename)
 
	if verbose:
		print("Saving figure to '%s'..." % savepath),
 
	# Actually save the figure
	plt.savefig(savepath)
	# Close it
	if close:
		plt.close()
 
	if verbose:
		print("Done")

def getFilenames(inDirPath):
    
    filenames = filter( lambda f: not f.startswith('.'),[f for f in os.listdir(inDirPath) if os.path.isfile(os.path.join(inDirPath, f))])
    return filenames

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|


################################################################
##  main
###############################################################
if __name__ == "__main__":
    """sssp_plots plots the sssp
        
        Parameters
        ----------
    """
    parser = argparse.ArgumentParser(description='py pub crawler...')
    parser.add_argument('input_file',help='file to use',action='store')

    args = parser.parse_args()
    print "Input file:", args.input_file

	##  read input file
    data = []
    with open(args.input_file, 'r') as f:
        for line in f:
            data.append(line.rstrip().split(","))
    df =pd.DataFrame(data,columns=['path','game','sp'])
    df.convert_objects(convert_numeric=True)
    #print df.convert_objects(convert_numeric=True).dtypes
    #print A.convert_objects(convert_numeric=True).describe()
    if 'score' in df.columns:
        pd.options.display.mpl_style = 'default'
        fig = plt.figure()
        ax = plt.gca()

    	ax.scatter(df['score'], df['dest'])#/*, c='blue', alpha=0.05, edgecolors='none'*/)
    	ax.set_yscale('log')
    	ax.set_xlim([0, 5])
    	#plt.xlim(0,5)
    	save_fig('figure_plot')
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        hs = ax.hist(df.sp.convert_objects(convert_numeric=True).values,alpha=0.8 )

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        #ax.spines['bottom'].set_visible(False)

        #ax.xaxis.set_ticks_position('none')
        #ax.yaxis.set_ticks_position('none')
        plt.title('Shortest Paths')
        ax.set_ylabel('count') #plt.ylabel('Count')
        ax.set_xlabel('$\mathcal{P}$ (n)') #plt.xlabel('Path Length (L)')
        save_fig('../public_html/figure_plot')
        print'Done'


# http://stackoverflow.com/questions/8151684/how-to-read-lines-from-mmap-file-in-python

