import telebot
import http_parser as parser
#from telebot import apihelper

TOKEN='6886199674:AAEMkmg63p6XtKTg4_omTCW7O_qaOxigXE4'
MAX_NEWS_COUNT = 7

bot = telebot.TeleBot(TOKEN)
news_parser = parser.News()

def news_sender(chat_id: int, news_index: int):
    if news_index >= 0 and news_index < MAX_NEWS_COUNT:
        news = news_parser.get_news(news_index=news_index)
        result = f'Новость № {news_index+1} ({news["date_time"]}):'
        result+=f'\n{news["head"]}'
        result+=f'\n\n{news["body"]}'
        bot.send_message(chat_id, f'{result}')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = ''
    if message.chat.first_name is not None:
        name += message.chat.first_name
    if message.chat.last_name is not None:
        name += ' ' + message.chat.last_name
    bot.send_message(message.chat.id, f'Привет, {name.strip()}!\nХочешь посмотреть новости о погоде?\n(/help - помощь)')

@bot.message_handler(commands=['help'])
def send_help(message):
    result = '/start - приветствие\n/help - список команд\n/about - описание бота\n'\
    + '/news n - показать n-ю новость (n от 1 до 7)\n'\
    + '/news all - показать все новости'
    bot.send_message(message.chat.id, f'Список команд:\n{result}')

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, 'Бот по запросу выводит новости о погоде с сайта https://www.gismeteo.ru\n по ее номеру от 1 до 7, либо сразу все.')

@bot.message_handler(commands=['news'])
def send_news(message):
    parameter = message.text.split(' ')
    if len(parameter)>1:
        parameter = parameter[1]
    if parameter == 'all':
        for news_index in range(MAX_NEWS_COUNT):
            news_sender(message.chat.id, news_index=news_index)
    else:
        try:
            news_index = int(parameter)-1
            if news_index >= 0 and news_index < MAX_NEWS_COUNT:
                news_sender(message.chat.id, news_index=news_index)
            else:
                send_help(message)
        except:
            send_help(message)

@bot.message_handler(content_types=['text'])
def reverse_text(message):
    send_help(message=message)

bot.polling()

