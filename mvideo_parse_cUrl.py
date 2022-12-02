import requests
import lxml
from bs4 import BeautifulSoup
import json

item_prices = {}
item_list = {}
def get_data():
    #code generate from curl converter
    # burp suite -> copy POST as curl command
    #    curl -i -s -k -X $'POST' \
    #        -H $'Host: data.bls.gov' -H $'Content-Length: 310' -H $'Cache-Control: max-age=0' -H $'Sec-Ch-Ua: \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"' -H $'Sec-Ch-Ua-Mobile: ?0' -H $'Sec-Ch-Ua-Platform: \"Windows\"' -H $'Upgrade-Insecure-Requests: 1' -H $'Origin: https://data.bls.gov' -H $'Content-Type: application/x-www-form-urlencoded' -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H $'Sec-Fetch-Site: same-origin' -H $'Sec-Fetch-Mode: navigate' -H $'Sec-Fetch-User: ?1' -H $'Sec-Fetch-Dest: document' -H $'Referer: https://data.bls.gov/timeseries/APU000072610?amp%253bdata_tool=XGtable&output_view=data&include_graphs=true' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' -H $'Connection: close' \
    #        -b $'_ga=GA1.2.1042388422.1669634882; _gid=GA1.2.560287523.1669634882; nmstat=50565c5a-aad2-0e92-fe38-319853d5b9f5; _ga=GA1.3.1042388422.1669634882; _gid=GA1.3.560287523.1669634882; _gat_GSA_ENOR0=1' \
    #        --data-binary $'x=38&y=5&request_action=get_data&reformat=true&from_results_page=true&years_option=specific_years&delimiter=comma&output_type=multi&periods_option=all_periods&output_view=data&to_year=2022&from_year=2012&output_format=excelTable&original_output_type=default&annualAveragesRequested=false&series_id=APU000072610' \
    #        $'https://data.bls.gov/pdq/SurveyOutputServlet'
