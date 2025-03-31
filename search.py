import requests

BASE_URL = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
API_KEY = "6u/cDWo0xCwclFJ3FhYrfsLemMvjJ8QCzrS383qo12i9Deb5QymzQjIXO3+cY8nv3Ak2+jFiRVWUxRKQVJeOIg=="

def search_stock(stock_name):
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

        stocks = []
        for item in items:
            stock_info = {
                "itmsNm": item.get("itmsNm"),        # 종목명
                "clpr": item.get("clpr"),            # 현재가
                "fltRt": item.get("fltRt"),          # 등락률
                "vs": item.get("vs"),                # 전일대비 등락
                "mrkTotAmt": item.get("mrktTotAmt")  # 시가총액
            }
            stocks.append(stock_info)

        return stocks, None

    except Exception as e:
        return None, str(e)
