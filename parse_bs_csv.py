import requests
from bs4 import BeautifulSoup
import lxml
import os
import json,csv
urlmain = 'https://shop.casio.ru/catalog/'
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}

req = requests.get(url=urlmain,headers=header)


# if not os.path.exists("data_capture\data"):
#     os.mkdir("data_capture\data")

# with open("data_capture\data\index.html",'w',encoding='utf-8') as file:
#     file.write(req.text)
with open('data_capture/watches.csv','w') as csvfile:
    writer = csv.writer(csvfile,delimiter=';')
    writer.writerow(('Артикул','Цена','ссылка'))
soup = BeautifulSoup(req.text,'lxml')
pagecount = soup.find('div',class_="bx-pagination-container").find_all('a')[-2].text
products=[]
for i in range(1,int(pagecount)+1):
    url = f'https://shop.casio.ru/catalog/?PAGEN_1={i}'
    pagereq = requests.get(url=url,headers=header)
    soup = BeautifulSoup(pagereq.text,'lxml')
    itemlist = soup.find_all('a',class_='product-item__link')
    for item in itemlist:
        product_art=item.find('p',class_='product-item__articul').text.strip()
        product_price=item.find('p',class_='product-item__price').text.strip()
        product_link=item.get('href')

        products.append({
        "Артикул":product_art,
        "Цена":product_price,
        "ссылка":'https://shop.casio.ru/catalog'+product_link,
        })
        with open('data_capture/watches.csv','a') as csvfile:
            writer = csv.writer(csvfile,delimiter=';')
            writer.writerow((product_art,product_price,'https://shop.casio.ru/catalog'+product_link))

with open('data_capture/watches.json','w',encoding='utf-16') as jsonfile:
    json.dump(products,jsonfile,indent=4,ensure_ascii = False)
#?PAGEN_1=2
