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

#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|


################################################################
##  main
###############################################################
if __name__ == "__main__":
	"""
	analysis_humanPaths.py: analyze Human Pahts 
        
	Parameters
	----------
	input file or folder

	"""
	parser = argparse.ArgumentParser(description='analyze Human Pahts...')
	parser.add_argument('dir_path',help='Path to dataFiles',action='store')
	parser.add_argument('output',help='output: plot, ranksum, kentau = Kendalls Tau',action='store')

	args = parser.parse_args()

	## Define the dataFrame
	results = pd.DataFrame(columns=('sourceFile','MWW_RankSum','t_b1', 't_b2'))
	rnkSums = pd.DataFrame(columns=('file','nGameUsers','MWW_RankSumPvalue'))
	kndllTaus = pd.DataFrame(columns=('file','nGameUsers','tauStat', 'pValue'))
	## get data files
	dataFiles = getFilenames(args.dir_path)

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
        plt.scatter(x=df.hp, y=df.sp, lw=0.5, cmap='hot', alpha=0.3)

        i += 1
        if i == 4:
            sys.exit()
    
        
        ## Kendall's Tau using Gary Strangman's lib in SciPy
        #print "Gary Strangman's implementation of Kendall's Tau in SciPy, t_b =", stats.stats.kendalltau(df.groupby(['guid','userid']).mean().sp,df.groupby(['guid','userid']).mean().hp)
        t_b = stats.stats.kendalltau(df.groupby(['guid','userid']).mean().sp,df.groupby(['guid','userid']).mean().hp)
        #print datfile.split('_hp_guuid_uuid_sssp.csv')[0]
        ## save values to an output file
        results.loc[i] = [datfile, p_val, t_b[0], t_b[1]]
        i += 1
        #csv.writer(f).writerow([datfile, p_val, t_b])
    print results.head()
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

    sys.exit()

# http://stackoverflow.com/questions/8151684/how-to-read-lines-from-mmap-file-in-python
# http://stackoverflow.com/questions/13872533/plot-different-dataframes-in-the-same-figure
# http://www.randalolson.com/2012/06/26/using-pandas-dataframes/
# http://www.randalolson.com/2012/08/06/statistical-analysis-made-easy-in-python/
# Kendall's Tau
#   http://www2.warwick.ac.uk/fac/sci/moac/people/students/peter_cock/python/rank_correlations/
# http://stackoverflow.com/questions/10715965/add-one-row-in-a-pandas-dataframe
"""
