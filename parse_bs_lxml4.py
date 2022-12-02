import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
import json
import csv
import os


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
}

url = "https://www.lifetime.plus/api/analysis2"
req = requests.get(url,headers=header)
t_date = datetime.now().strftime('%d-%m-%Y')
with open(f'data_capture\medjson {t_date}.json','w',encoding='utf-16') as jfile:
    json.dump(req.json(),jfile,indent=4,ensure_ascii=False)
data_list = []
categories = req.json()['categories']
with open(f'data_capture\med_parced_json {t_date}.csv','w',encoding='utf-16') as cfile:
    writer = csv.writer(cfile,delimiter='\t')
    writer.writerow(("название","синонимы","описание","время анализа","биоматериалы","Подготовка к анализу","цена"))

with open(f'data_capture\med_parced_json {t_date}.csv','a',encoding='utf-16') as cfile:
    writer = csv.writer(cfile,delimiter='\t')
    for cat in categories:
        cat_name = cat.get('name')
        cat_items = cat.get('items')
        for item in cat_items:
            item_name = item.get('name')
            item_syn = ';'.join(item.get('synonyms')).strip('\n')
            item_price = item.get('price')
            item_decr = item.get('description').strip()
            item_days = '-'.join(str(x) for x in item.get('daysInterval'))
            item_bio = item.get('biomaterial')
            item_prep = item.get('preparationGuide').strip()
            writer.writerow((item_name,item_syn,item_decr,item_days,item_bio,item_prep,item_price))
            data_list.append({
                "название":item_name,
                "синонимы":item_syn,
                "описание":item_decr,
                "время анализа":item_days,
                "биоматериалы":item_bio,
                "Подготовка к анализу":item_prep,
                "цена":item_price
                })

    with open(f'data_capture\med_parced_json {t_date}.json','w',encoding='utf-16') as jfile:
        json.dump(data_list,jfile,indent=4,ensure_ascii=False)




