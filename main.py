from pathlib import Path
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request
import json

OWNER = '@MilantievS'
TOKEN_FILE = 'token.txt'
TOKEN = Path(TOKEN_FILE).read_text().strip()
DATA_URL = 'http://resources.finance.ua/ru/public/currency-cash.json'

def start(update, context):
    """Command handler /start"""
    print('Command /start')
    update.message.reply_text(f'Привет, я бот, мой шеф {OWNER}')


def buy_usd(update, context):
    """Message handlers buy dollars"""
    print('Handler buy_usd')
    update.message.bot.send_message(update.message.chat_id, 'Я знаю чего ты хочешь')
    text = urllib.request.urlopen(DATA_URL).read()
    data = json.loads(text)

    sellers = [o for o in data['organizations'] if 'USD' in o['currencies']]
    sellers.sort(key=lambda o: float(o['currencies']['USD']['ask']))
    best = sellers[0]
    update.message.bot.send_message(update.message.chat_id, f' Лучший курс: {best["currencies"]["USD"]["ask"]} \n ' f'Где купить: {best["link"]}')

    import pdb; pdb.set_trace()

def main():
    updater = Updater(token = TOKEN, use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex('Купить доллары'), buy_usd))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


