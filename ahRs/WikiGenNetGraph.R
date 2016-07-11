## References:
# http://horicky.blogspot.com/2012/04/basic-graph-analytics-using-igraph.html

library(igraph)
## set the working dir
setwd('/Users/saguinag/Research/WikiGenesis/')

## 
in_file = "1262304000000emb_nodes.txt"
data.table = read.table(in_file, sep=" ")
head(data.table)
## load graph 
in_file = "wikigenesis_1262304000000.lg"
in_table <- read.table(in_file, sep=" ")
g <- graph.data.frame(in_table)

#degree(g,'607619', mode="all")

myList <- data.table$key
dat_deg <- list()
i <- 1
while (i<length(myList)+1)
  {
  dat_deg[i] <-degree(g,toString(myList[i]) , mode="all")
  i <- i + 1
  } 
i 
library(ggplot2)
qplot(myList, dat_deg, xlab="Horsepower", ylab="Miles per Gallon")
## metadata from the wiki graphs
#  Reference: http://rstudio-pubs-static.s3.amazonaws.com/1776_dbaebbdbde8d46e693e5cb60c768ba92.html
tsv.data  = read.delim("./logs/tsgraphs.csv")


#g <- read.table(graph_file)
#g.network<-graph.data.frame(g, directed=T) #the 'directed' attribute specifies whether the edges are directed
# edge list format review: http://cneurocvs.rmki.kfki.hu/igraphbook/igraphbook-foreign.html#id2558510

## Calculate graphlets
#gl <- graphlets(g, niter=1000)
M <- get.adjacency(g)
plot(g)

## http://bl.ocks.org/mbostock/4062045
## http://d3plus.org/workshops/11_19_2013/network/
in_file = "/Users/saguinag/Research/WikiGenesis/graphAnalysis/fsg_d3_1262304.txt"
g <- read.table(in_file, sep=" ", comment.char = "#", )
g <- read.graph(in_file, format = "edgelist")

## 
library(d3Network)
in_file = "/Users/saguinag/Research/WikiGenesis/graphAnalysis/fsg_d3_.R"
source(in_file)
## g1
NetworkData <- data.frame(g0)
d3SimpleNetwork(NetworkData, width = 200, height = 200)

grp0 <- data.frame(matrix(c(
  3,1,
  3,5,
  3,2,
  3,7,
  6,4,
  6,5,
  6,7), nrow=7, ncol=2))


grp0_ins1 <- data.frame(matrix(c(
  607619,607622,
  607619, 607624,
  607619, 607618,
  607619, 607620,
  607625, 607622,
  607625, 607624,
  607625, 607626), nrow=7,ncol=2) )
d3SimpleNetwork(grp0_ins1, width = 400, height = 200)

#g1 wiki_genesis_data/wikigenesis_1293840000000.g
g1_sub3_ins_1 <-data.frame(matrix(c( 
607619, 607622,
607619, 607624,
607619, 607618,
607619, 607620,
607625, 607622,
607625, 607624,
607625, 607626), nrow=7,ncol=2) )

# g4_sub_12_ins <- data.frame(matrix(c( 
#   607619, 607624,
#   607619, 607618,
#   607625, 607624,
#   607625, 607626), nrow=4,ncol=2) )
g <- read.table("/Users/saguinag/Research/WikiGenesis/tstgraph1.txt",header=TRUE )
g1_sub_1_ins<-data.frame(g)
g <- read.table("/Users/saguinag/Research/WikiGenesis/tstgraph2.txt",header=TRUE )
g2_sub_2_ins1<-data.frame(g)
g <- read.table("/Users/saguinag/Research/WikiGenesis/tstgraph4.txt",header=TRUE )
g4_sub_12_ins<-data.frame(g)
g <- read.table("/Users/saguinag/Research/WikiGenesis/tstgraph5.txt",header=TRUE )
g5_sub_9_ins<-data.frame(g)
d3SimpleNetwork(g5_sub_9_ins, width = 400, height = 200, file="g5_sub_9_ins.html")

