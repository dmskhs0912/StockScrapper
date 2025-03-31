import scrap, search
from flask import Flask, render_template, request

RSS_URLS = ['https://www.mk.co.kr/rss/30100041/', 'https://www.hankyung.com/feed/finance', 'https://rss.etoday.co.kr/eto/finance_news.xml']


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
    if request.method == 'GET':
        return render_template('search.html')
    
    elif request.method == 'POST':
        stock_title = request.form.get('stock_title')
        data = search.search(stock_title)
        print(data)
        return render_template('search.html', stock_title=stock_title)

@app.route('/scrap', methods=['GET', 'POST'])
def scrap_page():
    if request.method == 'GET':
        #data = scrap.fetch_headlines()
        return render_template('scrap.html')    
    elif request.method == 'POST':
        scrap_search = request.form.get('scrap_search')
        data = scrap.fetch_multiple_pages_with_keyword(RSS_URLS, scrap_search)
        return render_template('scrap.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)