#
 #       https://curlconverter.com/ -> python code
    cookies = {
        'COMPARISON_INDICATOR': 'false',
        'HINTS_FIO_COOKIE_NAME': '2',
        'MVID_AB_PDP_CHAR': '2',
        'MVID_AB_SERVICES_DESCRIPTION': 'var4',
        'MVID_BLACK_FRIDAY_ENABLED': 'true',
        'MVID_CALC_BONUS_RUBLES_PROFIT': 'false',
        'MVID_CART_AVAILABILITY': 'true',
        'MVID_CART_MULTI_DELETE': 'false',
        'MVID_CATALOG_STATE': '1',
        'MVID_CITY_ID': 'CityR_49',
        'MVID_CREDIT_AVAILABILITY': 'true',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_FILTER_CODES': 'true',
        'MVID_FILTER_TOOLTIP': '1',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_GEOLOCATION_NEEDED': 'true',
        'MVID_GET_LOCATION_BY_DADATA': 'DaData',
        'MVID_GIFT_KIT': 'true',
        'MVID_GLP': 'true',
        'MVID_HANDOVER_SUMMARY': 'true',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_KLADR_ID': '6000000100000',
        'MVID_LAYOUT_TYPE': '1',
        'MVID_LP_SOLD_VARIANTS': '3',
        'MVID_MCLICK': 'true',
        'MVID_MINDBOX_DYNAMICALLY': 'true',
        'MVID_MINI_PDP': 'true',
        'MVID_MOBILE_FILTERS': 'true',
        'MVID_NEW_ACCESSORY': 'true',
        'MVID_NEW_DESKTOP_FILTERS': 'true',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_NEW_MBONUS_BLOCK': 'true',
        'MVID_PROMO_CATALOG_ON': 'true',
        'MVID_REGION_ID': '49',
        'MVID_REGION_SHOP': 'S970',
        'MVID_SERVICES': '111',
        'MVID_SERVICES_MINI_BLOCK': 'var2',
        'MVID_TIMEZONE_OFFSET': '3',
        'MVID_WEBP_ENABLED': 'true',
        'NEED_REQUIRE_APPLY_DISCOUNT': 'true',
        'PRESELECT_COURIER_DELIVERY_FOR_KBT': 'true',
        'PROMOLISTING_WITHOUT_STOCK_AB_TEST': '2',
        'SENTRY_ERRORS_RATE': '0.1',
        'SENTRY_TRANSACTIONS_RATE': '0.5',
        'searchType2': '3',
        'MVID_CRM_ID': '0031805527',
        'MVID_SHOPPING_CART': '091d287a-b72a-4e16-befb-f75da7c991f6',
        'MVID_GUEST_ID': '21729894057',
        'wurfl_device_id': 'generic_web_browser',
        'MVID_NEW_OLD': 'eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9',
        'deviceType': 'desktop',
        '__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VMUmZjIXlzMQ4aZCVbPE0xE0oRITMsPWQZPWFSL1UuFR4mXXkIHzxdEyg8LBkKTSlCXDN4GkRoH2hMYCI0VlN/KyIVfWwqVgsTXS89XztefTBWKhNLKQ8fGjYhC1U4MFhBEQxhQ0d2dy88bCZjSVsbNSQORV0sUD4uXAxxFSd/DipvG382XRw5YxELGX46Y11GRzcVJHt1EmxdFBJCWRxBdG99EU0oP0dWVVY0XS1BfwtePklteC49bA9bOSFUDSAORGkLG0M1aAx7dSd2fiplMzxrI2VQXSVEXFZ9Jx4NaTpcGz8eInx8LjAbRTFfLHxVEQ8mFTYXI3s/L1QQRU8YDQ1fSHY=ilfo9w==',
        '__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VMUmZjIXlzMQ4aZCVbPE0xE0oRITMsPWQZPWFSL1UuFR4mXXkIHzxdEyg8LBkKTSlCXDN4GkRoH2hMYCI0VlN/KyIVfWwqVgsTXS89XztefTBWKhNLKQ8fGjYhC1U4MFhBEQxhQ0d2dy88bCZjSVsbNSQORV0sUD4uXAxxFSd/DipvG382XRw5YxELGX46Y11GRzcVJHt1EmxdFBJCWRxBdG99EU0oP0dWVVY0XS1BfwtePklteC49bA9bOSFUDSAORGkLG0M1aAx7dSd2fiplMzxrI2VQXSVEXFZ9Jx4NaTpcGz8eInx8LjAbRTFfLHxVEQ8mFTYXI3s/L1QQRU8YDQ1fSHY=ilfo9w==',
        'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
        'cfidsgib-w-mvideo': 'oULt6fNkzDlo2ilccRVe/2K3G+1OQw73pyaxvUg8GAS4rfX8YNMiM42qIoCzm3XwOxazPXLZ2jTATo1XsOZulnYelSe3MRCEvyR5eqoyhu444dbre3TNzKyAHg7ZePVqp8UgMtlo5Ox9FXgyLH5+xRs1o3PgQtQwHz3E',
        'cfidsgib-w-mvideo': 'oULt6fNkzDlo2ilccRVe/2K3G+1OQw73pyaxvUg8GAS4rfX8YNMiM42qIoCzm3XwOxazPXLZ2jTATo1XsOZulnYelSe3MRCEvyR5eqoyhu444dbre3TNzKyAHg7ZePVqp8UgMtlo5Ox9FXgyLH5+xRs1o3PgQtQwHz3E',
        'gsscgib-w-mvideo': 'JGl0LB8CXq9T6jztc7FwNof4mjOJ40jiW8P0wVqa8AExX/IXN3uHGsmXNDz4rAxhgqy2uqJJrI/lfOyjWoxZDhe9mtb5jutIs/90ILRqrYIf6qKCyXmLO1QV46MIoKyhYF9TVbYdChYEp0AaYCm7S9oonRxkAIklUv2AiUSE7yIJRBzglAy11KukXo7pbh2J9eF325rWgHPCqubgovpMZIHRhyKsgZSvu2Sx9NHG8vLvPuMTsek9pCAecuj+Mw==',
        'gsscgib-w-mvideo': 'JGl0LB8CXq9T6jztc7FwNof4mjOJ40jiW8P0wVqa8AExX/IXN3uHGsmXNDz4rAxhgqy2uqJJrI/lfOyjWoxZDhe9mtb5jutIs/90ILRqrYIf6qKCyXmLO1QV46MIoKyhYF9TVbYdChYEp0AaYCm7S9oonRxkAIklUv2AiUSE7yIJRBzglAy11KukXo7pbh2J9eF325rWgHPCqubgovpMZIHRhyKsgZSvu2Sx9NHG8vLvPuMTsek9pCAecuj+Mw==',
        'fgsscgib-w-mvideo': 'YJ9m736b8ce82867dbfddfe57bc7375b8d5bb94b',
        'fgsscgib-w-mvideo': 'YJ9m736b8ce82867dbfddfe57bc7375b8d5bb94b',
        'cfidsgib-w-mvideo': '1ncs/sCOU1Q3nW4A59MXzcOsXq2ueNLvfmxccD7eHTHsWElifYg3A6o8BiDxzdqP+tC6zfWcW/EPb1jeZTNX+ZiG6J0tRyFzjI55+7+IQ4LDzmDqSObnCg+QpxGen0yhCm+KkUCBr0AWiei2GQQRlMsl2wJ38bEPtjXM',
        'CACHE_INDICATOR': 'false',
        'MVID_GTM_ENABLED': '011',
        'MVID_OLD_NEW': 'eyJjb21wYXJpc29uIjpmYWxzZSwiZmF2b3JpdGUiOmZhbHNlLCJjYXJ0Ijp0cnVlfQ==',
        '__lhash_': 'c6af659fe322ac2c949e33c3848be42c',
        'MVID_AB_TOP_SERVICES': '2',
        'MVID_GLC': 'true',
        'MVID_IMG_RESIZE': 'true',
        'MVID_INIT_DATA_OFF': 'false',
        'MVID_LP_HANDOVER': '1',
        'flacktory': 'no',
        'JSESSIONID': '7TnfjGspKgnqnS58vJnyYyQ6LDYCfFsZqJQ5S7WWZ3QGnH5JbS4k!394829646',
        'bIPs': '-971835924',
        'MVID_ENVCLOUD': 'prod2',
    }

    headers = {
        'authority': 'www.mvideo.ru',
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=ab47e85c536440d590061ba085560869,sentry-sample_rate=0%2C5',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'COMPARISON_INDICATOR=false; HINTS_FIO_COOKIE_NAME=2; MVID_AB_PDP_CHAR=2; MVID_AB_SERVICES_DESCRIPTION=var4; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CALC_BONUS_RUBLES_PROFIT=false; MVID_CART_AVAILABILITY=true; MVID_CART_MULTI_DELETE=false; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityR_49; MVID_CREDIT_AVAILABILITY=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GET_LOCATION_BY_DADATA=DaData; MVID_GIFT_KIT=true; MVID_GLP=true; MVID_HANDOVER_SUMMARY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=6000000100000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=3; MVID_MCLICK=true; MVID_MINDBOX_DYNAMICALLY=true; MVID_MINI_PDP=true; MVID_MOBILE_FILTERS=true; MVID_NEW_ACCESSORY=true; MVID_NEW_DESKTOP_FILTERS=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=49; MVID_REGION_SHOP=S970; MVID_SERVICES=111; MVID_SERVICES_MINI_BLOCK=var2; MVID_TIMEZONE_OFFSET=3; MVID_WEBP_ENABLED=true; NEED_REQUIRE_APPLY_DISCOUNT=true; PRESELECT_COURIER_DELIVERY_FOR_KBT=true; PROMOLISTING_WITHOUT_STOCK_AB_TEST=2; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; searchType2=3; MVID_CRM_ID=0031805527; MVID_SHOPPING_CART=091d287a-b72a-4e16-befb-f75da7c991f6; MVID_GUEST_ID=21729894057; wurfl_device_id=generic_web_browser; MVID_NEW_OLD=eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9; deviceType=desktop; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VMUmZjIXlzMQ4aZCVbPE0xE0oRITMsPWQZPWFSL1UuFR4mXXkIHzxdEyg8LBkKTSlCXDN4GkRoH2hMYCI0VlN/KyIVfWwqVgsTXS89XztefTBWKhNLKQ8fGjYhC1U4MFhBEQxhQ0d2dy88bCZjSVsbNSQORV0sUD4uXAxxFSd/DipvG382XRw5YxELGX46Y11GRzcVJHt1EmxdFBJCWRxBdG99EU0oP0dWVVY0XS1BfwtePklteC49bA9bOSFUDSAORGkLG0M1aAx7dSd2fiplMzxrI2VQXSVEXFZ9Jx4NaTpcGz8eInx8LjAbRTFfLHxVEQ8mFTYXI3s/L1QQRU8YDQ1fSHY=ilfo9w==; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VMUmZjIXlzMQ4aZCVbPE0xE0oRITMsPWQZPWFSL1UuFR4mXXkIHzxdEyg8LBkKTSlCXDN4GkRoH2hMYCI0VlN/KyIVfWwqVgsTXS89XztefTBWKhNLKQ8fGjYhC1U4MFhBEQxhQ0d2dy88bCZjSVsbNSQORV0sUD4uXAxxFSd/DipvG382XRw5YxELGX46Y11GRzcVJHt1EmxdFBJCWRxBdG99EU0oP0dWVVY0XS1BfwtePklteC49bA9bOSFUDSAORGkLG0M1aAx7dSd2fiplMzxrI2VQXSVEXFZ9Jx4NaTpcGz8eInx8LjAbRTFfLHxVEQ8mFTYXI3s/L1QQRU8YDQ1fSHY=ilfo9w==; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; cfidsgib-w-mvideo=oULt6fNkzDlo2ilccRVe/2K3G+1OQw73pyaxvUg8GAS4rfX8YNMiM42qIoCzm3XwOxazPXLZ2jTATo1XsOZulnYelSe3MRCEvyR5eqoyhu444dbre3TNzKyAHg7ZePVqp8UgMtlo5Ox9FXgyLH5+xRs1o3PgQtQwHz3E; cfidsgib-w-mvideo=oULt6fNkzDlo2ilccRVe/2K3G+1OQw73pyaxvUg8GAS4rfX8YNMiM42qIoCzm3XwOxazPXLZ2jTATo1XsOZulnYelSe3MRCEvyR5eqoyhu444dbre3TNzKyAHg7ZePVqp8UgMtlo5Ox9FXgyLH5+xRs1o3PgQtQwHz3E; gsscgib-w-mvideo=JGl0LB8CXq9T6jztc7FwNof4mjOJ40jiW8P0wVqa8AExX/IXN3uHGsmXNDz4rAxhgqy2uqJJrI/lfOyjWoxZDhe9mtb5jutIs/90ILRqrYIf6qKCyXmLO1QV46MIoKyhYF9TVbYdChYEp0AaYCm7S9oonRxkAIklUv2AiUSE7yIJRBzglAy11KukXo7pbh2J9eF325rWgHPCqubgovpMZIHRhyKsgZSvu2Sx9NHG8vLvPuMTsek9pCAecuj+Mw==; gsscgib-w-mvideo=JGl0LB8CXq9T6jztc7FwNof4mjOJ40jiW8P0wVqa8AExX/IXN3uHGsmXNDz4rAxhgqy2uqJJrI/lfOyjWoxZDhe9mtb5jutIs/90ILRqrYIf6qKCyXmLO1QV46MIoKyhYF9TVbYdChYEp0AaYCm7S9oonRxkAIklUv2AiUSE7yIJRBzglAy11KukXo7pbh2J9eF325rWgHPCqubgovpMZIHRhyKsgZSvu2Sx9NHG8vLvPuMTsek9pCAecuj+Mw==; fgsscgib-w-mvideo=YJ9m736b8ce82867dbfddfe57bc7375b8d5bb94b; fgsscgib-w-mvideo=YJ9m736b8ce82867dbfddfe57bc7375b8d5bb94b; cfidsgib-w-mvideo=1ncs/sCOU1Q3nW4A59MXzcOsXq2ueNLvfmxccD7eHTHsWElifYg3A6o8BiDxzdqP+tC6zfWcW/EPb1jeZTNX+ZiG6J0tRyFzjI55+7+IQ4LDzmDqSObnCg+QpxGen0yhCm+KkUCBr0AWiei2GQQRlMsl2wJ38bEPtjXM; CACHE_INDICATOR=false; MVID_GTM_ENABLED=011; MVID_OLD_NEW=eyJjb21wYXJpc29uIjpmYWxzZSwiZmF2b3JpdGUiOmZhbHNlLCJjYXJ0Ijp0cnVlfQ==; __lhash_=c6af659fe322ac2c949e33c3848be42c; MVID_AB_TOP_SERVICES=2; MVID_GLC=true; MVID_IMG_RESIZE=true; MVID_INIT_DATA_OFF=false; MVID_LP_HANDOVER=1; flacktory=no; JSESSIONID=7TnfjGspKgnqnS58vJnyYyQ6LDYCfFsZqJQ5S7WWZ3QGnH5JbS4k!394829646; bIPs=-971835924; MVID_ENVCLOUD=prod2',
        'dnt': '1',
        'referer': 'https://www.mvideo.ru/holodilniki-i-morozilniki-2687/holodilniki-i-morozilnye-kamery-159?from=homepage',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': 'ab47e85c536440d590061ba085560869-92a0a9e3b936651e-1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-set-application-id': '0f5f3808-5fdd-4916-adea-1357972c7508',
    }

    params = {
        'categoryId': '159',
        'offset': '0',
        'limit': '24',
        'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
        'doTranslit': 'true',
    }

    response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies, headers=headers).json()
    with open('data_capture/get_listing_mvideo.json','w',encoding='Utf-16') as jsonfile:
        json.dump(response,jsonfile,indent =4,ensure_ascii=False)
    products = response.get('body').get('products')
    get_list(products,headers,cookies)
    get_prices(products,headers,cookies)

