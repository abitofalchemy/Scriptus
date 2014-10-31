#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-

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


#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------
def save_fig(path, ext='pdf', close=True, verbose=True):
	"""Save a figure from pyplot.
 
	Parameters
	----------
	path : string
	The path (and filename, without the extension) to save the
	figure to.
 
	ext : string (default='pdf')
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

def scatter_plot(xvec, yvec, plt_labels):
	#print 'save',plt_labels[2]
	plt.scatter(xvec, yvec,lw=0.5, cmap='hot', alpha=0.3)#
	ax.set_xlabel(plt_labels[0])
	ax.set_ylabel(plt_labels[1])
	ax.set_title(plt_labels[2])
	#save_fig('figure_plot')	
	#save_fig('figure_plot')
	return
#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|


################################################################
##  main
###############################################################
if __name__ == "__main__":
    """
	
        .py: analyze Human Pahts 
        
	Parameters
	----------
	input file or folder

    """
    parser = argparse.ArgumentParser(description='analyze Human Pahts...')
    parser.add_argument('inHPpath',help='Path to dataFiles',action='store')
    parser.add_argument('inSPpath',help='output: plot, ranksum, kentau = Kendalls Tau',action='store')

    args = parser.parse_args()

    ## Define the dataFrame
    results = pd.DataFrame(columns=('sourceFile','MWW_RankSum','t_b1', 't_b2'))
    rnkSums = pd.DataFrame(columns=('file','nGameUsers','MWW_RankSumPvalue'))
    kndllTaus = pd.DataFrame(columns=('file','nGameUsers','tauStat', 'pValue'))
    
    ## for humanPath files 
    hpDataFilenames = getFilenames(args.inHPpath)
    spDataFilenames = getFilenames(args.inSPpath)
    outputDF  = pd.DataFrame(columns=('game','clicks','sp'))
    overallDF = pd.DataFrame(columns=('game','clicks','sp'))
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.hold(True)
    
    for filename in hpDataFilenames:
		print filename 
		result = re.search('(.*)_wpgame_games.dataframe', filename)
		#print result.group(1)
		hpDatFrm = pd.read_csv(args.inHPpath+filename,header=0,sep=',')
		## path to corresponding SP data file 
		spFile =  args.inSPpath+result.group(1)+'_games_sp.dat'
		#print spFile
		if os.path.exists(spFile):
			spDatFrm = pd.read_csv(spFile, header=0, sep=',')
            #print spDatFrm.head()
            #print hpDatFrm.head()

		for index, row in hpDatFrm.iterrows():
			## find the correspoding SP where the game matches 
			output = (spDatFrm.loc[spDatFrm.game == row.game]).sp
			## Build new data_frame
			outputDF.loc[index] =[row.game, row.clicks, output.iat[0]] 
			#break
		
		#print outputDF.shape
		concatenated = pd.concat([outputDF,overallDF])
		overallDF = concatenated
		#print overallDF.shape
		#break
		#if filename == '22462_wpgame_games.dataframe': break
    scatter_plot(overallDF.sp, overallDF.clicks, ['SP','Clicks','100 sssp files'])
    save_fig('figure_plot')
    print overallDF.shape
"""
	if args.output == 'plot':
		fig = plt.figure()
		ax = fig.add_subplot(111) #plt.gca()
		#fig.hold(True)
		i = 0
		for datfile in dataFiles:
			##  read input file
			df =pd.read_csv(os.path.join(args.dir_path,datfile), sep=',')
			df.columns = ['hp','guid','userid','sp']
			print datfile #, ':\n', df.head()
		
			##  group print the hp and sp 
			for key, grp in df.groupby(['guid','userid']):
				plt.scatter(grp.sp,grp.hp,lw=0.5, cmap='hot', alpha=0.3)#, label=key)  
				#print grouped.groups.hp, 
			break
		ax.set_xlabel('Shorterst Path')
		ax.set_ylabel('Human Paths')
		ax.set_title('Wikipediagame/Wikipedia: User/Game Pairs')
		save_fig('figure_plot')
	elif args.output == 'ranksum':
		analysisFile = '/home/saguinag/knowledgeNetNav/analysesFiles/ranksum.csv'
		for idx, datfile in enumerate(dataFiles):
			print datfile
			##  read input file
			df =pd.read_csv(os.path.join(args.dir_path,datfile), sep=',')
			df.columns = ['hp','guid','userid','sp']
			#print 
			z_stat, p_val = stats.ranksums(df.sp,df.hp)
			rnkSums.loc[idx] = [datfile,len(df), p_val]
			print "MWW RankSum P for human paths vs sp =", p_val
			
		#print rnkSums.head()
		rnkSums.to_csv(analysisFile,sep=',',mode='w',encoding='utf-8',index=False)
		print 'Done.'
# 		print ranksums.rnksmpval.describe()
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
		#plt.boxplot(rnkSums['rnksmpval'])
# 		plt.scatter(rnkSums.n,rnkSums.rnksmpval, lw=0.5, cmap='hot', alpha=0.3)
# 		plt.boxplot(rnkSums.rnksmpval)
# 		plt.scatter(rnkSums.n,rnkSums.rnksmpval, alpha=0.3)
# 		ax.set_yscale('log')
# 		ax.set_ylim([0,.])
# 		ax.set_xlabel("Depth")
		#ax.remove_border()
# 		save_fig('ranksum_hist')
# 		#plt.xlim(55, 70)
        	#csv.writer(f).writerow([datfile, p_val, t_b])
        
	elif args.output == 'kndlltau':
		analysisFile = '/home/saguinag/knowledgeNetNav/analysesFiles/kendalltau.csv'
		for idx, datfile in enumerate(dataFiles):
			print datfile
			##  read input file
			df =pd.read_csv(os.path.join(args.dir_path,datfile), sep=',')
			df.columns = ['hp','guid','userid','sp']
			
			## Kendall's Tau using Gary Strangman's lib in SciPy
			tau, p_value = stats.stats.kendalltau(df.sp,df.hp)
			#print "Gary Strangman's implementation of Kendall's Tau in SciPy, t_b =",tau,p_value 
			kndllTaus.loc[idx] = [datfile, len(df), tau, p_value]
		#print kndllTaus.head()
		fig = plt.figure()
		## 1st plot
		ax = fig.add_subplot(121)
# 		plt.scatter(kndllTaus.pValue, kndllTaus.nGameUsers, lw=0.5, cmap='hot', alpha=0.3)
		plt.boxplot(kndllTaus.pValue)
		ax.set_ylim([-0.10,1.0])
 		## Custom x-axis labels
		ax.set_xticklabels(['sp vs. hp'])
		ax.set_ylabel('pValue')
		ax.set_title('Kendall Tau')
		## 2nd plot
		ax = fig.add_subplot(122)
		plt.scatter(kndllTaus.nGameUsers, kndllTaus.pValue, lw=0.5, cmap='hot', alpha=0.3)
		ax.set_ylim([-0.10,1.0])
		ax.set_title('Kendall Tau')
		ax.set_xlabel('n (Games/Users)')
		save_fig('kendalltau')	
		kndllTaus.to_csv(analysisFile,sep=',',mode='w',encoding='utf-8',index=False)
		print 'Done.'
	else:
		print 'What do you want?'
	

"""
	
