import telebot
import urllib
import time
import datetime
import argparse
import string
import json
import requests
import Twitme
import logging




#Telegram
logging.basicConfig()
logger = logging.getLogger(__name__)

TOKEN = "389091608:AAEQefEq_KSDOzhpeG1Wk4R9dby950BlVeo"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['send_steam'])
def send_welcome(message):
	Twitme.get_all_tweets("steam_games")
	data = Twitme.import_data('steam_games_tweets.csv')
	text = []
	for text in data:
		bot.reply_to(message, text[2])

@bot.message_handler(commands=['echo'])
def send_mad(message):
	pause = 1
    	cadena = str(message.from_user.id) + ',' + message.from_user.username + '\n'
    	infile = open('users_list.txt', 'r')
    	for line in infile:
    		if (line == cadena):
    			pause = 0
    			pass
    	infile.close()
    	if pause:
    		outfile = open('users_list.txt', 'a')
    		outfile.write(cadena)
    		outfile.close()

	bot.send_message(message.from_user.id, 'Dood')
	time.sleep(1)

@bot.message_handler(commands=['future'])
def send_mess(message):
	mess = message.text.split(" ")
	timact=datetime.datetime.now()
	timyact=time.mktime(datetime.datetime.strptime(str(timact[0:-6]), "%Y-%m-%d %H:%M:%S").timetuple())
	timy=time.mktime(datetime.datetime.strptime(mess[2], "%d/%m/%Y").timetuple())
	print(timyact)
	print(timy)
	if(len(mess)<3):
		bot.send_message(message.from_user.id, 'El comando es /future usuario fecha texto')
	else:	
		infile = open('users_list.txt', 'r')
		for line in infile:
			aux = line.split(",")
			if (aux[1][:-1] == mess[1]):
				userin=int(aux[0])
				if(timyact>=timy):
					bot.send_message(userin,mess[3])	
					pass		
		infile.close()
		



def listener():
	try:
		bot.polling(none_stop=True)
	except Exception as e:
		logger.error(e)
		time.sleep(15)