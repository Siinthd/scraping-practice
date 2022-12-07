import smtplib
import os
from email.mime.text import MIMEText


def send_email(message = 'test'):
    sender = 'turel1405@gmail.com'
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



if __name__=="__main__":
    print(send_email('hello'))
