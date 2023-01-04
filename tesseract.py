import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

filename = 'images/phones.png'
img = Image.open(filename)
custom_cfg = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(img,lang='rus',config=custom_cfg)
file = filename.replace('.','/').split('/')[1]
with open(f'data_capture/{file}.txt','w',encoding='Utf-8') as ftext:
    ftext.write(text)