import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'email@server.com'
EMAIL_PASSWORD = "Password"
RECIPIENT_EMAIL = 'email@email.com'

# Function to create the email content
def create_email(subject, body, attachment_path=None):
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = subject

    # Attach the body with the msg instance
    message.attach(MIMEText(body, 'plain'))

    # Attach the file if specified
    if attachment_path:
        attachment = open(attachment_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        message.attach(part)

    return message

# Function to send the email
def send_email(message):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, message.as_string())
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to generate the daily report
def generate_report():
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"Daily Report - {today}"
    body = "Here is your daily report.\n\nBest regards,\nYour Automation Script"
    #attachment_path = '/path/to/your/report/file.txt'  # Specify the path to your report file if any
    email_content = create_email(subject, body)
    send_email(email_content)

# Schedule the function to run daily
if __name__ == "__main__":
    generate_report()

