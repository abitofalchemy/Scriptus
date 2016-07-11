#!/Users/saguinag/ToolSet/anaconda/bin/python

## http://stackoverflow.com/questions/15283803/read-in-matrix-from-file-make-edgelist-and-write-edgelist-to-file

import networkx as nx
from pprint import pprint as pp

g = nx.Graph()
g.add_edge('a','b',weight=4.)
g.add_edge('b','d',weight=10.)
g.add_edge('d','f',weight=11.)
g.add_edge('a','c',weight=2.)
g.add_edge('b','c',weight=5.)
g.add_edge('c','e',weight=3.)
g.add_edge('e','d',weight=4.)

pp(nx.shortest_path(g,'a','f',weight='weight'))
pp(nx.shortest_path_length(g,'a','f',weight='weight'))




