from get import cbr_data, cripto_data
from pl import get_news,prompt_for_review



import telebot
import datetime
import schedule
import time
import threading

API_TOKEN = '<api_token>'

bot = telebot.TeleBot('6757646836:AAFrG9uM8Vasa8apNS87TjzyGhol6VcbUNU')
today = datetime.date.today()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """Привет, Денис. Изучи список команд:
        /prompt - получить промпт для обзора рынков с данными на сегодня
        /send_review - отправить обзор в канал
        """)

@bot.message_handler(commands=['prompt'])
def send_prompt(message):
    try:
        prompt = prompt_for_review()
        bot.reply_to(message,prompt)
    except:
        bot.reply_to(message,'Не удалось, поробуй еще раз, дружище')   

@bot.message_handler(commands=['send_review'])
def send_message(message): 
    
    send = bot.reply_to(message,'Вставь текст обзора:')

    bot.register_next_step_handler(send,send_review)

def send_review(message):
    channel_id = '@mamkin_bankir'
    #print(message.text())
    send_text(channel_id,message.text)






def send_text(channel_id,text):
    bot.send_message(channel_id, text, parse_mode = 'Markdown',disable_web_page_preview = True)


def send_cdr_data():
    data_cbr = cbr_data()
    data_cripto = cripto_data()
    message = f'''
    *Экономические показатели* \U0001F1F7\U0001F1FA
    *на {today}* 

    \U0001F6D2 Инфляция - {data_cbr[0]}%
    \U0001F4CA Процентная ставка - {data_cbr[1]}%

    _Курсы валют:_
                                        
    \U0001F4B5 Доллар(USD) - {data_cbr[2]}
    \U0001F4B6 Евро(EUR) - {data_cbr[3]}
    \U0001F4B4 Китайский юань(CNY) - {data_cbr[4]}

    _Цены на драгоценные металлы_
    _(рублей за грамм):_

    \U0001F4C0 Золото(Au) - {data_cbr[5]}
    \U0001F4BF Серебро(Ag) - {data_cbr[6]}
    \U0001F4BD Платина(Pt) - {data_cbr[7]}

    _Курс криптовалют в долларах(USD)_

    \U00002705 Bitcoin(BTC) - {data_cripto[0]}
    \U00002705 Ethereum(ETH) - {data_cripto[1]}
    \U00002705 Litecoin(LTC) - {data_cripto[2]}
    \U00002705 Ripple(xrp) - {data_cripto[3]}
    
    '''
    channel_id = '@mamkin_bankir'
    send_text(channel_id,message)

def news_send():
    news = get_news()
    title = news[0]
    annotation = news[1]
    link = news[2]
    magazine = news[3]

    channel_id = '@mamkin_bankir'
    send_news = f'*Обзор новостей на {today}*\n\n'

    for i in range(len(title)):
        text = f'_{magazine[i]}_\n*{title[i]}*\n {annotation[i]}\n [Читать-->]({link[i]})\n\n' 
        send_news = send_news+text
        time.sleep(1)
        
    send_text(channel_id,send_news)
        #bot.send_message(channel_id,send_news,parse_mode = 'Markdown', disable_web_page_preview = True)
        #print('News send')

def thread_info():
    schedule.every().day.at('10:00').do(send_cdr_data)
    schedule.every().day.at('13:00').do(news_send)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target = thread_info, daemon = True).start()


bot.infinity_polling()


#schedule.every(1).minutes.do(send_cdr_data)
#schedule.every().hour.do(job)
#schedule.every().day.at('16:35').do(send_cdr_data)
#schedule.every().day.at('16:39').do(news_send)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
#schedule.every().minute.at(":17").do(job)

#while True:
    #schedule.run_pending()
    #time.sleep(1)


