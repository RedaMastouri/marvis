import os
import smtplib
import imghdr
from email.message import EmailMessage
from secrets import *


contacts = ['azwaw@gmail.com', 'test@example.com']

msg = EmailMessage()
msg['Subject'] = 'tikchbila tiwliwla!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'rmastour@amazon.com'

msg.set_content('This is a plain text email')

msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">Aji, kayn chi man9diw!</h1>
        <h2 style="color:red;">wa khaddouj!</h2>
    </body>
</html>
""", subtype='html')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
