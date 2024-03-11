from playwright.sync_api import sync_playwright
from time import sleep


# Получает новости из дзена(Возвращает следующие списки: новость,краткое содержание, ссылку на новость, источник)
def get_news():
    with sync_playwright() as pw:
        #browser = pw.chromium.launch(headless=False)
        #context = browser.new_context(viewport={"width": 1920, "height": 1080})
        #page = context.new_page()

        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto('https://dzen.ru/news/rubric/business?issue_tld=ru')
        #page.screenshot(path = 'test.png')

        news = page.locator('div[class = "news-top-stories__other"]').all()
        #text = page.locator('div[class = "news-top-stories__other"]' ).text_content()
        #link = page.locator('div[class = "news-top-stories__other"]').get_attribute('href')

        

        title_list = []
        annotation_list = []
        link_list = []
        magazine_list = []

        print('Ok')
        for i in news:
            page_news = context.new_page()

            link_news = i.locator('a').get_attribute('href')
            page_news.goto(link_news)

            magazine = page_news.locator('span[class = "news-story-redesign__source-text"]').first.text_content()
            magazine_link = page_news.locator('h1[class = "news-story-head-redesign__title"]').locator('a').get_attribute('href')

            
            title_list.append(i.locator('span[class = "news-card2-redesign__title"]').text_content())
            annotation_list.append(i.locator('span[class = "news-card2-redesign__annotation"]').text_content())
            link_list.append(magazine_link)
            magazine_list.append(magazine)

            page_news.close()
            print('news_ok')
        
        browser.close()
        print('end')
        return title_list,annotation_list,link_list,magazine_list
        


# Вытаскивает даные индексов из предоставленной страницы(является вспомогательной функцией для работы market_overview)
def get_index(page,index):
    i_name = page.locator('tr[class = "datatable-v2_row__hkEus dynamic-table-v2_row__ILVMx"]').filter(has_text = f'{index}')
    i_meaning = i_name.locator('td').nth(1).locator('span').text_content()
    i_change = i_name.locator('td').nth(5).text_content()
    return index,i_meaning,i_change

# Вытаскивает даные валют из предоставленной страницы(является вспомогательной функцией для работы market_overview)
def get_currencies(page,currency):
    cur = page.locator('tr[class = "datatable-v2_row__hkEus dynamic-table-v2_row__ILVMx"]').filter(has_text = f'{currency}')
    cur_meaning = cur.locator('td').nth(2).locator('span').text_content()
    cur_change = cur.locator('td').nth(7).text_content()
    return currency,cur_meaning,cur_change

# Вытаскивает даные криптовалют из предоставленной страницы(является вспомогательной функцией для работы market_overview)
def get_crypto_c(page,crypto_c):
    crypto = page.locator('tr[class = "row-RdUXZpkv listRow"]').filter(has_text = f"{crypto_c}")
    crypto_meaning = crypto.locator('td').nth(2).text_content()
    crypto_change = crypto.locator('td').nth(3).text_content()
    return crypto_c,crypto_meaning,crypto_change
    
    


# Получает данные индексов рынков и курсы валют
def market_overview():
        
    
    with sync_playwright() as pw:

        browser = pw.chromium.launch(headless = True)
        context = browser.new_context()
        page = browser.new_page()
        page.set_default_timeout(0)

        
        page.goto('https://ru.investing.com/')
        #page.screenshot(path = 'test.png', full_page = True)
        
        # Индексы
        indexs = ['Индекс Мосбиржи','РТС','Dow Jones','Nasdaq']
        indexs_text = ''
        
        for i in indexs:
            index_data = get_index(page,i)
            indexs_text = indexs_text + f'{index_data[0]} {index_data[1]} {index_data[2]} \n'
        
        print('Index end')
        
        # Курсы вылют
        page.goto('https://ru.investing.com/currencies/single-currency-crosses?currency=rub')
        
        currencies = ['USD/RUB','EUR/RUB','CNY/RUB']
        currencies_text = ''

        for i in currencies:
            currencies_data = get_currencies(page,i)
            currencies_text = currencies_text + f'{currencies_data[0]} {currencies_data[1]} {currencies_data[2]} \n'

        print('Currencies end')
        
        # Криптовалюты
        page.goto('https://ru.tradingview.com/markets/cryptocurrencies/prices-all/')
        
        crypto_c = ['BTC','ETH','LTC','XRP']
        crypto_text = ''

        for i in crypto_c:
            crypto_data = get_crypto_c(page,i)
            crypto_text = crypto_text + f'{crypto_data[0]} {crypto_data[1]} {crypto_data[2]} \n'

        print('Crypto end')


   
        browser.close()
        return indexs_text, currencies_text, crypto_text


# Вытаскивает даные по секторам из предоставленной страницы(является вспомогательной функцией для работы sector_info)
def get_sector(page,sector_name):
    
    sector = page.locator('tr[class = "row-RdUXZpkv listRow"]').filter(has_text = f'{sector_name}')
    sector_change = sector.locator('td').nth(3).text_content()
    return sector_name,sector_change


# Получает данные по секторам рынка

def sector_info():

    with sync_playwright() as pw:

        browser = pw.chromium.launch(headless = True)
        context = browser.new_context()
        page = browser.new_page()


        page.goto('https://ru.tradingview.com/markets/stocks-russia/sectorandindustry-sector/')
        page.screenshot(path = 'test.png', full_page = True)

        sectors = ['Коммерческие услуги','Здравоохранение','Промышленное производство','Технологии','Транспорт']
        sectors_text = ''
        
        for i in sectors:
            sectors_data = get_sector(page,i)
            sectors_text = sectors_text + f'{sectors_data[0]} {sectors_data[1]} \n'

        print('Sector end')

        
        browser.close()
        return sectors_text

def prompt_for_review():
    
    s = sector_info()
    m = market_overview()
    prompt_text = f'''Представь что ты профессиональный инвестор.
    Тебе предстоит написать ежедневный обзор рынков.
    Используй следующие данные:
    Индексы:
    {m[0]}
    Динамика по секторам:
    {s}
    Курсы валют:
    {m[1]}
    {m[2]}
    '''

    return prompt_text


if __name__ == '__main__':
    #sector_info()
    #market_overview()
    prompt_for_review()
