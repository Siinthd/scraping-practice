import requests
from bs4 import BeautifulSoup
import lxml
import json,csv

url = 'https://health-diet.ru/table_calorie/'
header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
req = requests.get(url,headers=header).text
soup = BeautifulSoup(req,"lxml")
all_prod_href = soup.find_all(class_="mzr-tc-group-item-href")
cats= {}
for i in all_prod_href:
    cats[i.text] = 'https://health-diet.ru'+i.get("href")

with open("products.json",'w') as file:
    json.dump(cats,file,indent=4,ensure_ascii=False)
#работаем далее с джсоном
with open("products.json") as file:
    all_cats = json.load(file)

itercount = int(len(all_cats))
count = 1
for cat_name,cat_href in all_cats.items():
    for item in [',','-',' ']:
        if item in cat_name:
            cat_name = cat_name.replace(item,'_')
    req = requests.get(cat_href,headers=header).text
    with open(f'data_capture/{count}_{cat_name}.html','w',encoding='utf-8') as file:
        file.write(req)
    soup = BeautifulSoup(req,"lxml")
    table_head = soup.find(class_='mzr-tc-group-table')
    if table_head is not None:
        table_head=table_head.find('tr').find_all('th')
        productname = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats =table_head[3].text
        carbohedrates = table_head[4].text
        with open(f"data_capture/{count}_{cat_name}.csv",'w',encoding='utf-16') as file:
    #шапка
            writer = csv.writer(file,delimiter=';')
            writer.writerow((productname,calories,proteins,fats,carbohedrates))
    #данные о продукте
            product_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
            product_info = []
            for i in product_data:
                productname = i.find_all('td')[0].find('a').text
                calories = i.find_all('td')[1].text
                proteins = i.find_all('td')[2].text
                fats = i.find_all('td')[3].text
                carbohedrates = i.find_all('td')[4].text
                product_info.append(
                    {
                        "title":productname,
                        "calories":calories,
                        "proteins":proteins,
                        "fats":fats,
                        "carbohydrates":carbohedrates
                    }
                )
                writer.writerow((productname,calories,proteins,fats,carbohedrates))
                with open(f"data_capture/{count}_{cat_name}.json",'w',encoding='utf-16') as jsonfile:
                    json.dump(product_info,jsonfile,indent=4,ensure_ascii = False)
    print(f"{cat_name} записан...{itercount-count} осталось.")
    count+=1
print("Готово!")

