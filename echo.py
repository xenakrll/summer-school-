# -*- coding: UTF-8 -*-

import logging
import telegram
import api
from telegram.error import NetworkError, Unauthorized
from time import sleep


update_id = None

def main():
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('243386141:AAFGPVRHnB83v20MtfSE6fPTtsMOvUSzKqY')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

findtxt = 'Where? (location/address)'
datetxt = 'When? (now/date and time(YY-mm-dd H:M:S))'
# написать oops we didn't find anything
from time import sleep
def echo(bot):
    global update_id
    # Request updates after the last update_id
    while True:
        sleep(0.5)
        print "Qq"
        update = bot.getUpdates(offset=update_id, limit=1, timeout=10)[0]


        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        #if update.message:  # your bot can receive updates without messages
		# Reply to the message
		#bot.sendMessage(chat_id=chat_id, text='Viberi mesto')


        if update.message.text == '/find':
            print "Qq"
            bot.sendMessage(chat_id=chat_id, text=findtxt)
            #update_id = update.update_id + 1

            #update = "get next"

            update = bot.getUpdates(offset=update_id, limit=1, timeout=10)[0]
            chat_id = update.message.chat_id
            update_id = update.update_id + 1

            if update.message.location:
                lat_input = str(update.message.location.latitude)
                longt_input = str(update.message.location.longitude)
                area = api.do_your_worst(lat_input, longt_input).lower()
                for pair in api.read_locales():
                    if pair['name'].lower() == area:
                        id_area = pair['_id']
            else:
                adr = str(update.message.text)
                (lat_input, longt_input) = api.get_coordinates(adr)
                area = api.do_your_worst(lat_input, longt_input).lower()
                for pair in api.read_locales():
                    if pair['name'].lower() == area:
                        id_area = pair['_id']

            bot.sendMessage(chat_id=chat_id, text=datetxt)
            update = bot.getUpdates(offset=update_id, limit=1, timeout=10)[0]
            chat_id = update.message.chat_id
            update_id = update.update_id + 1

            if update.message.text == 'now':
                date_time = str(update.message.date)
                pattern = '%Y-%m-%d %H:%M:%S'
                bgn_input = int(time.mktime(time.strptime(date_time, pattern))) * 1000 - 1800000
                end_input = bgn_input + 7200000

            else:
                date_time = str(update.message.text)
                pattern = '%Y-%m-%d %H:%M:%S'
                bgn_input = int(time.mktime(time.strptime(date_time, pattern))) * 1000 - 1800000
                end_input = bgn_input + 7200000
            output = api.get_list(id_area, bgn_input, end_input)
            bot.sendMessage(chat_id=chat_id, text=output)



'''
                bot.sendMessage(chat_id=chat_id, text=str(update.message.location.latitude))
                bot.sendMessage(chat_id=chat_id, text=str(update.message.location.longitude))
                bot.sendMessage(chat_id=chat_id, text=api.output)'''





if __name__ == '__main__':
    main()
