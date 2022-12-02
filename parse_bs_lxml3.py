import requests
from bs4 import BeautifulSoup
import lxml
import json
proxies = {
    "http":"45.131.4.210"
}
header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

host = 'https://www.skiddle.com'
links_list = []
fest_data = []
for i in range(0,144,24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=May"
    req = requests.get(url,headers=header,proxies=proxies)
    json_data=json.loads(req.text)
    html_resp = json_data['html']
    soup = BeautifulSoup(html_resp,'lxml')
    links = soup.find_all('a',class_='card-details-link')

    for i in links:
        link = i.get('href')
        link = host + link
        links_list.append(link)
for i in links_list:
    req = requests.get(i,headers=header,proxies=proxies)
    soup = BeautifulSoup(req.text,'lxml')
    fest_block = soup.find('div',class_='MuiBox-root')
    fest_name = fest_block.find('h1').text.strip()
    try:
        fest_date = fest_block.find('div',class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol')
    except:
        fest_date = "no date"
    try:
        fest_place = fest_date.findNext('div',class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol')
    except:
        fest_place = "no place"
    try:
        fest_price = fest_place.findNext('div',class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol').text
    except:
        fest_price = 'no price.'
    if fest_price == fest_date.text:
        fest_price='No price'
    fest_data.append({
        "fest_name":fest_name,
        "fest_date":fest_date.text,
        "fest_price":fest_price,
        "link":i
    })

with open('data_capture/fests.json','w',encoding='utf-16') as jsonfile:
    json.dump(fest_data,jsonfile,indent=4,ensure_ascii = False)