def get_prices(product_id,headers,cookies):
    params = {
                'productIds':','.join(product_id),
                'addBonusRubles': 'true',
                'isPromoApplied': 'true',
             }

    response = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies, headers=headers).json()
    with open('data_capture/prices_mvideo.json','w',encoding='Utf-16') as jsonfile:
        json.dump(response,jsonfile,indent =4,ensure_ascii=False)
    material_prices = response.get('body').get('materialPrices')
    for item in material_prices:
        item_id = item.get('productId')
        base_price = item.get('price').get('basePrice')
        sale_price = item.get('price').get('salePrice')
        item_bonus = item.get('bonusRubles').get('total')
        item_prices[item_id]={
                                "base_price":base_price,
                                "sale_price":sale_price,
                                "item_bonus":item_bonus
                            }


def get_list(prod_ids,headers,cookies):
    json_data = {
        'productIds': prod_ids,
        'mediaTypes': [
            'images',
        ],
        'category': True,
        'status': True,
        'brand': True,
        'propertyTypes': [
            'KEY',
        ],
        'propertiesConfig': {
            'propertiesPortionSize': 5,
        },
        'multioffer': False,
    }

    response = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers, json=json_data).json()
    with open('data_capture/get_listmvideo.json','w',encoding='Utf-16') as jsonfile:
        json.dump(response,jsonfile,indent =4,ensure_ascii=False)
    lists = response.get('body').get('products')
    for item in lists:
        item_id = item.get('productId')
        item_name = item.get('name')
        item_list[item_id] = item_name



get_data()
#result = {}
#1 вариант
# for i,j in zip(item_prices,item_list):
#     result[item_list[i]] = item_prices[i]
# with open('data_capture/resultmvideo.json','w',encoding='Utf-16') as jsonfile:
#     json.dump(result,jsonfile,indent =4,ensure_ascii=False)
#2й
with open('data_capture/get_listmvideo.json', encoding="utf-16") as file:
    product_data = json.load(file)

product_data = product_data.get('body').get('products')
for i in product_data:
    prod_id = i.get('productId')
    if prod_id in item_prices:
        price = item_prices[prod_id]
    i['base_price'] = price.get('base_price')
    i['sale_price'] = price.get('sale_price')
    i['item_bonus'] = price.get('item_bonus')
print(product_data)
with open('data_capture/resultmvideo.json','w',encoding='Utf-16') as jsonfile:
    json.dump(product_data,jsonfile,indent =4,ensure_ascii=False)
