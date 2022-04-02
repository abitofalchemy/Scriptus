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
import logging
from datetime import datetime
import json
from src.ges_utils import (
    prep_graph_for_training,
    list_cached_claims
)
from icdcodex import icd2vec, hierarchy
import src.train_ne_model as getrain
import src.node_embeddings_model_evaluation as eval

### Util Functions
def list_available_graphs(app_configs):
    from src.ges_utils import list_available_graphs

    list_available_graphs(app_configs)
    return 

def list_available_models(app_configs):
    from src.ges_utils import list_available_models
    logging.info("list available models")
    list_available_models(app_configs)
    return  

def initialize_logger(output_dir, logfname, mode):
    """
    @param output_dir:  output directory for log files
    @return:        None
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

def select_graph_train_n2v(conf):
    
    return
    
def get_parser():
    ''' Get Parser
    <Expanded description>
    Args: None

    Return: argparser object to use the arguments passed to this function
    '''
    ### Define set of valid arguments
    parser = argparse.ArgumentParser(description='Graph Embeddings')
    parser.add_argument(
        '-c',
        '--config_file',
        dest='config_file',
        type=str,
        default=None,
        help='config file',
    )
    parser.add_argument('--version', action='version', version=__version__)
    return parser


def main():

    ### Setup Logging
    LOG_DIR='./logs'
    LOG_FNAME=sys.argv[0].split('.')[0]
    LOG_FNAME+='.log'
    # print(LOG_FNAME)
    initialize_logger(LOG_DIR, LOG_FNAME, 'a')

    parser = get_parser()
    args = vars(parser.parse_args())
    
    
    if args['config_file'] is not None and ('.yaml' in args['config_file']):
        # The escaping of "\t" in the config file is necesarry as
        # otherwise Python will try to treat is as the string escape
        # sequence for ASCII Horizontal Tab when it encounters it
        # during json.load
#        config = json.load(open(args['config_file']))
#        print(config)
        import yaml
        with open(args['config_file'], 'r') as file:
            config = yaml.safe_load(file)
        print(config.keys())
    ###
    config['logger'] = logging
    # list_cached_claims(config)
    # list_available_graphs(config)
    # list_available_models(config)
    # prep_graph_for_training(config)         # Builds graph
    # select_graph_train_n2v(config)          # Select a graph
    getrain.model_traing(config)          # Train selected node embeddings
    eval.node_embeddings_evaluation(config)     # Evaluation (intrinsic) node embeddings

    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
      print (str(e))
      traceback.print_exc()
      os._exit(1)
    sys.exit(0)
