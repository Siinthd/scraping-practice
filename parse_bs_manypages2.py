import requests
import lxml
from bs4 import BeautifulSoup
import json
import csv
import time
import datetime


getcontext().prec = 2
'''
[
    {
        "НАЗВАНИЕ":
        "АВТОР":
        "ИЗД-ВО/СЕРИЯ":
        "ЦЕНА И БОНУСЫ":
        "НАЛИЧИЕ":
        "Cсылка":
    }
]
'''

start_time = time.time()



header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

url = "https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0&display=table"
soup = BeautifulSoup(requests.get(url, headers=header).text, "lxml")


last_page = int(soup.find_all("div", class_="pagination-number")[-1].text.strip())
books = []
count = 0
with open('data_capture/books.csv','w',encoding = 'utf-16') as csvfile:
    writer = csv.writer(csvfile,delimiter='\t')
    writer.writerow(("НАЗВАНИЕ","АВТОР","ИЗД-ВО/СЕРИЯ","ЦЕНА",'СТАРАЯ ЦЕНА',"НАЛИЧИЕ","Cсылка"))

    for i in range(1, last_page + 1):
        try:
            try:
                req = requests.get(
                    f"https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0&display=table&page={i}",
                    headers=header,
                )
            except Exception as exp:
                    if retry:
                        req = requests.get(
                        f"https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0&display=table&page={i}",
                        headers=header,
                        )
        except:
            continue
        soup = BeautifulSoup(req.text,'lxml')
        books_in_page = soup.find('tbody',class_='products-table__body').find_all('tr')
        for book in books_in_page:
            name = book.find('a',class_="book-qtip").text.strip()
            auth =  book.find('td',class_="col-sm-2").find('div',class_="mt3").text.strip()
            publish = book.find('td',class_="products-table__pubhouse col-sm-2").find('div',class_="mt3").text.strip().replace('\n','').replace('            ',' ')
            price = book.find('span',class_="price-val").text.strip()
            try:
                price_old = book.find('span',class_='price-old').text.strip()
            except:
                price_old = price
            amount = book.find('td',class_="product-table__available col-sm-1").text.strip()
            link = "https://www.labirint.ru" + book.find('a',class_="book-qtip").get("href")
            books.append(
                {
                    'НАЗВАНИЕ':name,
                    'АВТОР': auth,
                    'ИЗД-ВО/СЕРИЯ':publish,
                    'ЦЕНА':price,
                    'СТАРАЯ ЦЕНА':price_old,
                    'НАЛИЧИЕ':amount,
                    'ССЫЛКА':link
                }
                )
            writer.writerow((name,auth,publish,price,price_old,amount,link))
            count+=1
        print(f'page {i} saved.')
with open('data_capture/books.json','a',encoding='utf-16') as file:
    json.dump(books,file,indent=4,ensure_ascii=False)
print(f'{count} books saved to books.json. and books.csv')
finish_time = time.time()-start_time
print(f"{finish_time} sec.")


