from aiogram import Bot,Dispatcher,executor,types
from aiogram.dispatcher.filters import Text
from parse_aiogram2 import collect_data
from aiofiles import os

tbot = Bot(token=os.getenv('tgTOKEN'))
dp = Dispatcher(tbot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Moscow','Pskov']
    keyb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyb.add(*start_button)
    await message.answer("Выберите город.",reply_markup = keyb)

@dp.message_handler(Text(equals='Moscow'))
async def moscow_city(message: types.Message):
    await message.answer("Москва ждите")
    chat_id = message.chat.id
    await send_data('2398',chat_id)

@dp.message_handler(Text(equals='Pskov'))
async def moscow_city(message: types.Message):
    await message.answer("Псков ждите")
    chat_id = message.chat.id
    await send_data('1963',chat_id)

async def send_data(city_code = '2398',chat_id=''):
    file = await collect_data(city_code=city_code)
    await tbot.send_document(chat_id=chat_id,document = open(file,'rb'))
    await os.remove(file)



if __name__=='__main__':
    executor.start_polling(dp)

