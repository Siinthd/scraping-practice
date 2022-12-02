import requests
import lxml
from bs4 import BeautifulSoup
import json
import datetime

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
}

def get_data():
    url='https://roscarservis.ru/catalog/legkovye/?set_filter=Y&sort[recommendations]=asc&PAGEN_1'
    req = requests.get(url,headers=header)
    pages = req.json()['pagesCount']
    data_list = []
    for i in range(1,pages):
        url_s=f'https://roscarservis.ru/catalog/legkovye/?set_filter=Y&sort[recommendations]=asc&PAGEN_1={i}'
        req_s = requests.get(url_s,headers=header)
        data=req_s.json()
        items=data["items"]
        possible_stores = ['discountStores','externalStores','commonStores']
        stores = []
        for item in items:
            total_count=0
            item_name = item["name"]
            item_price = item["price"]
            item_img = 'https://roscarservis.ru'+item["imgSrc"]
            item_url = 'https://roscarservis.ru'+item["url"]
            for ps in possible_stores:
                if ps in item:
                    if item[ps] is None or len(item[ps]) < 1:
                        continue
                    else:
                        for store in item[ps]:
                            store_name = store["STORE_NAME"]
                            store_price = store["PRICE"]
                            store_count = store["AMOUNT"]
                            total_count+=int(store_count)
                            stores.append({
                            'store_name':store_name,
                            'store_price':store_price,
                            'total_amount':total_count
                            })
            data_list.append({
            "item_name":item_name,
            "item_price":item_price,
            "item_img":item_img,
            "item_url":item_url,
            "stores":stores})
        current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        print(f'{current_time} data_{i} saved.')
    with open(f'data_capture/data.json','a',encoding='utf-16') as file:
        json.dump(data_list,file,indent=4,ensure_ascii=False)


get_data()
