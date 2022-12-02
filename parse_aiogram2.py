import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import lxml
import time
import csv
import aiohttp
import asyncio
import aiogram
import aiofiles
from aiocsv import AsyncWriter
header = {
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "DNT": "1",
    "Origin": "https://magnit.ru",
    "Referer": "https://magnit.ru/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

url = "https://magnit.ru/promo/"


async def collect_data(city_code="2398"):
    start_time = time.time()
    c_time = datetime.datetime.now().strftime("%d-%m-%Y")
    goods = []
    ua = UserAgent()
    cookie = {#"PHPSESSID": "f78f2kglq9rqb311q02vmmcokf",
    "mg_geo_id": f"{city_code}"}

    req = requests.get(url, headers=header, cookies=cookie)
    soup = BeautifulSoup(req.text, "lxml")
    city = soup.find(
        "a", class_="header__contacts-link header__contacts-link_city"
    ).text.strip()
    print(f'Начинается загрузка данных для города {city}')
    page = 0
    total_goodies = 0
    with open(f'data_capture/{city}.csv','w') as csvfile:
        writer = csv.writer(csvfile,delimiter=';')
        writer.writerow(('Название','Новая цена','Старая цена','скидка','Время акции'))
        time.sleep(1.5)
    broken_pages = []
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                page += 1
                #data get from cUrl
                data = {
                    "page": f"{page}",
                }
                response = await session.post(url, cookies=cookie, headers=header, data=data)
                if response.status != 200:
                    broken_pages.append(str(page))
                if await response.text() == "":
                    break
                soup = BeautifulSoup(await response.text(), "lxml")
                cards = soup.find_all("a", class_="card-sale card-sale_catalogue")
                for card in cards:
                    card_title = card.find("div", class_="card-sale__title").text
                    try:
                        discount_type = (
                            card.find("div", class_="card-sale__type").find("span").get("class")
                        )
                        if "mextra" in discount_type[1]:
                            discount = card.find(
                                "div", class_="label label_sm label_mextra card-sale__discount"
                            ).text
                        elif "family" in discount_type[1]:
                            discount = card.find(
                                "div", class_="label label_sm label_family card-sale__discount"
                            ).text
                        else:
                            discount = card.find(
                                "div", class_="label label_sm label_magnit card-sale__discount"
                            ).text
                    except:
                        discount = "No discount"
                        continue
                    if discount not in "No discount":
                        card_price_old = f"{card.find('div',class_='label__price label__price_old').find('span',class_='label__price-integer').text.strip()}.{card.find('div',class_='label__price label__price_old').find('span',class_='label__price-decimal').text.strip()}"
                        card_price_new = f"{card.find('div',class_='label__price label__price_new').find('span',class_='label__price-integer').text.strip()}.{card.find('div',class_='label__price label__price_old').find('span',class_='label__price-decimal').text.strip()}"
                        card_sale_date = card.find('div',class_='card-sale__date').text.strip().replace('\n',' ')
                        goods.append([card_title,card_price_new,card_price_old,discount.replace('\u2212','-'),card_sale_date])
                print(f'[{city}]: page {page} parsed.')
                time.sleep(3)
        except Exception as ex:
            print(ex)
            broken_pages.append(str(page))
            continue
    async with aiofiles.open(f'data_capture/{city}.csv','a') as csvfile:
        writer = AsyncWriter(csvfile,delimiter=';')
        await writer.writerows(goods)
    print(f'[{city}]: {len(broken_pages)} пропущено.',','.join(broken_pages))
    finish_time = time.time()-start_time
    print(f"[{city}]: {finish_time} секунд потрачено из них {finish_time - page*3} на парсинг.")
    return f'data_capture/{city}.csv'


async def main():
    await collect_data("2398")


if __name__ == "__main__":
    asyncio.run(main())
