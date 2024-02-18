from bot import send_cdr_data,news_send

import schedule
import time

def job():

    #schedule.every(10).minutes.do(job)
    #schedule.every().hour.do(job)
    #schedule.every().day.at("10:30").do(job)
    #schedule.every().monday.do(job)
    #schedule.every().wednesday.at("13:15").do(job)
    schedule.every().day.at("15:58").do(news_send)
    #schedule.every().minute.at(":17").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
