import requests
import img2pdf
url = 'https://www.recordpower.co.uk/flip/Winter2020/mobile/index.html'
header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }

img_list = []
for i in range(1,49):
    url = f"https://www.recordpower.co.uk/flip/Winter2020/files/thumb/{i}.jpg"
    req = requests.get(url,headers=header)
    response=req.content
    with open(f'data_capture/media/{i}.jpg','wb') as image:
        image.write(response)
        img_list.append(f'data_capture/media/{i}.jpg')

with open('data_capture/result.pdf','wb') as pdffile:
    pdffile.write(img2pdf.convert(img_list))

