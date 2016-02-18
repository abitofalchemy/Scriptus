# -*- coding: utf-8 -*-

__author__  = 'Sal Aguinaga'
__license__ = "GPL"
__version__ = "0.1.0"
__email__   = "saguinag@nd.edu"

from tweepy import StreamListener, Stream
from pprint import pprint
import json, time, sys, csv
from HTMLParser import HTMLParser

## http://stackoverflow.com/questions/23531608/how-do-i-save-streaming-tweets-in-json-via-tweepy

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
  import json

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
  api = tweepy.API(auth)
  counter =0
  cur = tweepy.Cursor(api.search, \
                      q=('Isomorphism AND Babai OR Laszlo Babai'), \
                      since='2015-10-01', until='2016-02-02').items()
  #cur = tweepy.Cursor(api.search, \
  #        q="Babai AND isomorphism", \
  #        lang="en").items()

  fprefix="outfile.laszlo_babai.json"
  f = open(fprefix, 'a') 
  search_results =[]
  for tweet in cur:
    try:
        print "Tweet created:", tweet.created_at
        print "Tweet:", tweet.text.encode('utf8')
        #twt = json.loads(HTMLParser().unescape(tweet))
        twt = tweet._json 

        f.write(str(twt)+'\n')
        counter += 1

    except IOError:
        time.sleep(60)
        continue

  f.close()
  #print len(search_results)
  #with open(fprefix, 'a') as f:
  #  json.dump(search_results, f)

