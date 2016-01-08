__author__ = 'saguinag'+'@'+'nd.edu'
__version__ = "0.1.0"

##
##  hrgm = hyperedge replacement grammars model
##

## TODO: some todo list
#

## VersionLog:
# 0.0.1 Initial commit
#

import argparse,traceback,optparse
import pandas as pd
import os, sys, time
import networkx as nx
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def get_parser():
  parser = argparse.ArgumentParser(description='filename: Descritipn like: Hyperedge Replacement Grammars Model')
    parser.add_argument('graph_name', metavar='GRAPH_NAME', nargs=1, help='the graph name to process')
    #parser.add_argument('--list',  nargs=0, help='unique file names', action=ListSupportedGraphs)
    parser.add_argument('-s','--save',  help='Save to disk with unique names', action='store_true', default=False)
    parser.add_argument('--version', action='version', version=__version__)
    return parser

def main():
  #global options, args
  #g = command_line_runner()
  parser = get_parser()
  args = vars(parser.parse_args())

  print args

if __name__ == '__main__':
    # g = command_line_runner()

    # ## View/Plot the graph to a file
    # fig = plt.figure(figsize=(1.6*6,1*6))
    # ax0 = fig.add_subplot(111)

    # nx.draw_networkx(g[1],ax=ax0)
    # plt_filename="/tmp/outfig"

    # try:
    #   save_plot_figure_2disk(plotname=plt_filename)
    #   print 'Saved plot to: '+plt_filename
    # except Exception, e:
    #   print 'ERROR, UNEXPECTED SAVE PLOT EXCEPTION'
    #   print str(e)
    #   traceback.print_exc()
    #   os._exit(1)
    # sys.exit(0)
    main()
    sys.exit(0)

