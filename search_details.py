import requests

BASE_URL = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
API_KEY = "6u/cDWo0xCwclFJ3FhYrfsLemMvjJ8QCzrS383qo12i9Deb5QymzQjIXO3+cY8nv3Ak2+jFiRVWUxRKQVJeOIg=="

def search_stock(stock_code):
    params = {
        "serviceKey": API_KEY,
        "numOfRows": "5",
        "pageNo": "1",
        "resultType": "json",
        "likeSrtnCd": stock_code
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])

        stocks = []

        for item in items:
            stock_info = {
                "itmsNm": item.get("itmsNm"),
                "srtnCd": item.get("srtnCd"),
                "clpr": item.get("clpr"),
                "fltRt": item.get("fltRt"),
                "vs": item.get("vs"),
                "mrkTotAmt": item.get("mrktTotAmt"),
                "basDt": item.get("basDt")
            }
            stocks.append(stock_info)

        return {"stocks": stocks, "error": None}

    except Exception as e:
        return {"stocks": None, "error": str(e)}
