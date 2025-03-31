import scrap
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
        # search.search_by_title(stock_title)이 구현되어있다고 가정. stock_title을 종목명으로 하는 주식 API 이용해서 검색.
        # 반환 데이터 형식은 딕셔너리. {'title': '...', 'price': '...'}
        #search_data = search.search_by_title(stock_title)
        return render_template('search.html', stock_title=stock_title)

@app.route('/scrap', methods=['GET', 'POST'])
def scrap_page():
    if request.method == 'GET':
        #data = scrap.fetch_headlines()
        return render_template('scrap.html')    
    elif request.method == 'POST':
        scrap_search = request.form.get('scrap_search')
        data = []
        for url in RSS_URLS:
            data.append(scrap.fetch_headlines_with_keyword(url, scrap_search))
        return render_template('scrap.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)