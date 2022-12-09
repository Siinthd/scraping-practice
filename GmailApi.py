import smtplib
import os
from email.mime.text import MIMEText
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def send_email(message = 'test'):
    sender = 'turel1405@gmail.com'
    #os.getenv("GMAILEMAIL")
    password = os.getenv("GMAILTOKEN")

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()

    try:
        server.login(sender,password)
        msg = MIMEText(message)
        msg['Subject'] = 'text'
        server.sendmail(sender,sender,msg.as_string())

        return "the message has sent succefully."
    except Exception as ex:
        print(ex)

def driveApi_text():
    try:
        auth = GoogleAuth()
        auth.LocalWebserverAuth()

        drive = GoogleDrive(auth)

        new_file = drive.CreateFile({'title':'file_name.txt'})
        new_file.SetContentString("Hello World")
        new_file.Upload()
        print('file_name.txt','saved succefully')
    except Exception as ex:
        print(ex)

def driveApi_content():
    try:
        auth = GoogleAuth()
        auth.LocalWebserverAuth()

        drive = GoogleDrive(auth)

        for i in os.listdir(dir_path):
            new_file = drive.CreateFile({'title':f'{i}'})
            new_file.SetContentFile(os.path.join(dir_path,i))
            new_file.Upload()
            print(f'{i}','saved succefully')
    except Exception as ex:
        print(ex)

