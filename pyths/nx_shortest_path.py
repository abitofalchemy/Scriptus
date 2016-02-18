# encoding: utf-8
"""
Routes to LANL from 186 sites on the Internet.

This uses Graphviz for layout so you need PyGraphviz or Pydot.

"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
#    Copyright (C) 2004-2008
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

# class Graph:
#   def __init__(self):
#     self.nodes = set()
#     self.edges = defaultdict(list)
#     self.distances = {}
 
#   def add_node(self, value):
#     self.nodes.add(value)
 
#   def add_edge(self, from_node, to_node, distance):
#     self.edges[from_node].append(to_node)
#     self.edges[to_node].append(from_node)
#     self.distances[(from_node, to_node)] = distance
 
 
# def dijsktra(graph, initial):
#   visited = {initial: 0}
#   path = {}
 
#   nodes = set(graph.nodes)
 
#   while nodes: 
#     min_node = None
#     for node in nodes:
#       if node in visited:
#         if min_node is None:
#           min_node = node
#         elif visited[node] < visited[min_node]:
#           min_node = node
 
#     if min_node is None:
#       break
 
#     nodes.remove(min_node)
#     current_weight = visited[min_node]
 
#     for edge in graph.edges[min_node]:
#       weight = current_weight + graph.distance[(min_node, edge)]
#       if edge not in visited or weight < visited[edge]:
#         visited[edge] = weight
#         path[edge] = min_node
 
#   return visited, path

def dijsktra(graph, initial):
  ## http://stackoverflow.com/questions/25003702/source-algorithm-for-networkx-shortest-pathg-source-target-weight-functio
  ## http://stackoverflow.com/questions/12449375/how-to-make-networkx-shortest-path-can-support-self-defined-weight-function?rq=1
  visited = {initial: 0}
  path = {}
 
  nodes = set(graph.nodes())
 
  while nodes: 
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node
 
    if min_node is None:
      break
 
    nodes.remove(min_node)
    current_weight = visited[min_node]
 
    for edge in graph.edges(min_node):
      try:
        for 
        weight = current_weight + graph.distance[(min_node, edge)]
      except:
        print 'exception'
        continue
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node
 
  return visited, path

if __name__ == '__main__':
  import networkx as nx
  ws=nx.watts_strogatz_graph(30,3,0.1)
  
  print 