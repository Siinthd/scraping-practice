import requests
import lxml
from bs4 import BeautifulSoup
import os
import json
import time

from aiogram import Bot,Dispatcher,executor,types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold,hlink
from fake_useragent import UserAgent

ua = UserAgent()
tbot = Bot(token = os.getenv('tgTOKEN'),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(tbot)


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
    r = s.get('https://hi-tech.mail.ru/ajax/mobile-catalog/', params=params, headers={'user-agent':f'{ua.random}'}).json()
    pages = r.get('Models').get('Pages')
    for i in range(1,pages+1):
        params['page'] = str(i)
        r = s.get('https://hi-tech.mail.ru/ajax/mobile-catalog/', params=params, headers={'user-agent':f'{ua.random}'}).json()
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
