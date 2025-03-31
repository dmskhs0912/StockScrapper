from pymongo import MongoClient

def connect_to_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['stock_db']
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def add_user(db, username, password, name, email):
    try:
        users = db['users']
        user_data = {'username': username, 'password': password, 'name': name, 'email': email}
        users.insert_one(user_data)
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    