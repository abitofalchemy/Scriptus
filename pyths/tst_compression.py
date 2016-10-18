#!/usr/bin/python

import networkx as nx
import datetime
import pickle


def load_cliques_obj():
    pickleFileName = "/data/saguinag/datasets/arxiv/cond_mat_03_cliques.pkl"
    t0 = datetime.datetime.now()
    with open(pickleFileName, 'rb') as ifile:
        data = pickle.load(ifile)
    print datetime.datetime.now()-t0,' elapsed time.'
    return data

def getCliques(g):
    netscience_graph = g
    t0 = datetime.datetime.now()
    cliques = list(nx.find_cliques(netscience_graph))
    print datetime.datetime.now()-t0,' elapsed time.'
    print (len(cliques))
    print cliques[0]
    
def load_graph():
    t0 = datetime.datetime.now()
    netscience_graph = nx.read_gml('cond-mat-2003.gml')
    print(datetime.datetime.now()-t0,' elapsed time.')
    return (netscience_graph)

if __name__ == '__main__':
    print '-'*80
    if not ('cliques' in globals()):
        if not ('g' in globals()):
            g = load_graph()
        print ()
        getCliques(g)

    cliques  = load_cliques_obj()
    one_to_two_model, two_to_one_intxn_model = pheonix.compress(cliques)

    one_to_two_model = helpers.normalize_distributions(one_to_two_model)
    two_to_one_intxn_model = helpers.normalize_distributions(two_to_one_intxn_model)


    clq_numb_dist = helpers.clique_number_distribution(cliques)
    clqs_x_clqs_dist = helpers.cliques_x_cliques_distribution(cliques)

    clq_numb_dist = helpers.normalize_distribution(clq_numb_dist)
    clqs_x_clqs_dist = helpers.normalize_distributions(clqs_x_clqs_dist)
