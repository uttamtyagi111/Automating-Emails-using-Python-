import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time
import json

# Load sender information from JSON file
with open('send_from.json') as f:
    send_from = json.load(f)

# Load recipient emails from JSON file
with open('sendTo.json') as f:
    emailsTo = json.load(f)

# Extract sender details
from_addr = send_from['email']
display_name = send_from['display_name']
password = send_from['password']

# Extract recipient email addresses
to_addr = [entry['Email'] for entry in emailsTo]

# Email setup
import os

# Email setup
filename = '10.png'
file_path = os.path.join('.', filename)  # '.' refers to the current directory


# Initialize the counter for total emails sent
total_email_sent = 0

mail = smtplib.SMTP("mail.wishgeekstechserve.com", 587)
mail.ehlo()
mail.starttls()
mail.login(from_addr, password)

# HTML content with Content-ID reference for the image
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }}
        .container {{
            width: 80%;
            margin: auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
        }}
        .header {{
            background-color: #f4f4f4;
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }}
        .content {{
            padding: 20px;
        }}
        .footer {{
            background-color: #f4f4f4;
            padding: 10px;
            text-align: center;
            border-top: 1px solid #ddd;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Welcome to WishGeeks Tech Services</h2>
        </div>
        <div class="content">
            <p>Hello,</p>
            <p>We are excited to have you onboard. Below is a picture to welcome you:</p>
            <img src="cid:image1" alt="Welcome Image">
            <p>Feel free to reach out to us for any queries.</p>
        </div>
        <div class="footer">
            <p>Best Regards,<br>WishGeeks Tech Services</p>
        </div>
    </div>
</body>
</html>
"""

for recipient in to_addr:
    msg = MIMEMultipart()
    msg['From'] = f'{display_name} <{from_addr}>'
    msg['To'] = recipient
    msg['Subject'] = 'Automating the Mails'  # Add your email title here

    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # Add the image as an attachment
    try:
        with open(file_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            part.add_header('Content-ID', '<image1>')  # Content-ID for referencing in HTML
            part.add_header('X-Attachment-Id', 'image1')
            msg.attach(part)
    except FileNotFoundError:
        print(f"File {filename} not found at {file_path}")

    try:
        text = msg.as_string()
        mail.sendmail(from_addr, recipient, text)

        # Increment the total email sent counter
        total_email_sent += 1

        # Log email details
        history_info = f"***** Last Email History *****\n\n" \
                       f"From : {from_addr}\n" \
                       f"Send to : {recipient}\n" \
                       f"At Time : {time.strftime('%Y-%m-%d %H:%M:%S')}\n" \
                       f"Total Emails Sent : {total_email_sent}\n"

        with open("history.txt", "a") as file:
            file.write(history_info)

        # Print info to console
        info = {
            "Send to": recipient,
            "From": from_addr,
            "At Time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "Total Emails Sent": total_email_sent
        }
        print(info)

        # Pause before sending next email
        time.sleep(15)
    except smtplib.SMTPDataError as e:
        print(f"SMTPDataError: {e}")

mail.quit()
