import telebot
import urllib
import time
import argparse
import string
import json
import requests
import Twitme 




#Telegram

TOKEN = "389091608:AAEQefEq_KSDOzhpeG1Wk4R9dby950BlVeo"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['send_steam'])
def send_welcome(message):
	Twitme.get_all_tweets("steam_games")
	data = Twitme.import_data('steam_games_tweets.csv')
	text = []
	for text in data:
		bot.reply_to(message, text[2])

def listener():
	bot.polling()