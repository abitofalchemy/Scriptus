# -*- coding: utf-8 -*-

__author__  = 'saguinag'
__license__ = "GPL"
__version__ = "0.1.0"
__email__   = "saguinag@nd.edu"
__status__  = "Development"

#Import the necessary methods from tweepy library
from tweepy import StreamListener
from pprint import pprint
import json, time, sys
from HTMLParser import HTMLParser


"""
This work is based on a tutorial:
http://pythoncentral.io/introduction-to-tweepy-twitter-for-python/
http://adilmoujahid.com/posts/2014/07/twitter-analytics/
http://stats.seandolinar.com/collecting-twitter-data-using-a-python-stream-listener/
http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
##
http://stackoverflow.com/questions/21519351/tweepy-tracking-multiple-terms

"""

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
  
  def __init__(self, api = None, fprefix = 'streamer'):
    self.api = api or API()
    self.counter = 0
    self.fprefix = fprefix
    #self.output  = open(fprefix + '.'+ time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
    self.output  = open(fprefix + '.json', 'a')

  def on_data(self, data):
    data = json.loads(HTMLParser().unescape(data))
    #tweet = "%s => %s"%(data['text'].encode('utf-8'), data['place']['name'].encode('utf-8'))
    self.output.write(str(data) + "\n")
    self.counter += 1
    if self.counter > 50:
        self.output.close()
        self.counter = 0
        return False
    return True
#
#  def on_error(self, status):
#    print status
#
#  def on_status(self, status):
#    return
#  def on_data(self, data):
#    data = json.loads(HTMLParser().unescape(data))
#    tweet = data['text']
#    self.output.write(tweet + "\n")
#    #print self.counter, tweet
#    self.counter += 1
#
#    if self.counter >= 50:
#      self.output.close()
#      self.counter = 0
#      return False
#
#
#    elif 'limit' in data:
#            if self.on_limit(json.loads(data)['limit']['track']) is False:
#                return False
#    elif 'warning' in data:
#            warning = json.loads(data)['warnings']
#            print warning['message']
#            return false
#    return

  def on_status(self, status):
    print 'ons',self.counter, status['text']
    self.counter += 1

    if self.counter >= 50:
      self.output.close()
      self.counter = 0
      return False
  
    return

  def on_delete(self, status_id, user_id):
    self.delout.write( str(status_id) + "\n")
    return
    
  def on_limit(self, track):
    sys.stderr.write("!! " + track + "\n")
    return

  def on_error(self, status_code):
    sys.stderr.write('Error: ' + str(status_code) + "\n")
    return False
    
  def on_timeout(self):
    sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
    time.sleep(60)
    return
