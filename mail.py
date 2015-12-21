import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import configparser
import os

PATH = os.path.dirname(os.path.abspath(__file__))

def send_mail(send_to, subject, text, files=None):
    assert isinstance(send_to, list)

    config = configparser.ConfigParser()
    config.read(os.path.join(PATH, 'config.ini'))

    send_from = config['mail']['from']
    server = config['mail']['smtp']

    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f),
                Name=basename(f)
            ))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
