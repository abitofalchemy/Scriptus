# -*- coding: utf-8 -*-

__author__  = 'saguinag'
__license__ = "GPL"
__version__ = "0.1.0"
__email__   = "saguinag@nd.edu"
__status__  = "Development"

#Import the necessary methods from tweepy library
import tweepy as twpy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pprint import pprint
import json, time, sys
from HTMLParser import HTMLParser

APP_KEY = CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = access_token = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = access_token_secret = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'


## OAuth process, using the keys and tokens
#auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(access_token, access_token_secret)
# 

"""
This work is based on a tutorial:
http://pythoncentral.io/introduction-to-tweepy-twitter-for-python/
http://adilmoujahid.com/posts/2014/07/twitter-analytics/
http://stats.seandolinar.com/collecting-twitter-data-using-a-python-stream-listener/
http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
"""

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
  
  def __init__(self, fprefix = 'streamer'):
    self.counter = 0
    self.fprefix = fprefix
    self.output  = open(fprefix + '.'+ '.json', 'a')

  def on_data(self, status):
    data = json.loads(HTMLParser().unescape(status))
    tweet = data['text']
      #if 'weather' or 'indiana' in tweet.lower():
    print tweet
    self.output.write(tweet + "\n")
    self.counter += 1

    if self.counter > 50:
      self.output.close()
      self.counter = 0
      return False
  

  def on_error(self, status):
    print status

  def on_status(self, status):
    #self.output.write(status + "\n")
    self.counter += 1
    print "on_status\n"
    


#def data_crawler_collect_tweets_by_keywords():


#This handles Twitter authetification and the connection to Twitter Streaming API
auth = twpy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(access_token, access_token_secret)


## Creation of the actual interface, using authentication
api = twpy.API(auth)

l = StdOutListener('hw1_')
strm = Stream(auth, l)
try:
  strm.filter(track=['indiana'])
except:
  print "error!"
  strm.disconnect()
