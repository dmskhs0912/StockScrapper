import scrap, search, email_sender, db_manager
from flask import Flask, render_template, request, redirect

RSS_URLS = ['https://www.mk.co.kr/rss/50200011/', 'https://www.hankyung.com/feed/finance', 'https://rss.etoday.co.kr/eto/finance_news.xml']


app = Flask(__name__)
db = db_manager.connect_to_mongodb()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
    if request.method == 'GET':
        return render_template('search.html')
    
    elif request.method == 'POST':
        stock_title = request.form.get('stock_title')
        data, error = search.search_stock(stock_title)
        print(data)
        return render_template('search.html', data=data)

@app.route('/scrap', methods=['GET', 'POST'])
def scrap_page():
    if request.method == 'GET':
        #data = scrap.fetch_headlines()
        data = scrap.fetch_multiple_pages_with_keyword(RSS_URLS, '')
        return render_template('scrap.html', data=data)   
    elif request.method == 'POST':
        scrap_search = request.form.get('scrap_search')
        data = scrap.fetch_multiple_pages_with_keyword(RSS_URLS, scrap_search)
        return render_template('scrap.html', data=data, keyword=scrap_search)

@app.route('/scrap/send-email/<keyword>', methods=['POST'])
def send_email(keyword):
    print(f'키워드 : {keyword}')
    to_email = request.form.get('to_email')
    email_sender.send_news_email(RSS_URLS, keyword, to_email)
    return render_template('send.html', to_email=to_email, keyword=keyword)

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    pass

if __name__ == '__main__':
    app.run(debug=True)
    