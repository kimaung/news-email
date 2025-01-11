import requests  
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
  
# API Details  
API_URL = "https://api.currentsapi.services/v1/latest-news"  
API_KEY = "${{ secrets.CURRENTSAPI_KEY }}"  
LANGUAGE = "en"  
  
# Email Details  
SMTP_SERVER = "smtp.mail.yahoo.com"  
SMTP_PORT = 587  
EMAIL_ADDRESS = "${{ secrets.MAIL_USERNAME }}"  
EMAIL_PASSWORD = "${{ secrets.MAIL_PASSWORD }}"  
RECIPIENT_EMAIL = "aessaputra@yahoo.com"  
  
def fetch_news():  
    params = {  
        "language": LANGUAGE,  
        "apiKey": API_KEY  
    }  
    response = requests.get(API_URL, params=params)  
    data = response.json()  
    return data['news']  
  
def send_email(news):  
    msg = MIMEMultipart()  
    msg['From'] = EMAIL_ADDRESS  
    msg['To'] = RECIPIENT_EMAIL  
    msg['Subject'] = "Daily News Update"  
  
    body = "<h1>Daily News Update</h1><ul>"  
    for article in news:  
        body += f"<li><strong>{article['title']}</strong><br>{article['description']}<br><a href='{article['url']}'>Read more</a></li>"  
    body += "</ul>"  
  
    msg.attach(MIMEText(body, 'html'))  
  
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:  
        server.starttls()  
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())  
  
if __name__ == "__main__":  
    news = fetch_news()  
    send_email(news)  