## read 8v,8e graphs from file
in_file = "/Users/saguinag/Research/WikiGenesis/graphAnalysis/8v8e_graph.txt"
g <- read.table(in_file, sep=",", header=TRUE,fill=TRUE)
netDf = data.frame(g)
d3SimpleNetwork(netDf, width = 400, height = 200, file="index.html")

## fetch the entire graph
library(igraph)
library(d3Network)
in_file = "/Users/saguinag/Research/WikiGenesis/wikigenesis_1262304000000.lg"
#in_file = "/Users/saguinag/Research/WikiGenesis/wikigenesis_1388534400000.lg"

# g <- read.table(in_file, format = "edgelist")
# plot(g)
in_table <- read.table(in_file, sep=" ")
#g_df <- data.frame(in_table)
  
g <- graph.data.frame(in_table)

## http://horicky.blogspot.com/2012/04/basic-graph-analytics-using-igraph.html
## graph stats
# transitivity(g)
# centralization.degree(g)$centralization
# # centralization.closeness(g, mode="all")$centralization
# length(V(g))
# length(E(g))
# # Number of islands 
# clusters(g)$no
# # Global cluster coefficient:
# #(close triplets/all triplets)
# transitivity(g, type="global")
# degree.distribution(g)
# plot(degree.distribution(g), xlab="node degree")
# lines(degree.distribution(g))
degree(g,'607619', mode="all")
##

in_file = "/Users/saguinag/Research/WikiGenesis/tstg4s10.txt"
in_table <- read.table(in_file, sep=" ", header=TRUE)
g_df <- data.frame(in_table)
d3SimpleNetwork(g_df, width = 200, height = 200, file="index.html")

####################(18 May 2015)####################
# http://matthewlincoln.net/2014/12/20/adjacency-matrix-plots-with-r-and-ggplot2.html
library(igraph)
library(dplyr)
library(ggplot2)

setwd('/Users/saguinag/Research/MetaGraphs/wikilogs/')

# Read in CSV files with edge and node attributes
original_edgelist <- read.csv("wikigenesis_1262304000000_edgelist.txt", stringsAsFactors = FALSE, sep=" ")
original_nodelist <- read.csv("wikigenesis_1262304000000_nodelist.txt", stringsAsFactors = FALSE, sep=" ")

# Create iGraph object
graph <- graph.data.frame(original_edgelist, directed = TRUE, vertices = original_nodelist)
# Calculate various network properties, adding them as attributes
# to each node/vertex
V(graph)$comm <- membership(optimal.community(graph))
V(graph)$degree <- degree(graph)
V(graph)$closeness <- centralization.closeness(graph)$res
V(graph)$betweenness <- centralization.betweenness(graph)$res
V(graph)$eigen <- centralization.evcent(graph)$vector
# Re-generate dataframes for both nodes and edges, now containing
# calculated network attributes
node_list <- get.data.frame(graph, what = "vertices")

csv <- read.csv("tst_0.csv",header=FALSE)
# Set a gradient of colors that we will use for as many of the plots as possible
# The gradient goes from blue (negative correlations) to white (0) to red (positive correlations)
cols2 <- colorRampPalette(c("blue","white","red"))(256)
# Notice how we are only using columns 2 through 14 for the plot.
# The first column contains the region labels
# image(as.matrix(t1_data[,c(1,2,4,5)],  col = cols2, col2))
library(reshape2)
library(ggplot2)
csv.m <- melt(csv[,c(1,2,4,5)], id.vars="V1")
csv.m$V1 <- factor(csv.m$V1, levels=unique(as.character(csv.m$V1)) )
qplot(x=variable, y=V1, data=csv.m, fill=value, geom="tile") + theme(axis.text.x = element_text(angle = 90, hjust = 1)) + scale_fill_gradient2(low = "blue", mid = "white", high = "red")
