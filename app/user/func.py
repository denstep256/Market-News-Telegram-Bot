import requests
import yfinance as yf
import config


def get_currency_rates():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = response.json()
    currencies = {
        'USD': data['Valute']['USD'],
        'EUR': data['Valute']['EUR'],
        'CNY': data['Valute']['CNY']
    }
    return currencies

def get_crypto_data():
    api_key = config.CMC_API
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    parameters = {'symbol': 'BTC,ETH,XRP,BNB,SOL,TON,TRUMP', 'convert': 'USD'}
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    cryptocurrencies = {
        'BTC': data['data']['BTC']['quote']['USD'],
        'ETH': data['data']['ETH']['quote']['USD'],
        'XRP': data['data']['XRP']['quote']['USD'],
        'BNB': data['data']['BNB']['quote']['USD'],
        'SOL': data['data']['SOL']['quote']['USD'],
        'TON': data['data']['TON']['quote']['USD'],
        'TRUMP': data['data']['TRUMP']['quote']['USD']
    }
    return cryptocurrencies

def get_fear_and_greed_index():
    url = 'https://api.alternative.me/fng/'
    response = requests.get(url)
    data = response.json()
    return data['data'][0]

def get_yahoo_data():
    symbols = {'S&P 500': '^GSPC', 'Apple': 'AAPL', 'Tesla': 'TSLA', 'Nvidia': 'NVDA', 'Google': 'GOOGL', 'Amazon': 'AMZN'}
    yahoo_data = {}
    for name, ticker in symbols.items():
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        price = data['Close'].iloc[-1]
        change = (data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1] * 100
        yahoo_data[name] = {'price': price, 'change': change}
    return yahoo_data


def get_moex_data():
    stocks = ['SBER', 'GAZP', 'LKOH', 'YDEX', 'ROSN']
    moex_data = {}

    for stock in stocks:
        url = f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{stock}.json'
        response = requests.get(url).json()
        market_data = response.get('marketdata', {}).get('data', [])
        if market_data:
            price = market_data[0][12] if len(market_data[0]) > 12 else None
            change = market_data[0][13] if len(market_data[0]) > 13 else None
            moex_data[stock] = {'price': price, 'change': change}

    # Добавляем индекс IMOEX
    url_imoex = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/IMOEX.json'
    response_imoex = requests.get(url_imoex).json()
    market_data_imoex = response_imoex.get('marketdata', {}).get('data', [])

    if market_data_imoex:
        price_imoex = market_data_imoex[0][2] if len(market_data_imoex[0]) > 2 else None
        change_imoex = market_data_imoex[0][4] if len(market_data_imoex[0]) > 4 else None
        moex_data['IMOEX'] = {'price': price_imoex, 'change': change_imoex}

    return moex_data

