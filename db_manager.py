from pymongo import MongoClient

def connect_to_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['stock_db']
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def add_user(db, username, password, name, email, money=1000000):
    try:
        users = db['users']
        user_data = {'username': username, 'password': password, 'name': name, 'email': email, 'balance': money}
        users.insert_one(user_data)
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def get_user_data(db, username):
    try:
        users = db['users']
        user_data = users.find_one({'username': username})
        return user_data
    except Exception as e:
        print(f"Error getting user data: {e}")
        return None

def add_user_stock(db, username, stock_name, quantity, current_price):
    try:
        users = db['users']
        if users.find_one({'username': username,'stocks.stock_name': stock_name}):
            update_user_stock(db, username, stock_name, quantity, current_price)
            return True
        
        user_data = users.find_one_and_update(
            {'username': username}, 
            {'$push': 
             {'stocks': 
              {'stock_name': stock_name, 
               'quantity': quantity, 
               'current_price': current_price}}}, upsert=True)
        return True
    except Exception as e:
        print(f"Error adding user stock: {e}")
        return False

def update_user_stock(db, username, stock_name, quantity, current_price):
    try:
        users = db['users']
        if not users.find_one({'username': username,'stocks.stock_name': stock_name}):
            print(f"{username}은 다음 주식을 갖고 있지 않습니다: {stock_name}")
            return False
        
        user_data = users.find_one_and_update(
            {'username': username, 'stocks.stock_name': stock_name},
            {'$set': {'stocks.$.quantity': quantity, 'stocks.$.current_price': current_price}})
        return True
    except Exception as e:
        print(f"주식 업데이트 오류: {e}")
        return False

def get_user_stocks(db, username):
    try:
        users = db['users']
        user_data = users.find_one({'username': username})
        if user_data:
            return user_data.get('stocks', [])
        else:
            return []
    except Exception as e:
        print(f"유저 주식 정보 로드 오류: {e}")
        return []
    
#db = connect_to_mongodb()
#add_user(db, 'testuser', 'testpass', 'Test User', 'test@example.com')
#add_user_stock(db, 'testuser', '삼성', 100, 100.5)
#add_user_stock(db, 'testuser', 'AAPL', 50, 120.5)
#update_user_stock(db, 'testuser', 'AAPL', 100, 120.5)
#print(get_user_stocks(db, 'testuser'))
