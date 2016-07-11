import snap
from glob import glob

working_dir = "/home/saguinag/Phoenix/demo_graphs/"

graph_files = glob(working_dir+'*.txt')
for f in graph_files:
  mat_file = f.replace('.txt','.mtx')
  g = snap.LoadEdgeList(snap.PUNGraph, f, 0,1)
  snap.SaveMatlabSparseMtx(g,mat_file)
print glob(working_dir+'*.mtx')


