#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет:)\
""")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.sendMessage(chat_id=chat_id, text=message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
