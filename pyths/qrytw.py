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
import time, tweepy, sys, csv
from LocStrmListener import StdOutListener


def twitter_authentication():
  fileNamePaht = ".env/keys.tsv"
  keys_dict = dict()
  with open(fileNamePaht, 'r') as f:
    inreader = csv.reader(f,delimiter='\t')
    for row in inreader:
      keys_dict[row[0]] = row[1]
    
    return keys_dict

def get_parser():
  parser = argparse.ArgumentParser(description='query twitter and output to file')
  parser.add_argument('query', metavar='QUERY',    help='Quoted query')
  parser.add_argument('-o',    metavar='OUT_FILE', default='/tmp/output', help='Basename output file')
  parser.add_argument('--version', action='version', version=__version__)
  return parser

def main():
  parser = get_parser()
  args = vars(parser.parse_args())

  print args

  ## Read my twitter auth keys and tokens
  auth_keys = twitter_authentication()
  
  CONSUMER_KEY = auth_keys['CONSUMER_KEY']
  CONSUMER_SECRET = auth_keys['CONSUMER_SECRET']
  OAUTH_TOKEN=auth_keys['OAUTH_TOKEN']
  OAUTH_TOKEN_SECRET = auth_keys['OAUTH_TOKEN_SECRET']
  
  
  ## OAuth process, using the keys and tokens
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  
  ## Creation of the actual interface, using authentication
  api = tweepy.API(auth)
  
  trck = [str(args['query'])]

  listen = StdOutListener(api, str(args['o']))
  stream = tweepy.Stream(auth = api.auth, listener = listen)
  
  print "Streaming started..."
  
  try:
    stream.filter(track= trck, async=True)
  except:
    print "error!"
    stream.disconnect()


if __name__ == '__main__':

  main()
  sys.exit(0)

