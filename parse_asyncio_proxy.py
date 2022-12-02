import requests
from bs4 import BeautifulSoup
import lxml
import json
import time
import asyncio
import aiohttp
proxies = {
    "https":"20.111.54.16:8123"
}
proxies2 = {
    "https":"178.63.237.147:8080"
}
proxiesstr ="https://178.63.237.147:8080"

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest',
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
'''
    {
        fritz_name:
        fritz_work:
        fritz_links:
        fritz_rabotal:  {   name:
                            {
                                    name:link,
                                    name:link,
                                    name:link,
                            }
                        }
    }

'''
nemetc_data = []

async def gather_data():
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        for i in range(0,741,20):
            url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
            task = asyncio.create_task(get_page(session,url))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def get_page(session,page):
    async with session.get(url=page,headers=header) as response:
        resp_text = await response.text()
        soup = BeautifulSoup(resp_text,'lxml')
        fritz_list = soup.find_all('div',class_='col-xs-4 col-sm-3 col-md-2 bt-slide')
        tasks = []
        for i in fritz_list:
            url = url=i.find('a').get('href')
            task = asyncio.create_task(get_page_lvl2(session,url))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def get_page_lvl2(session,page):
    req_lvl2 = requests.get(url=page,headers=header)
    soup_lvl2 = BeautifulSoup(req_lvl2.text,'lxml')
    fritz_block = soup_lvl2.find('div',class_='col-xs-8 col-md-9 bt-biografie-name')
    try:
        fritz_name = fritz_block.find('h3').text.strip()
    except:
        fritz_name = 'Unknown'
    try:
        fritz_work = fritz_block.find('p').text.strip()
    except:
        fritz_work = 'Unknown'
    fritz_links = {}
    try:
        links = soup_lvl2.find_all('a',class_="bt-link-extern")
        for j in links:
            fritz_links[j.text.strip()] = j.get('href')
    except:
        links = []
    try:
        fritz_rab_1 = soup_lvl2.find('div',{"id": "bt-aemter-collapse"})
        fritz_rab_h5 = fritz_rab_1.find_next('h5')
        fritz_rab_li = fritz_rab_1.find('ul')
        rabotal_dict = {}
        while fritz_rab_h5 != None:
            listtt = fritz_rab_li.find_all('li')
            rabotal_dict_lvl2 = {}
            for n in listtt:
                try:
                    rabotal_dict_lvl2[n.text.strip()] = 'https://www.bundestag.de' + n.find('a').get('href')
                except:
                    rabotal_dict_lvl2[n.text.strip()] = 'no link'
                rabotal_dict[fritz_rab_h5.text.strip()] = rabotal_dict_lvl2
                fritz_rab_h5 = fritz_rab_h5.find_next('h5')
                fritz_rab_li = fritz_rab_li.find_next('ul')
    except:
        rabotal_dict= 'None'
        nemetc_data.append({
                    "fritz_name":fritz_name,
                    "fritz_work":fritz_work,
                    "fritz_links":fritz_links,
                    "fritz_rabotal":rabotal_dict,
                    })
    print(f'page {page} parsed.')

def sync():
    page = 1
    for i in range(0,741,20):
        start_time = time.time()
        url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
        r = requests.get(url=url,headers=header)
        soup = BeautifulSoup(r.text,'lxml')
        fritz_list = soup.find_all('div',class_='col-xs-4 col-sm-3 col-md-2 bt-slide')
        page_lvl2 = 1
        for i in fritz_list:
            req_lvl2 = requests.get(url=i.find('a').get('href'),headers=header)
            soup_lvl2 = BeautifulSoup(req_lvl2.text,'lxml')
            fritz_block = soup_lvl2.find('div',class_='col-xs-8 col-md-9 bt-biografie-name')
            try:
                fritz_name = fritz_block.find('h3').text.strip()
            except:
                fritz_name = 'Unknown'
            try:
                fritz_work = fritz_block.find('p').text.strip()
            except:
                fritz_work = 'Unknown'
            fritz_links = {}
            try:
                links = soup_lvl2.find_all('a',class_="bt-link-extern")
                for j in links:
                    fritz_links[j.text.strip()] = j.get('href')
            except:
                continue
            try:
                fritz_rab_1 = soup_lvl2.find('div',{"id": "bt-aemter-collapse"})
                fritz_rab_h5 = fritz_rab_1.find_next('h5')
                fritz_rab_li = fritz_rab_1.find('ul')
                rabotal_dict = {}
                while fritz_rab_h5 != None:
                    listtt = fritz_rab_li.find_all('li')
                    rabotal_dict_lvl2 = {}
                    for n in listtt:
                        try:
                            rabotal_dict_lvl2[n.text.strip()] = 'https://www.bundestag.de' + n.find('a').get('href')
                        except:
                            rabotal_dict_lvl2[n.text.strip()] = 'no link'
                    rabotal_dict[fritz_rab_h5.text.strip()] = rabotal_dict_lvl2
                    fritz_rab_h5 = fritz_rab_h5.find_next('h5')
                    fritz_rab_li = fritz_rab_li.find_next('ul')
            except:
                rabotal_dict= 'None'
            nemetc_data.append({
                        "fritz_name":fritz_name,
                        "fritz_work":fritz_work,
                        "fritz_links":fritz_links,
                        "fritz_rabotal":rabotal_dict,
                        })
        finish_time = time.time()-start_time
        print(f'page {url} parsed - {finish_time} sec.')


def main():
    asyncio.run(gather_data())



if __name__ == '__main__':
    print('sync start')
    start_time = time.time()
    sync()
    sync_time = time.time()-start_time
    print(f"sync - {sync_time} sec.")

    nemetc_data=[]
    print('async start')
    start_time = time.time()
    main()
    async_time = time.time()-start_time
    print(f"async - {async_time} sec.")

    print(f"{sync_time}sec - {async_time} sec.")
    with open('data_capture/nemec.json','w',encoding = 'utf=16') as jsonfile:
        json.dump(nemetc_data,jsonfile,indent=4,ensure_ascii=False)

