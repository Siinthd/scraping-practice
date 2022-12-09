from string import digits,ascii_letters,punctuation
import itertools
import win32com.client as client
import time
from datetime import datetime
def brute(from_ = 5,to_=5):
    count = 0
    start = datetime.now()
    possible_symbols = ascii_letters
    for pass_lenght in range(from_,to_+1):
        for password in itertools.product(possible_symbols,repeat=pass_lenght):
            password = "".join(password)
            opened_doc = client.Dispatch("Excel.Application")
            count+=1
            time.sleep(0.1)
            try:
                print(password)
                opened_doc.workbooks.Open(r'C:\Users\DevSiinthd\mu_code\scraping-practice\test\Test.xlsx',False,True,None,password)
                print(datetime.now()-start)
                return password
            except Exception as ex:
                print(f'wrong password - {password}')
                pass