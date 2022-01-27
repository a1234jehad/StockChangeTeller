import datetime
import requests
import os


######################################VARS####################################


my_stock_api_key = os.environ['my_stock_api_key']
my_news_api_key = os.environ['my_news_api_key']
my_email = os.environ['my_email']
token = os.environ['token_tele']
my_user_id = os.environ['my_user_id']
chat_id = os.environ['chat_id']



######################################Time check####################################
today = datetime.datetime.now()
yestarday = (int(today.weekday()) - 1) % 7

para = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': "",
    'apikey': my_stock_api_key,
}
if yestarday not in (5, 6):
    stocks = [{'Stock_Name': 'Tesla', 'Stock_ticker': 'TSLA'}, {'Stock_Name': 'palantir', 'Stock_ticker': 'PLTR'},
              {'Stock_Name': 'National Presto Industries', 'Stock_ticker': 'NPK'}]

    for x in stocks:
        STOCK = x['Stock_ticker']
        COMPANY_NAME = x['Stock_Name']
        print(STOCK)
        para['symbol'] = STOCK
        response = requests.get(url='https://www.alphavantage.co/query', params=para)
        response.raise_for_status()
        data = response.json()
        data = data["Time Series (Daily)"]
        yestarday_index = list(data)[0]
        byestarday_index = list(data)[1]
        price_yesterday = float(data[yestarday_index]['4. close'])
        price_bfyesterday = float(data[byestarday_index]['4. close'])
        diff = price_yesterday - price_bfyesterday
        percentage = round((float((diff / price_bfyesterday) * 100)), 2)

        #############NEWS API########
        paras = {
            'q': COMPANY_NAME,
            'from': yestarday_index,
            'sortBy': 'popularity',
            'apiKey': my_news_api_key,
        }

        news_response = requests.get(url='https://newsapi.org/v2/everything', params=paras)
        news_response.raise_for_status()
        news_data = news_response.json()
        Top3news = f"The 3 top articles about {COMPANY_NAME}:\n "
        no_articles = False

        for x in range(3):
            Top3news += f"\nArticle{x + 1}:\n "
            try:
                Top3news += news_data['articles'][x]['title'] + '\n '
                Top3news += news_data['articles'][x]['url'] + '\n'

            except(IndexError):
                no_articles = True
                break

        # SENDING MSGS
        emoji = ""

        if no_articles:
            Top3news="There are no news related to the stock 🥺"

        if abs(percentage) < 4:
            continue

        if percentage > 0:
            emoji = f"📈 +{percentage}"

        else:
            emoji = f"📉 {percentage}"


        #send_telegram_msg
        link = 'https://api.telegram.org/bot' + token
        get_update = link + '/getUpdates'
        message = ""
        send_message = f"{link}/sendMessage?chat_id={str(chat_id)}&text=Stock {STOCK} is {emoji} \n\n{Top3news}"
        print(send_message)

        rss = requests.get(url=send_message)
        rss.raise_for_status()
        send_message = f"{link}/sendMessage?chat_id={str(chat_id)}&text=\n\n---------------------------------------\n\n"
        rss = requests.get(url=send_message)



print("FINISHED")

