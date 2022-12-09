import time
from datetime import datetime
import requests
from pyfiglet import Figlet
import folium

def block_IP_thru_hosts():
    start_time = datetime(datetime.now().year,datetime.now().month,datetime.now().day,11,21)
    finish_time = datetime(datetime.now().year,datetime.now().month,datetime.now().day,11,23)

    hosts = r'C:/Windows/System32/drivers/etc/hosts'
    redirect_url = '127.0.0.1'

    blocked_sites = ['www.pikabu.ru','vk.com']

    while True:
        if start_time < datetime.now()<finish_time:
            with open(hosts,'r+') as host:
                scr = host.read()
                for site in blocked_sites:
                    if site in scr:
                        pass
                    else:
                        host.write(f'{redirect_url} {site}\n')
        else:
            with open(hosts,'r+') as host:
                scr = host.readlines()
                host.seek(0)

                for line in scr:
                    if not any(site in line for site in blocked_sites):
                        host.write(line)
                host.truncate()

def find_over_IP(ip = '127.0.0.1'):
    try:
        preview_text = Figlet(font='slant')
        print(preview_text.renderText('Hello World'))
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        data = {
                  "Zip":response.get("zip"),
                  "lat":response.get("lat"),
                  "lon":response.get("lon"),
                  "country":response.get("country"),
                  "city":response.get("city"),
                  "isp":response.get("isp"),
                }
        for i,j in data.items():
            print(f'[{i}] - {j}')
        area = folium.Map(location = [response.get("lat"),response.get("lon")])
        area.save(f'{ip} - {response.get("city")}.html')
    except requests.exceptions.ConnectionError:
        print('Проверь соединение')
