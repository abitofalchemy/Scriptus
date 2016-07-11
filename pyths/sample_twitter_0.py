# -*- coding: utf-8 -*-

__author__  = 'Sal Aguinaga'
__license__ = "GPL"
__version__ = "0.1.0"
__email__   = "saguinag@nd.edu"

import time, tweepy, sys, csv
from StrmListener import StdOutListener

def twitter_authentication():

  ## authentication
  fileNamePaht = "../.env/keys.tsv"
  keys_dict = dict()
  with open(fileNamePaht, 'r') as f:
    inreader = csv.reader(f,delimiter='\t')
    for row in inreader:
      keys_dict[row[0]] = row[1]

    return keys_dict

def main():

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

  trck = ['Indiana','weather']
  
  listen = StdOutListener(api, 'hw1p3-2')
  stream = tweepy.Stream(auth = api.auth, listener = listen)

  print "Streaming started..."

  try: 
    stream.filter(track= trck, async=True)
  except:
    print "error!"
    stream.disconnect()

if __name__ == '__main__':
    main()
