import requests
import asyncio
import lxml
import time
import json
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink, hbold

ua = UserAgent()
url = "https://www.securitylab.ru/news/"

tbot = Bot(token=os.getenv("tgTOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(tbot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_button = ["Свежие новости", "Последние пять новостей"]
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyb.add(*start_button)
    await message.answer("Узнать новости", reply_markup=keyb)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_all_news(message: types.Message):
    print("запрос всех новостей...")
    if os.path.exists("data_capture/news.json"):
        with open("data_capture/news.json", encoding="UTF-8") as file:
            news = json.load(file)
    else:
        news = update_news()
    for i, j in sorted(news.items()):
        nnews = (
            f"<b>{datetime.fromtimestamp(j['article_date_from_epoch'])}</b>\n"
            f"<u>{j['article_title']}</u>\n"
            f"<code>{j['article_desc']}</code>\n"
            f"{j['article_link']}\n"
        )
        await message.answer(nnews)


@dp.message_handler(Text(equals="Последние пять новостей"))
async def get_last_news(message: types.Message):
    print("запрос последних 5ти новостей...")
    if os.path.exists("data_capture/news.json"):
        with open("data_capture/news.json", encoding="UTF-8") as file:
            news = json.load(file)
    else:
        news = update_news()
    for i, j in sorted(news.items())[:5]:
        nnews = (
            f"<b>{datetime.fromtimestamp(j['article_date_from_epoch'])}</b>\n"
            f"<u>{j['article_title']}</u>\n"
            f"<code>{j['article_desc']}</code>\n"
            f"{j['article_link']}\n"
        )
        await message.answer(nnews)


async def refresh():
    while True:
        new = update_news()
        if len(new) > 0:
            print("refresh new news.")
            for i, j in sorted(new.items())[:2]:
                nnews = (
                    f"<b>{datetime.fromtimestamp(j['article_date_from_epoch'])}</b>\n"
                    f"<u>{j['article_title']}</u>\n"
                    f"<code>{j['article_desc']}</code>\n"
                    f"{j['article_link']}\n"
                )
                #userid get from @userinfobot
            await tbot.send_message('userid',nnews, disable_notification=True)
        else:
            print("no new news.")
        await asyncio.sleep(10)


def collect_data():
    news_dict = {}
    response = requests.get(url=url, headers={"user-agent": f"{ua.random}"})
    soup = BeautifulSoup(response.text, "lxml")
    news_cards = soup.find_all("a", class_="article-card")
    for i in news_cards:
        article_title = i.find("h2", class_="article-card-title").text
        article_desc = i.find("p").text.strip()
        article_link = "https://www.securitylab.ru" + i.get("href")
        article_date = time.mktime(
            datetime.strptime(
                datetime.strftime(
                    datetime.fromisoformat(i.find("time").get("datetime")),
                    "%Y-%m-%d %H:%M:%S",
                ),
                "%Y-%m-%d %H:%M:%S",
            ).timetuple()
        )
        news_dict[i.get("href").replace(".", "/").split("/")[-2]] = {
            "article_title": article_title,
            "article_desc": article_desc,
            "article_link": article_link,
            "article_date_from_epoch": article_date,
        }
    with open("data_capture/news.json", "w", encoding="UTF-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def update_news():
    if os.path.exists("data_capture/news.json"):
        with open("data_capture/news.json", encoding="UTF-8") as file:
            news = json.load(file)
    else:
        news = {}
    fresh_news = {}
    response = requests.get(url=url, headers={"user-agent": f"{ua.random}"})
    soup = BeautifulSoup(response.text, "lxml")
    news_cards = soup.find_all("a", class_="article-card")
    for i in news_cards:
        if i.get("href").replace(".", "/").split("/")[-2] in news:
            continue
        else:
            article_title = i.find("h2", class_="article-card-title").text
            article_desc = i.find("p").text.strip()
            article_link = "https://www.securitylab.ru" + i.get("href")
            article_date = time.mktime(
                datetime.strptime(
                    datetime.strftime(
                        datetime.fromisoformat(i.find("time").get("datetime")),
                        "%Y-%m-%d %H:%M:%S",
                    ),
                    "%Y-%m-%d %H:%M:%S",
                ).timetuple()
            )
            news[i.get("href").replace(".", "/").split("/")[-2]] = {
                "article_title": article_title,
                "article_desc": article_desc,
                "article_link": article_link,
                "article_date_from_epoch": article_date,
            }
            fresh_news[i.get("href").replace(".", "/").split("/")[-2]] = {
                "article_title": article_title,
                "article_desc": article_desc,
                "article_link": article_link,
                "article_date_from_epoch": article_date,
            }
    with open("data_capture/news.json", "w", encoding="UTF-8") as file:
        json.dump(news, file, indent=4, ensure_ascii=False)
    return fresh_news


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(refresh())
    executor.start_polling(dp)
