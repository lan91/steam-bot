import tweepy
import urllib
import time
import argparse
import string
import json
import requests
import csv
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener




#Twitter
consumer_key = '9awEDlRvba20bb4zkTskZa2KM'
consumer_secret = 'qHBZMXK7y16UK3OwPhNcWYwbZiwYuUnap40V4EtW9VVJ5xfgiX'
access_token = '407683186-fmYEDzIiavJGkKFQPPmHtpdItna8eNie4iDgeFwT'
access_secret = 'Y9lUgKwc9CrXTGrefk9NalWxMXKET3QjDn0lQ1QEu9yB5'
 
def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[0].id
    i=0
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) < 10:
        print("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[i].id +1
        
        print ("...%s tweets downloaded so far" % (len(alltweets)))
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    
    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass


def import_data(delimited_file):
    """imports the a delimited file and casts the data to a list"""
    
    with open(delimited_file, 'rb') as csvfile:
        all_data = list(csv.reader(csvfile, delimiter=','))
    return all_data
    

def get_basic_statistics(data):
    """
    grabs the values for a specific crime
    *function should be renamed*
    """
    text = []
    for text in data:
        print(text[2])