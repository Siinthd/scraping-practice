import requests
from bs4 import BeautifulSoup
import lxml,json
urls = 'https://ru.startup.network/startups/'
page = '/page/2/'
header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }


def get_data(url):
    result = []
    for page in range(1,43):
        proj_urls = []
        req = requests.get(url+f'/page/{page}/',headers=header).text
        soup = BeautifulSoup(req,"lxml")
        articles = soup.find_all('a', class_="projects_list_b")
        for i in articles:
            url = i.get('href')
            if '?' not in url:
                proj_urls.append(url)

        for i in proj_urls:
            url_name = i.split('/')[-1]
            req_s = requests.get(i,headers=header).text
            with open(f'data_capture/{url_name}','w',encoding='utf-16') as file:
                file.write(req)
                print(f'data_capture/{url_name} saved.' )
            soup = BeautifulSoup(req_s,"lxml")
            try:
                IDEA = soup.find(attrs= {'itemprop':"description"}).text
            except:
                IDEA = 'NOIDEA'
            try:
                articles_name = soup.find(attrs= {'itemprop':"name"}).text
            except:
                articles_name = "No title"
            try:
                Status = soup.find('div',{"id": "PRESENT_S"}).find(class_='i_d_c').text.strip().strip('\r')
            except:
                Status= "NoName"
            try:
                Product = soup.find('div',{"id": "PRODUCT"}).find(class_='i_d_c').text.strip().strip('\r')
            except:
                Product= "NoName"
            result.append(
                            {
                                "Название стартапа":articles_name,
                                "Ссылка":i,
                                "Идея":IDEA,
                                "Статус":Status,
                                "Решение":Product
                            }
                        )
    with open(f'data_capture/startups.json','w',encoding='utf-16') as jsonfile:
        json.dump(result,jsonfile,indent=4,ensure_ascii = False)

get_data(urls)

