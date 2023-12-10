__author__ = 'saguinaga'+'@'+'deloitte.com'
__version__ = "0.1.0"

##
##  Describe me
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
import logging
from datetime import datetime


import matplotlib.pyplot as plt
plt.style.use('ggplot')

### Util Functions
def initialize_logger(output_dir, logfname, mode):
    """
    @param output_dir: output directory for log files
    @param logfname:   logs filename
    @param mode:       'a' for append or 'w' to overwrite to log
    @return:           None
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ### create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    ### create error file handler and set level to error
    if not os.path.exists(output_dir):
      from pathlib import Path
      Path(output_dir).mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(
            os.path.join(output_dir, 'error.log'),
        mode, encoding=None, delay='true'
    )
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    ### logfname = log_
    ### set the log file name
    handler = logging.FileHandler(
            os.path.join(
                    output_dir,
                    logfname),
            mode)  # all.log

    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.info('\n\n{} : {}'.format(datetime.now(),sys.argv[0]))
    logging.info('logs >> %s ', (os.path.join(
                    output_dir,
                    logfname)))
    return

def get_parser():
    ''' Get Parser
    <Expanded description>
    Args: None

    Return: argparser object to use the arguments passed to this function
    '''
    ### Define set of valid arguments
    parser = argparse.ArgumentParser(description='filename: Description like: Hyperedge Replacement Grammars Model')
    parser.add_argument('graph_name', metavar='GRAPH_NAME', nargs=1, help='the graph name to process')
    #parser.add_argument('--list',  nargs=0, help='unique file names', action=ListSupportedGraphs)
    parser.add_argument('-s','--save',  help='Save to disk with unique names', action='store_true', default=False)
    parser.add_argument('--version', action='version', version=__version__)
    return parser


def main():
    ### Main Description

    ### Setup Logging
    LOG_DIR='./logs'
    LOG_FNAME=sys.argv[0].split('.')[0]
    LOG_FNAME+='.log'
    print(LOG_FNAME)
    initialize_logger(LOG_DIR, LOG_FNAME, 'a')

    parser = get_parser()
    args = vars(parser.parse_args())
    logging.info(f"{args}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
      print (str(e))
      traceback.print_exc()
      os._exit(1)
    sys.exit(0)
