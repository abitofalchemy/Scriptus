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
from scipy import stats


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
		directory = '/home/saguinag/public_html'
 
	# If the directory does not exist, create it
	if not os.path.exists(directory):
		os.makedirs(directory)
 
	# The final path to save to
	savepath = os.path.join(directory, filename)
        print savepath 
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
    """
     analyze Human Pahts 
        
     Parameters
     ----------
     input file or folder

    """
    parser = argparse.ArgumentParser(description='analyze Human Pahts...')
    #parser.add_argument('input_file',help='file to use',action='store')
    parser.add_argument('dir_path',help='Path to files',action='store')
    #parser.add_argument('',help='Path to files',action='store')

    args = parser.parse_args()

    pd.options.display.mpl_style = 'default'
    fig = plt.figure()
    ax = fig.add_subplot(111) #plt.gca()
    #fig.hold(True)
    ## get data files
    dataFiles = getFilenames(args.dir_path)
    for datfile in dataFiles:
        print datfile
        ##  read input file
        df =pd.read_csv(os.path.join(args.dir_path,datfile), sep=',')
        df.columns = ['hp','guuid','userid','sp']
        #print df.head()
        z_stat, p_val = stats.ranksums(df.hp,df.sp)
        print "MWW RankSum P for treatments 1 and 2 =", p_val
        break
        sys.exit()
        
        #ax.scatter(df['hp'], df['sp'])#/*, c='blue', alpha=0.05, edgecolors='none'*/)
        #plt.scatter(df['hp'], df['sp'], cmap='hot')#/*, c='blue', alpha=0.05, edgecolors='none'*/)
        #plt.plot(df['hp'], df['sp'],'o',lw=0.5, color="black", alpha=0.3)
        dfnew = df.groupby(['guuid','userid'])
        #plt.scatter(dfnew['hp'], dfnew['sp'], lw=0.5, cmap='hot', alpha=0.3)#/*, c='blue', alpha=0.05, edgecolors='none'*/)
        print dfnew.head(2)
        break

    #ax.set_yscale('log')
    ax.set_xlim([0, 40])
    ax.set_ylim([0, 5])
    save_fig('figure_plot')

    sys.exit()

# http://stackoverflow.com/questions/8151684/how-to-read-lines-from-mmap-file-in-python
# http://stackoverflow.com/questions/13872533/plot-different-dataframes-in-the-same-figure
# http://www.randalolson.com/2012/06/26/using-pandas-dataframes/

