__author__ = 'saguinag'+'@'+'nd.edu'
__version__ = "0.1.0"

##
##  json_dataset_tograph = convert twitter (json format) dataset to a graph object
##  arguments:  input file (json) 
##

## VersionLog:
# 0.0.1 Initial commit
#

import argparse,traceback,optparse
import urllib, json
import sys


def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

def get_parser():
  parser = argparse.ArgumentParser(description='query twitter and output to file')
  # parser.add_argument('jsonfile', metavar='JSONFILE',    help='Quoted query')
  parser.add_argument('--version', action='version', version=__version__)
  return parser

def main():
  parser = get_parser()
  args = vars(parser.parse_args())

  #print args
  #url = "http://apollo.cse.nd.edu/datasets/paris_shooting.txt"
  # url = "http://dsg1.crc.nd.edu/~saguinag/paper_accepted.json"
  # response = urllib.urlopen(url)
  # data = json.loads(response.read())
  # data = response.read()
  # for line in data:
  infile = "paper_accepted.json"
  data = []
  with open(infile) as data_file:
    lines = data_file.readlines()
  print len(lines)
  for l in lines:
    d =  json.dumps(l)
    print type(d)
    # print json_loads_byteified(l)
    break

  # with open(infile) as f:
  #     ldict = json.load(f)
  #     print type(ldict)
  #     # break

if __name__ == '__main__':

  main()
  sys.exit(0)

