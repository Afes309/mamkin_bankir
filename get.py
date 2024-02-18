import requests
from bs4 import BeautifulSoup




# Данные с сайта банка России
def cbr_data():
    url = 'https://cbr.ru/key-indicators/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html5lib')
                    
                        
    # Инфляция и процентная ставка
    key_indicators = soup.find_all('div',class_ = 'value')
    inflation = key_indicators[1].text.split('%')[0]
    the_interest_rate = key_indicators[2].text.split('%')[0]

    #Курсы валют
    exchange_rates = soup.find_all('td',class_ = 'value td-w-4 _bold _end mono-num')
    usd = exchange_rates[1].find_next_sibling('td').text
    eur = exchange_rates[2].find_next_sibling('td').text
    cny = exchange_rates[0].find_next_sibling('td').text

                                                                
    #Драгоценные метеллы

    #золото
    au = exchange_rates[3].find_next_sibling('td').text
    #серебро
    ag = exchange_rates[4].find_next_sibling('td').text
    #платина
    pt = exchange_rates[5].find_next_sibling('td').text

    return inflation,the_interest_rate,usd,eur,cny,au,ag,pt


def cripto_data():
    #url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDC'
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {'ids':'bitcoin,ethereum,litecoin,ripple','vs_currencies':'usd'}
                     
    r = requests.get(url, params = params)
    soup = BeautifulSoup(r.text,'html5lib')
                                  
    btc = r.json()['bitcoin']['usd']
    eth = r.json()['ethereum']['usd']
    ltc = r.json()['litecoin']['usd']
    xrp = r.json()['ripple']['usd']

    return btc,eth,ltc,xrp



    if __name__ == '__main__':
        print(cbr_data())







