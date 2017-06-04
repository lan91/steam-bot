import telebot
import urllib
import time
import argparse
import string
import json
import requests




#Telegram

TOKEN = "389091608:AAEQefEq_KSDOzhpeG1Wk4R9dby950BlVeo"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

def listener():
	bot.polling()