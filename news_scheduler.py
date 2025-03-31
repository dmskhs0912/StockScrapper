import schedule
import time
from email_sender import send_news_email

schedule.every().day.at("09:00").do(send_news_email)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
