import requests  
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
import logging  
import os  
  
# Konfigurasi logging  
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  
  
# API Details  
API_URL = "https://api.currentsapi.services/v1/latest-news"  
API_KEY = os.getenv('CURRENTSAPI_KEY')  
LANGUAGE = "en"  
  
# Email Details  
SMTP_SERVER = "smtp.mail.yahoo.com"  
SMTP_PORT = 587  
EMAIL_ADDRESS = os.getenv('MAIL_USERNAME')  
EMAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  
RECIPIENT_EMAIL = "aessaputra@yahoo.com"  
  
def fetch_news():  
    params = {  
        "language": LANGUAGE,  
        "apiKey": API_KEY  
    }  
    try:  
        response = requests.get(API_URL, params=params)  
        response.raise_for_status()  # Raise an error for bad responses  
        data = response.json()  
        if 'news' in data:  
            return data['news']  
        else:  
            logging.error(f"API response does not contain 'news' key: {data}")  
            return []  
    except requests.exceptions.RequestException as e:  
        logging.error(f"Error fetching news: {e}")  
        return []  
  
def send_email(news):  
    if not news:  
        logging.info("No news to send.")  
        return  
  
    msg = MIMEMultipart()  
    msg['From'] = EMAIL_ADDRESS  
    msg['To'] = RECIPIENT_EMAIL  
    msg['Subject'] = "Daily News Update"  
  
    body = "<h1>Daily News Update</h1><ul>"  
    for article in news:  
        body += f"<li><strong>{article['title']}</strong><br>{article['description']}<br><a href='{article['url']}'>Read more</a></li>"  
    body += "</ul>"  
  
    msg.attach(MIMEText(body, 'html'))  
  
    try:  
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:  
            server.starttls()  
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())  
        logging.info("Email sent successfully.")  
    except smtplib.SMTPException as e:  
        logging.error(f"Error sending email: {e}")  
  
if __name__ == "__main__":  
    news = fetch_news()  
    send_email(news)  
