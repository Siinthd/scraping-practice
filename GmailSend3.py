from fileinput import filename
import mimetypes
import smtplib
from tqdm import tqdm
import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os

def send_email(message = 'test'):
    sender = 'turel1405@gmail.com'
    #os.getenv("GMAILEMAIL")
    password = os.getenv("GMAILTOKEN")

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()

    try:
        server.login(sender,password)
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = sender
        msg['Subject'] = ('ВАЖНО!')

        msg.attach(MIMEText('Hi'))

        for file in tqdm(os.listdir("attachment")):
            filename=os.path.basename(file)
            ftype,encoding=mimetypes.guess_type(file)
            print(ftype)
            file_type,subtype = ftype.split("/")

            if file_type == "text":
                with open(f"attachment/{file}") as f:
                    file = MIMEText(f.read())
            elif file_type == "image":
                with open(f"attachment/{file}","rb") as f:
                    file = MIMEImage(f.read(),subtype)
            elif file_type == "audio":
                with open(f"attachment/{file}","rb") as f:
                    file = MIMEAudio(f.read(),subtype)
            elif file_type == "application":
                with open(f"attachment/{file}","rb") as f:
                    file = MIMEApplication(f.read(),subtype)
            else: #universal version
                with open(f"attachment/{file}","rb") as f:
                    file = MIMEBase(f.read(),subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            file.add_header('content-disposition','attachment',filename=filename)
            msg.attach(file)

        server.sendmail(sender,sender,msg.as_string())

        return "the message has sent succefully."
    except Exception as ex:
        print(ex)
send_email()