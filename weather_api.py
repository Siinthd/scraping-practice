import os
import requests
import time
import json
from datetime import datetime
from aiogram import Bot,Dispatcher,executor,types
from aiogram.dispatcher.filters import Text

tbot = Bot(token=os.getenv('tgTOKEN'))
dp = Dispatcher(tbot)

API_key = os.getenv('openweathermap_token')
state_code = ""
country_code = '643'
limit = 5



@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Узнать погоду']
    keyb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyb.add(*start_button)
    await message.answer("Узнать погоду в Пскове",reply_markup = keyb)

@dp.message_handler(Text(equals='Узнать погоду'))
async def moscow_city(message: types.Message):
    await message.answer("Ждите")
    file = get_weather("Pskov")[0]
    await message.reply(f"***{file.get('Время запроса')}***\n"
                        f"{file.get('Погода')}\n"
                        f"{file.get('Значок погоды')}\n"
                        f"{file.get('Минимальная температура') - 273.13} - "
                        f"{file.get('Максимальная температура')- 273.13}\n")

def get_weather(city_name):
    result = []
    try:
        url_city = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={API_key}'
        city_coords = requests.get(url_city)
        for i in city_coords.json():
            weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={i.get("lat")}&lon={i.get("lon")}&appid={API_key}&lang={"ru"}').json()
            try:
                result.append({
                "Рассвет" : datetime.fromtimestamp(weather.get('sys').get('sunrise')).strftime('%Y-%m-%d %H:%M:%S'),
                "Закат" : datetime.fromtimestamp(weather.get('sys').get('sunset')).strftime('%Y-%m-%d %H:%M:%S'),
                "Время запроса" :datetime.fromtimestamp(weather.get('dt')).strftime('%Y-%m-%d %H:%M:%S'),
                "Давление" : weather.get('main').get('pressure'),
                "Влажность" : weather.get('main').get('humidity'),
                "Максимальная температура" :weather.get('main').get('temp_max'),
                "Минимальная температура" : weather.get('main').get('temp_min'),
                "Ощущается как" : weather.get('main').get('feels_like'),
                "Погода" : weather.get('weather')[0].get('description'),
                "Значок погоды" : f"http://openweathermap.org/img/wn/{weather.get('weather')[0].get('icon')}@2x.png",
                "Направление ветра" : weather.get('wind').get('deg'),
                "Скорость ветра" : weather.get('wind').get('speed'),
                "Часовой пояс" : weather.get('timezone'),
                "Количество облаков" : weather.get('clouds').get('all')
                })
            except Exception as ex:
                print(ex)

    except Exception as ex:
        print(ex)
    return result

if __name__=='__main__':
    # executor.start_polling(dp)
    print(get_weather("Pskov")[0])
