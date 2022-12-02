import requests
from bs4 import BeautifulSoup
import lxml
import time
import json
import os
import asyncio
import aiohttp

header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}

books = []

async def get_page_data(session,page):
    url = f"https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0&display=table&page={page}"

    async with session.get(url=url,headers=header) as response:
        resp_text = await response.text()
        soup = BeautifulSoup(resp_text,'lxml')
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
    print(f"page {page} parced.")


async def gather_data():
    async with aiohttp.ClientSession() as session:
        url = "https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0&display=table"
        soup = BeautifulSoup(requests.get(url, headers=header).text, "lxml")
        last_page = int(soup.find_all("div", class_="pagination-number")[-1].text.strip())
        tasks = []
        for i in range(1, last_page + 1):
            task = asyncio.create_task(get_page_data(session,i))
            tasks.append(task)
        await asyncio.gather(*tasks)

def main():
    asyncio.run(gather_data())

if __name__ == "__main__":
    start_time = time.time()
    main()
    finish_time = time.time()-start_time
    print(f"{finish_time} sec.")
