import requests    
import smtplib    
from email.mime.text import MIMEText    
from email.mime.multipart import MIMEMultipart    
import logging    
import os    
  
# Konfigurasi logging    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    
  
# Konstanta API dan Email    
API_URL = "https://api.currentsapi.services/v1/latest-news"    
API_KEY = os.getenv('CURRENTSAPI_KEY')    
LANGUAGE = "en"    
SMTP_SERVER = "smtp.gmail.com"    
SMTP_PORT = 465    
EMAIL_ADDRESS = os.getenv('MAIL_USERNAME')    
EMAIL_PASSWORD = os.getenv('MAIL_PASSWORD')    
RECIPIENT_EMAIL = "gbln50hc@anonaddy.me"  
  
def fetch_news():    
    """Fetch the latest news from the API."""  
    params = {    
        "language": LANGUAGE,    
        "apiKey": API_KEY    
    }    
    try:    
        response = requests.get(API_URL, params=params)    
        response.raise_for_status()    
        return response.json().get('news', [])    
    except requests.exceptions.RequestException as e:    
        logging.error(f"Error fetching news: {e}")    
        return []    
  
def create_email_content(news):    
    """Create the HTML content for the email."""  
    articles_html = "".join(create_article_html(article) for article in news)  
    return f"""  
    <!DOCTYPE html>  
    <html>  
    <head>  
        <style>  
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}  
            .container {{ width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}  
            .header {{ background-color: #FF5733; color: #ffffff; padding: 20px; text-align: center; border-top-left-radius: 8px; border-top-right-radius: 8px; }}  
            .header h1 {{ margin: 0; font-size: 24px; }}  
            .content {{ padding: 20px 0; }}  
            .article {{ margin-bottom: 20px; border-bottom: 1px solid #ddd; padding-bottom: 10px; }}  
            .article:last-child {{ border-bottom: none; }}  
            .article h2 {{ margin: 0 0 10px 0; font-size: 18px; color: #333333; }}  
            .article p {{ margin: 0 0 10px 0; color: #666666; }}  
            .article a {{ color: #007BFF; text-decoration: none; }}  
            .article img {{ max-width: 100%; height: auto; border-radius: 5px; margin: 10px 0; }}  
            .footer {{ background-color: #FF5733; color: #ffffff; padding: 10px 0; text-align: center; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; }}  
            .footer p {{ margin: 0; font-size: 12px; }}  
        </style>  
    </head>  
    <body>  
        <div class="container">  
            <div class="header">  
                <h1>Daily News Update</h1>  
            </div>  
            <div class="content">  
                {articles_html}  
            </div>  
            <div class="footer">  
                <p>&copy; 2025 Daily News Update</p>  
            </div>  
        </div>  
    </body>  
    </html>  
    """  
  
def create_article_html(article):    
    """Create HTML for a single article."""  
    image_html = f'<img src="{article["image"]}" alt="{article["title"]}">' if article.get("image") else ''  
    return f"""  
    <div class="article">  
        <h2>{article['title']}</h2>  
        {image_html}  
        <p>{article['description']}</p>  
        <p><a href="{article['url']}">Read more</a></p>  
    </div>  
    """  
  
def send_email(content):    
    """Send the email with the provided content."""  
    msg = MIMEMultipart()    
    msg['From'] = f"Daily News Update <{EMAIL_ADDRESS}>"    
    msg['To'] = RECIPIENT_EMAIL    
    msg['Subject'] = "Daily News Update"    
    msg.attach(MIMEText(content, 'html'))    
  
    try:    
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:    
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)    
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())    
        logging.info("Email sent successfully.")    
    except smtplib.SMTPException as e:    
        logging.error(f"Error sending email: {e}")    
  
if __name__ == "__main__":    
    news = fetch_news()    
    if news:    
        email_content = create_email_content(news)    
        send_email(email_content)    
    else:    
        logging.info("No news to send.")    
