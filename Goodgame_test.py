import requests
import time
import os
from fake_useragent import UserAgent

ua = UserAgent()


streamer = input("Введи ссылку на плеер стримера,например, https://goodgame.ru/player?15365\n")
streamer = streamer.split('?')[-1]
last_files = []
if not os.path.exists('data_capture'):
    os.mkdir('data_capture')

while True:
    try:
        response = requests.get(f'https://hls.goodgame.ru/hls/{streamer}.m3u8', headers={'user-agent':f'{ua.random}'})
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



