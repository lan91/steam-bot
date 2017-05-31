import telebot
import tweepy
import urllib
import time
import argparse
import string
import json
import requests
import re
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
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass


def import_data(delimited_file):
    """imports the a delimited file and casts the data to a list"""
    
    with open(delimited_file, 'r') as csvfile:
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
    
data = import_data('steam_games_tweets.csv')
get_basic_statistics(data)



#Telegram
TOKEN = '389091608:AAEQefEq_KSDOzhpeG1Wk4R9dby950BlVeo'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
	get_all_tweets("steam_games")
	main()