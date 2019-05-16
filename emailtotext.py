# Send a text message
import smtplib
from os import environ

def send_simple(number):
    # Primary information
    content = 'There has been an update to MyBackPack!'
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    # Start encryption
    mail.ehlo()
    mail.starttls()
    # Login
    mail.login('email@email.com', environ.get('password'))
    mail.sendmail('email@email.com', (str(number)+'@txt.att.net'), content)
    mail.close()
