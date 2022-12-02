import requests
from bs4 import BeautifulSoup
import lxml
import os
from datetime import datetime
import csv
import time
requests.packages.urllib3.disable_warnings()
proxies = {
    "https":"20.111.54.16:8123"
}

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest',
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
url_src = 'https://www.bls.gov/regions/midwest/data/averageenergyprices_selectedareas_table.htm'

def curl_gentable(Series_id):
    '''
        burp suite -> copy POST as curl command
        curl -i -s -k -X $'POST' \
            -H $'Host: data.bls.gov' -H $'Content-Length: 310' -H $'Cache-Control: max-age=0' -H $'Sec-Ch-Ua: \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"' -H $'Sec-Ch-Ua-Mobile: ?0' -H $'Sec-Ch-Ua-Platform: \"Windows\"' -H $'Upgrade-Insecure-Requests: 1' -H $'Origin: https://data.bls.gov' -H $'Content-Type: application/x-www-form-urlencoded' -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H $'Sec-Fetch-Site: same-origin' -H $'Sec-Fetch-Mode: navigate' -H $'Sec-Fetch-User: ?1' -H $'Sec-Fetch-Dest: document' -H $'Referer: https://data.bls.gov/timeseries/APU000072610?amp%253bdata_tool=XGtable&output_view=data&include_graphs=true' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' -H $'Connection: close' \
            -b $'_ga=GA1.2.1042388422.1669634882; _gid=GA1.2.560287523.1669634882; nmstat=50565c5a-aad2-0e92-fe38-319853d5b9f5; _ga=GA1.3.1042388422.1669634882; _gid=GA1.3.560287523.1669634882; _gat_GSA_ENOR0=1' \
            --data-binary $'x=38&y=5&request_action=get_data&reformat=true&from_results_page=true&years_option=specific_years&delimiter=comma&output_type=multi&periods_option=all_periods&output_view=data&to_year=2022&from_year=2012&output_format=excelTable&original_output_type=default&annualAveragesRequested=false&series_id=APU000072610' \
            $'https://data.bls.gov/pdq/SurveyOutputServlet'

        https://curlconverter.com/ -> python code
    '''

    headers = {
        'Host': 'data.bls.gov',
        # 'Content-Length': '310',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://data.bls.gov',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': f'https://data.bls.gov/timeseries/{Series_id}?amp%253bdata_tool=XGtable&output_view=data&include_graphs=true',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close',
        # Requests sorts cookies= alphabetically
        # 'Cookie': '_ga=GA1.2.1042388422.1669634882; _gid=GA1.2.560287523.1669634882; nmstat=50565c5a-aad2-0e92-fe38-319853d5b9f5; _ga=GA1.3.1042388422.1669634882; _gid=GA1.3.560287523.1669634882; _gat_GSA_ENOR0=1',
    }

    data = {
        'x': '38',
        'y': '5',
        'request_action': 'get_data',
        'reformat': 'true',
        'from_results_page': 'true',
        'years_option': 'specific_years',
        'delimiter': 'comma',
        'output_type': 'multi',
        'periods_option': 'all_periods',
        'output_view': 'data',
        'to_year': '2022',
        'from_year': '2012',
        'output_format': 'excelTable',
        'original_output_type': 'default',
        'annualAveragesRequested': 'false',
        'series_id': f'{Series_id}',
    }
    if not os.path.exists('data_capture/filesUSA/'):
        os.mkdir('data_capture/filesUSA/')
    response = requests.post('https://data.bls.gov/pdq/SurveyOutputServlet',headers=headers, data=data, verify=False)#''' proxies=proxies,'''
    with open(f'data_capture/filesUSA/{Series_id}.xlsx', 'wb') as file:
        file.write(response.content)


def get_data(url):
    series = []
    current_data = datetime.now().strftime('%d-%m-%Y')
    if os.path.exists('data_capture/source.html'):
        with open('data_capture/source.html') as file:
            source = file.read()
    else:
        r = requests.get(url=url,headers=header)#,proxies = proxies)
        print(r)
        with open('data_capture/source.html','w') as file:
            file.write(r.text)
            source = r.text
    soup = BeautifulSoup(source,'lxml')
    table = soup.find('table',id='ro5xgenergy')
    data_th = soup.find('thead').find_all('tr')[-1].find_all('th')
    head = ['Area']
    for th in data_th:
        head.append(th.text.strip())
    with open(f'data_capture/table_{current_data}.csv','w') as csvfile:
        writer = csv.writer(csvfile,delimiter=';')
        writer.writerow(head)
    body = table.find('tbody').find_all('tr')
    for tr in body:
        area = tr.find('th').text.strip()
        data=[area]
        data_month = tr.find_all('td')
        for td in data_month:
            if td.find('a'):
                data_temp = td.find('a').get('href')
                series_id = data_temp.split('/')[-1].split('?')[0]
                series.append(series_id)
            elif td.find('span'):
                data_temp = td.find('span').text.strip()
            else:
                data_temp = 'None'
            data.append(data_temp)
        with open(f'data_capture/table_{current_data}.csv','a') as csvfile:
            writer = csv.writer(csvfile,delimiter=';')
            writer.writerow(data)
    file = 1
    for _id in series:
        print(f'download file {file} of {len(series)}.')
        curl_gentable(_id)
        time.sleep(3)
        file+=1

get_data(url_src)
