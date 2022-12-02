import requests
import lxml
from bs4 import BeautifulSoup
import os
import json
import time

from aiogram import Bot,Dispatcher,executor,types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold,hlink

TOKEN = "5503506299:AAFCDcwWPROwFFZM3E_EoS9gJmfyAH_si70"

tbot = Bot(token = TOKEN,parse_mode=types.ParseMode.HTML)
dp = Dispatcher(tbot)

headers = {
    'authority': 'hi-tech.mail.ru',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'VID=1v4_0q1dR2YC00000h1ML4IC:::0-0-0-8425b4e:CAASECg3fvKFFktXwI2Azjs4w_UaYP5NH4c2a6Lr0Z0LiBDfV5SDVawBHSBSDtRpuyu0WljPOg-sqNECyrrIoNsLlbXyuBSAKAuGEc5s7WVXw_G5qo3QFUoo1IWGmUB7-f0kv8NZrJC0cn4NCqe1QTdtxgt6VA; mrcu=06964e84ef0dc6fcf18557f39f12; t=obLD1AAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAB8AA4FxgcA; s=ww=1920|wh=832|octavius=1; OTVET-10838=53; OTVET-10845=7; b=aksBAKA2XMwDJA6oC4hIjt0BBQAAIAAA; c=kCduYwEA8EhjoAUUAAQAvKY4MOwBAAAAAIAA; o=razelim@list.ru:997:IAA=.m; compare=18999200f318a07ad8e1d31d041f2f4c; ph=pp_l=1|pp_t=1669978783012; mtrc=%7B%22mytrackerid%22%3A52850%7D; Mpop=1669978783:01535a5874006f0e1905000017031f051c054f6c5150445e05190401041d43584a525d5054195d5942431b4540:razelim@list.ru:; sdcs=sl:1669978783:Isx1laLoiVCDqDsXvVNbqOoy4mqGhSeJAamoH68Ooxo; s_cp=skipNotificationsTo=1670065191548',
    'dnt': '1',
    'referer': 'https://hi-tech.mail.ru/mobile-catalog/?vendor_id=11589',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'sort': 'popular',
    'sort_order': 'desc',
    'vendor_id': '11589',
    'param5333': '68555',
    'param7220': '101802',
    'param7159': 'param7159',
    'param489': 'param489',
    'param7377': 'param7377',
    'param7202': 'param7202',
    'page': '1',
}

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['телефоны','Пусто']
    keyb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyb.add(*start_button)
    await message.answer("показать телефоны Xiaomi с 128 Гб памяти и дешевле 20к рублей?",reply_markup = keyb)


@dp.message_handler(Text(equals='телефоны'))
async def moscow_city(message: types.Message):
    await message.answer("ждите")
    collect_data()
    with open('data_capture/mobiles.json',encoding = 'UTF-16') as file:
       jfile = json.load(file)
    for i in jfile:
        await message.answer(f"{hlink(i.get('Name'), i.get('link'))}\n {hbold(i.get('average Price'))}🔥🔥🔥")


def collect_data():
    collection = []
    s = requests.Session()
    r = s.get('https://hi-tech.mail.ru/ajax/mobile-catalog/', params=params, headers=headers).json()
    pages = r.get('Models').get('Pages')
    for i in range(1,pages+1):
        params['page'] = str(i)
        r = s.get('https://hi-tech.mail.ru/ajax/mobile-catalog/', params=params, headers=headers).json()
        Models = r.get('Models').get('Listing')
        for smart in Models:
            Name = smart.get('Name')
            try:
                avgPrice = smart.get('Prices').get('avg')
            except:
                avgPrice = 0
            link = 'https://hi-tech.mail.ru/' + smart.get('HiTechUrl')
            if (int(avgPrice) > 0 and int(avgPrice) < 20000):
                collection.append({'Name':Name,'average Price':avgPrice,'link':link})
    with open('data_capture/mobiles.json','w',encoding='utf-16') as file:
        json.dump(collection,file,indent=4,ensure_ascii=False)




def main():
    pass


if __name__ == "__main__":
    executor.start_polling(dp)
