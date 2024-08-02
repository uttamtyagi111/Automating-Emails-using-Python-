import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time

from_addr = 'enquirywishgeekstechservecom@enquirywishgeeks.getgodesk.com'
display_name = 'Wish Geeks Tech Service'
to_addr = 'uttam@wishgeekstechserve.com'

# Email setup
filename = '10.png'
file_path = os.path.join('c:/Users/Wish/Documents/Automation', filename)

# Initialize the counter for total emails sent
total_email_sent = 0

email = 'enquiry@wishgeekstechserve.com'
password = 'Enquiry@2024'

# SMTP server configuration
smtp_server = 'mail.wishgeekstechserve.com'
port = 465  # SSL/TTLS port

try:
    # Establish an SSL connection
    mail = smtplib.SMTP_SSL(smtp_server, port)
    mail.login(email, password)

    msg = MIMEMultipart()
    msg['From'] = f'{display_name} <{from_addr}>'
    msg['To'] = to_addr
    msg['Subject'] = 'Automating the Mails'

    body = 'Hello World'
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(file_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)
    except FileNotFoundError:
        print(f"File {filename} not found at {file_path}")

    try:
        text = msg.as_string()
        mail.sendmail(from_addr, to_addr, text)

        # Increment the total email sent counter
        total_email_sent += 1

        # Log email details
        history_info = f"***** Last Email History *****\n\n" \
                       f"From : {from_addr}\n" \
                       f"Send to : {to_addr}\n" \
                       f"At Time : {time.strftime('%Y-%m-%d %H:%M:%S')}\n" \
                       f"Total Emails Sent : {total_email_sent}\n"

        with open("history.txt", "a") as file:
            file.write(history_info)

        # Print info to console
        info = {
            "Send to": to_addr,
            "From": from_addr,
            "At Time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "Total Emails Sent": total_email_sent
        }
        print(info)

        # Pause before sending next email
        time.sleep(15)
    except smtplib.SMTPDataError as e:
        print(f"SMTPDataError: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    mail.quit()
