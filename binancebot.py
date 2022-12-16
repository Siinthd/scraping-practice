from KEYS import API_KEY,API_SECRET
import time
from urllib.parse import urlencode
import hmac
import hashlib
import requests
#workin with yobit's API
def get_info():
    values = dict()
    values['method'] = 'getInfo'
    values['nonce'] = str(int(time.time()))

    body = urlencode(values).encode('Utf-8')
    sign = hmac.new(API_SECRET.encode('Utf-8'),body,hashlib.sha512).hexdigest()
    header = {
                'key':API_KEY,
                'sign':sign
             }
    response = requests.post(url='https://yobit.net/tapi/',headers= header,data=values)
    print(response.json())

def get_depo_address():
    values = dict()
    values['method'] = 'GetDepositAddress'
    values['coinName'] = 'btc'
    values['need_new'] = 0
    values['nonce'] = str(int(time.time()))

    body = urlencode(values).encode('Utf-8')
    sign = hmac.new(API_SECRET.encode('Utf-8'),body,hashlib.sha512).hexdigest()
    header = {
                'key':API_KEY,
                'sign':sign
            }
    response = requests.post(url='https://yobit.net/tapi/',headers= header,data=values)
    print(response.json())
get_depo_address()
