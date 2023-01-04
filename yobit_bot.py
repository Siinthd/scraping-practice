import requests

# Пример парсинга криптобиржи

#all tickers
url = 'https://yobit.net/api/3/info'
re = requests.get(url)
with open('data_capture/charts.txt','w') as charts:
    charts.write(re.text)
#concrete tickers coin1_coin2-coin1_coin3
url = 'https://yobit.net/api/3/ticker'+'/doge_usd-decr_btc-geo_btc?ignore_invalid=1'
re = requests.get(url)
with open('data_capture/ticker.txt','w') as charts:
    charts.write(re.text)
#concrete tickers with depth(limit)
url = 'https://yobit.net/api/3/depth'+'/doge_usd?limit=2000&ignore_invalid=1'
re = requests.get(url)
bids = re.json()['doge_usd']['bids']
total = 0
for item in bids:
    price = item[0]
    coin_amount = item[1]

    total+=price*coin_amount
print(total,'$')
#trades
url = 'https://yobit.net/api/3/trades'+'/doge_usd?limit=2000&ignore_invalid=1'
re = requests.get(url)

asks = 0
bids = 0

for item in re.json()['doge_usd']:
    if item['type'] == 'ask':
        asks += item['price']*item['amount']
    else:
        bids += item['price']*item['amount']

print('asks: ',asks ,'bids: ',bids)