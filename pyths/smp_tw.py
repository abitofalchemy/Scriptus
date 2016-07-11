# -*- coding: utf-8 -*-

__author__  = 'Sal Aguinaga'
__license__ = "GPL"
__version__ = "0.1.0"
__email__   = "saguinag@nd.edu"

from tweepy import StreamListener, Stream
from pprint import pprint
import json, time, sys, csv
from HTMLParser import HTMLParser

def twitter_authentication():

  ## authentication
  fileNamePaht = ".env/keys.tsv"
  keys_dict = dict()
  with open(fileNamePaht, 'r') as f:
    inreader = csv.reader(f,delimiter='\t')
    for row in inreader:
      keys_dict[row[0]] = row[1]

    return keys_dict
#
#follow_acc = ['759251'] #cnn id
#track_words = ['New Zealand flag'] # if remove ReTweets, add '-RT' in the word

class Listener(StreamListener):
  def __init__(self, api = None, fprefix = 'streamer'):
    self.api = api or API()
    self.counter = 0
    self.fprefix = fprefix
    self.output  = open(fprefix + '.json', 'a')
  
  def on_status(self, status):
    status = json.loads(HTMLParser().unescape(status))
    if 'indiana' or 'weather' in stats.lower():
        # status.created_at is datetime object and status.text is the tweet's text
        text = '::'.join([str(status.created_at), status.text, status.author.screen_name]) + '\n'
        f.write(text)


if __name__=='__main__':
 
  import tweepy
  auth_keys = twitter_authentication()
  CONSUMER_KEY = auth_keys['CONSUMER_KEY']
  CONSUMER_SECRET = auth_keys['CONSUMER_SECRET']
  OAUTH_TOKEN=auth_keys['OAUTH_TOKEN']
  OAUTH_TOKEN_SECRET = auth_keys['OAUTH_TOKEN_SECRET']
  
  # print len (CONSUMER_KEY), len(CONSUMER_SECRET)
  # print len(OAUTH_TOKEN), len(OAUTH_TOKEN_SECRET)
  
  ## OAuth process, using the keys and tokens
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  
  ## Creation of the actual interface, using authentication
  api    = tweepy.API(auth)
  trck = ['Indiana']
  
  listen = StdOutListener(api, 'hw1_p3')
  stream = tweepy.Stream(auth = api.auth, listener = listen)

  print "Streaming started..."

  try: 
    stream.filter(track= trck)
  except:
    print "error!"
    stream.disconnect()

#  twitterStream = Stream(auth, Listener())
#  twitterStream.filter(track = trck)
