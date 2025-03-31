import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from scrap import fetch_headlines_with_keyword

load_dotenv()

# 네이버 SMTP 설정
SEND_EMAIL = os.getenv("SECRET_ID")
SEND_PWD = os.getenv("SECRET_PASS")
RECV_EMAIL = "sju07032@naver.com"

SMTP_NAME = "smtp.naver.com"
SMTP_PORT = 587

def send_news_email():
    keyword = "삼성"
    news_data = fetch_headlines_with_keyword(keyword)
    
    if not any(news_data):
        text = f"'{keyword}' 키워드로 검색된 뉴스가 없습니다."
    else:
        text = f"'{keyword}' 관련 뉴스 헤드라인:\n\n"
        for i, news_list in enumerate(news_data):
            text += f"📌 RSS 사이트 {i+1}:\n"
            for news in news_list:
                text += f"- {news['title']}\n  {news['link']}\n\n"

    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = f"'{keyword}' 뉴스 헤드라인"
    msg['From'] = SEND_EMAIL
    msg['To'] = RECV_EMAIL

    s = smtplib.SMTP(SMTP_NAME, SMTP_PORT)
    s.starttls()
    s.login(SEND_EMAIL, SEND_PWD)
    s.sendmail(SEND_EMAIL, RECV_EMAIL, msg.as_string())
    s.quit()
