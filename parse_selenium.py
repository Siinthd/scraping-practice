import requests
from bs4 import BeautifulSoup
import lxml
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType




url = "https://tury.ru/hotel/?cat=1317"
filename = 'data_capture/index.html'
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "accept-encoding": "gzip, deflate, br",
    # "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "cookie": "TURYSESS=smmpsbl7heub1f4begtog5opgh",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}
"""
1
    # hotels_link = []
    # req = requests.get(url=url,headers=header)
    # soup = BeautifulSoup(req.text,"lxml")
    # hotel_url = soup.find_all('div',class_="reviews-travel__item")
    # for i in hotel_url:
    #     hotels_link.append(i.find('a').get('href'))
    # print(hotels_link)
"""


def get_data_from(url):
    hotels_link = []
    driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
    driver.get(url)
    time.sleep(2)
    with open(filename,'w',encoding='utf-8') as file:
        file.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source,"lxml")
    hotel_url = soup.find_all('div',class_="reviews-travel__item")
    for i in hotel_url:
        hotels_link.append(i.find('a').get('href'))
    print(hotels_link)
    driver.close()


get_data_from(url)
