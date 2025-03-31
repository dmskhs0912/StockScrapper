'''from flask import Flask, render_template, request
import requests

app = Flask(__name__)

BASE_URL = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
API_KEY = "6u/cDWo0xCwclFJ3FhYrfsLemMvjJ8QCzrS383qo12i9Deb5QymzQjIXO3+cY8nv3Ak2+jFiRVWUxRKQVJeOIg=="

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])'''
def search(stock_name):
    stock_name = request.form.get('stock_name')

    params = {
        "serviceKey": API_KEY,
        "numOfRows": "5",
        "pageNo": "1",
        "resultType": "json",
        "likeItmsNm": stock_name
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])

        if items:
            return render_template('result.html', stocks=items)
        else:
            return render_template('result.html', stocks=None)

    except Exception as e:
        return render_template('result.html', stocks=None, error=str(e))


#if __name__ == '__main__':
#    app.run(debug=True)