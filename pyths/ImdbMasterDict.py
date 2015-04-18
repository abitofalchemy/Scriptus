import pandas as pd
from pprint import pprint
import shelve


class Simple:
	def __init__(self, str):
		print("Inside the Simple constructor")
		self.s = str
	# Two methods:
	def show(self):
		print(self.s)
	def showMsg(self, msg):
		print(msg + ':',
		self.show()) # Calling another method

if __name__ == "__main__":
	infile_df = master_df = pd.DataFrame()
	infile_lst = [
		"imdb_1908.csv",
		"imdb_1909.csv",
		"imdb_1910.csv"]

	for infile in infile_lst:
		infile = "/data/saguinag/MetaGraphs/imdb_data/"+infile
		infile_df = pd.read_csv(infile, sep=',', header=0)
		master_df = master_df.append(infile_df)

	masterDict = dict()
	inx = 1
	for row in master_df.iterrows():
		if not masterDict.has_key(row[1]['actor']):
			masterDict[row[1]['actor']] = inx
			inx += 1
		if not masterDict.has_key(row[1]['title_year']):
			masterDict[row[1]['title_year']] = inx
			inx +=1

	print 'Size of this dict:',len(masterDict)

	# 
	outFile = "/data/saguinag/Datasets/imdb/masterActorTitle2NodeId.shl"

  # writing the dictionary to a shelve
	titlesMasterDict = shelve.open(outFile,"n")
	titlesMasterDict.update(masterDict)
	titlesMasterDict.close()

	print "\n","-"*80
