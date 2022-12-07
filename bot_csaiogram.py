import requests
from bs4 import BeautifulSoup
import json
import time
import os
from aiogram import Bot,Dispatcher,executor,types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold,hlink

from fake_useragent import UserAgent

ua = UserAgent()


tbot = Bot(token = os.getenv('tgTOKEN'),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(tbot)

def collect():
    result = []
    offset  =0
    batch_size=60
    undone = True
    while undone:
        for item in range(offset,offset+batch_size,60):
            try:
                url = f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=30&isStore=true&limit=60&maxPrice=10000&minPrice=1&offset={offset}&sort=botFirst&type=4&withStack=true'
                response = requests.get(url = url,headers={'user-agent':f'{ua.random}'}).json()
                data = response.get('items')
                if data is None:
                    undone = False
                    break
                for i in data:
                    if i.get('overprice') is not None and  i.get('overprice') < -23:
                        item_full = i.get('fullName')
                        item_price = i.get('price')
                        item_3d = i.get('3d')
                        item_overprice = i.get('overprice')
                        result.append({
                                        "Full name":item_full,
                                        "Price":item_price,
                                        "3D":item_3d,
                                        "Overprice":item_overprice,
                                    })
                offset+=batch_size
                print(f'{offset} items parsed.')
            except Exception as ex:
                offset-=60
    with open('data_capture/cs.json','w',encoding = 'utf-8') as file:
        json.dump(result,file,indent = 4,ensure_ascii = False)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['перчатки','снайперские винтовки','ножи']
    keyb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyb.add(*start_button)
    await message.answer("есть только винтовки",reply_markup = keyb)

@dp.message_handler(Text(equals='снайперские винтовки'))
async def send_data(message: types.Message):
    await message.answer("ждите")
    collect()
    with open('data_capture/cs.json',encoding = 'UTF-8') as file:
       jfile = json.load(file)
    for index,i in enumerate(jfile):
        cards = f"{hlink(i.get('Full name') + ' - ' + str(i.get('Overprice'))+'%', i.get('3D'))}\n {hbold(i.get('Price'))}🔥🔥🔥"
        if index%20 == 0:
            time.sleep(3)
        await message.answer(cards)

if __name__=="__main__":
    executor.start_polling(dp)
