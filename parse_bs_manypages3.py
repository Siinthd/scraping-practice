import requests
from bs4 import BeautifulSoup
import lxml
import time
import json
import os

'''
{
    'name':
    'link':
    'img':f'https://landingfoliocom.imgix.net/{img_link}'
    'PostDate':
    'Favorites':
    'Views':
}
'''



header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}

result = []
def get_data_file():
    offset = 1
    while True:
        url_woffset = f'https://s3.landingfolio.com/inspiration?page={offset}&sortBy=free-first'
        response = requests.get(url=url_woffset,headers=header)
        data = response.json()
        if len(data) > 0:
            for item in data:
                if '_id' in item:
                    views = item.get('analytics').get('views')
                    favorites = item.get('analytics').get('favorites')
                    title = item.get('title')
                    link = item.get('url')
                    postDate = item.get('postDate').split('T')[0]
                    try:
                        images = item.get('screenshots') #list of dicts
                        for i in images:
                            for j,k in i.get('images').items():
                                i.get('images').update({j:f'https://landingfoliocom.imgix.net/{k}'})
                    except:
                        images = []
                    result.append(
                    {
                        'name':title,
                        'link':link,
                        'images':images,
                        'PostDate':postDate,
                        'Favorites':favorites,
                        'Views':views,
                        }
                    )
            print(len(data),'data downloaded')
        else:
            with open('data_capture/landings.json','w',encoding='utf-16') as jsonfile:
                json.dump(result,jsonfile,indent=4)
                break
        offset+=1
        time.sleep(2)
    print('*'*80)
    print(len(result),'data total')

def get_images(file_path):
    src = []
    try:
        with open(file_path,'r', encoding='utf-16') as file:
            src = json.load(file)
            list_size = len(src)
            list_iter = 1
        for item in src:
            name = item.get('name')
            if not os.path.exists(f'data_capture/{name}'):
                os.mkdir(f'data_capture/{name}')
            for i in item.get('images'):
                r = requests.get(url=i.get('images').get('desktop'))
                with open(f'data_capture/{name}/{i.get("title")}.png','wb') as file:
                    file.write(r.content)
            print(f'#{list_iter}({name}) of {list_size} downloaded.')
            list_iter+=1
            time.sleep(2)

    except Exception as ex:
        print(ex)



get_data_file()
get_images('data_capture/landings.json')
