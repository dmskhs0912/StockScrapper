import scrap, search, email_sender, db_manager, search_details
from flask import Flask, render_template, request, redirect, send_file, session

RSS_URLS = ['https://www.mk.co.kr/rss/50200011/', 'https://www.hankyung.com/feed/finance', 'https://rss.etoday.co.kr/eto/finance_news.xml']


app = Flask(__name__)
app.secret_key = 'my_secret_key'
db = db_manager.connect_to_mongodb()

@app.route('/')
def index():
    return render_template('index.html', username=session.get('username'))

@app.route('/search', methods=['GET', 'POST'])
def search_page():
    if request.method == 'GET':
        return render_template('search.html')
    
    elif request.method == 'POST':
        stock_title = request.form.get('stock_title')
        username = session.get('username')
        data = search.print_st(stock_title)
        return render_template('search.html', data=data, username=username)

@app.route('/search/detail',methods=['POST'])
def detail_view():
    stock_code = request.form.get('code')
    stocks = search_details.search_stock(stock_code).get('stocks')
    return render_template('search_details.html', stocks=stocks)


@app.route('/scrap', methods=['GET', 'POST'])
def scrap_page():
    if request.method == 'GET':
        #data = scrap.fetch_headlines()
        data = scrap.fetch_multiple_pages_with_keyword(RSS_URLS, '')
        return render_template('scrap.html', data=data)   
    elif request.method == 'POST':
        scrap_search = request.form.get('scrap_search')
        data = scrap.fetch_multiple_pages_with_keyword(RSS_URLS, scrap_search)
        excel_path = scrap.save_news_to_excel(data, scrap_search)
        return render_template('scrap.html', data=data, keyword=scrap_search, excel_path=excel_path)

@app.route('/scrap/send-email/<keyword>', methods=['POST'])
def send_email(keyword):
    print(f'키워드 : {keyword}')
    to_email = request.form.get('to_email')
    email_sender.send_news_email(RSS_URLS, keyword, to_email)
    return render_template('send.html', to_email=to_email, keyword=keyword)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if db.users.find_one({'username': username, 'password': password}):
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='아이디 또는 비밀번호가 틀립니다.')
        

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')

        if db.users.find_one({'username': username}):
            return render_template('register.html', error='아이디가 이미 사용 중입니다.')
        else:
            db_manager.add_user(db, username, password, name, email)
            return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/profile/<username>')
def profile(username):
    if username != session.get('username'):
        return redirect('/')
    
    user_data = db_manager.get_user_data(db, username)
    for stock in user_data['stocks']:
        recent_data = search.get_exact_stock(stock['stock_name'])
        if recent_data:
            db_manager.update_user_stock(db, username, stock['stock_name'], stock['quantity'], recent_data['clpr'])
    return render_template('profile.html', user_data=user_data)

@app.route('/buystock/<stock_name>', methods=['POST'])
def buystock(stock_name):
    if not session.get('username'):
        return redirect('/login')
    
    username = session.get('username')
    user_data = db_manager.get_user_data(db, username)
    price = int(request.form.get('price').replace(',', ''))
    try:
        stock_quantity = int(request.form.get('buy_quantity'))
    except ValueError:
        return redirect(f'/search')
    
    if price * stock_quantity > user_data['balance']: # 잔액 부족
        return redirect('/search')
    
    user_stocks = db_manager.get_user_stocks(db, username)
    for stock in user_stocks:
        if stock['stock_name'] == stock_name:
            stock['quantity'] += stock_quantity
            db_manager.update_user_stock(db, username, stock_name, stock['quantity'], price)
            db_manager.update_user_balance(db, username, -(price * stock_quantity))
            return redirect('/search')
    db_manager.add_user_stock(db, username, stock_name, stock_quantity, price)
    db_manager.update_user_balance(db, username, -(price * stock_quantity))
    return redirect('/search')
    



# 엑셀 다운로드 엔드포인트 
@app.route('/download/<keyword>', methods=['GET'])
def download_excel(keyword):
    file_path = f"static/{keyword}_news.xlsx"
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    