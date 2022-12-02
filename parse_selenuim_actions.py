import requests
from bs4 import BeautifulSoup
import lxml
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

url = "https://pskov.zoon.ru/restaurants/type/pitstseriya/"
filename = "data_capture/index.html"
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "TURYSESS=smmpsbl7heub1f4begtog5opgh",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


'''
 {'Название':
  'ссылка':
  'номер телефона':
  'оценка':
 }
'''
def get_phone_from_site(url):
    req = requests.get(url,headers=header)
    soup = BeautifulSoup(req.text,'lxml')
    phones = soup.find_all('span',class_='js-phone phoneView phone-hidden')
    result = []
    for i in phones:
        result.append(i.get('data-number').replace(u'\xa0', u''))
    return result

def get_data_from(url):
    driver = webdriver.Chrome(
        service=BraveService(
            ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
        )
    )
    try:
        driver.get(url)
        time.sleep(2)
        while True:
            find_more_element = driver.find_element(By.CLASS_NAME,"catalog-button-showMore")

            if driver.find_elements(By.CLASS_NAME,"reset-filters-btn"):
                return driver.page_source
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                time.sleep(2)
                if driver.find_element(By.CSS_SELECTOR, ".button-block"):
                    block = driver.find_element(By.CSS_SELECTOR, '.button-block')
                    ActionChains(driver).move_to_element(block).click(block).perform()
                    time.sleep(1)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

data = get_data_from(url)
soup = BeautifulSoup(data,'lxml')
pizzeries_list = soup.find_all('div',class_='minicard-item__info')
result = []
for shop in pizzeries_list:
    try:
        name = shop.find('h2',class_='minicard-item__title').text.strip()
    except:
        stars = "нет названия"
    try:
        link = shop.find('a',class_='title-link').get('href')
    except:
        stars = "нет ссылки"
    try:
        phones = get_phone_from_site(link)
    except:
        stars = "нет номера телефона"
    try:
        stars = shop.find('div',class_='stars-view stars-view-medium').get('title').replace(u'\xa0', u' ').strip()
    except:
        stars = "нет оценок"
    result.append(
        {'Название':name,
        'ссылка':link,
        'номер телефона': ','.join(phones),
        'оценка': stars,
    })
with open('data_capture/pizza.json','w',encoding='utf-16') as jsonfile:
    json.dump(result,jsonfile,indent=4,ensure_ascii=False)



