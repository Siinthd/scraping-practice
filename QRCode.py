import qrcode

def generate_qr(url = 'https:\\www.yandex.ru',name = 'default'):
    qr = qrcode.make(data=url)
    qr.save(stream =f'{name}.png')

