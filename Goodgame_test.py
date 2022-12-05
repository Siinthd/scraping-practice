import requests
import time
import os
headers = {
    'authority': 'hls.goodgame.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'dnt': '1',
    'origin': 'https://goodgame.ru',
    'referer': 'https://goodgame.ru/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}
streamer = input("Введи ссылку на плеер стримера,например, https://goodgame.ru/player?15365\n")
streamer = streamer.split('?')[-1]
last_files = []
if not os.path.exists('data_capture'):
    os.mkdir('data_capture')

while True:
    try:
        response = requests.get(f'https://hls.goodgame.ru/hls/{streamer}.m3u8', headers=headers)
        queue = []
        for i in response.text.replace(',','').strip().split('\n'):
            if i[0] != '#'and i not in queue:
                queue.append(i)
        EXTTime = response.text.strip().split('\n')[-2].replace(',','')
        time.sleep(float(EXTTime.split(':')[1]))
        for ExtFile in queue:
            if ExtFile not in last_files:
                filets = requests.get('https://hls.goodgame.ru/hls/' + ExtFile, headers=headers)
                with open(f'data_capture/{streamer}.ts','ab') as file:
                    file.write(filets.content)
                    last_files.append(ExtFile)
    except Exception as ex:
        print(ex)
        last_files = []
        queue = []
        continue



